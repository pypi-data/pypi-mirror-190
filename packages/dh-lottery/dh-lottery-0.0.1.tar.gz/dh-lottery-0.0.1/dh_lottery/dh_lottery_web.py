"""동행 복권."""
import datetime
import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from . import const
from .const import DH_HISTORY_URL
from .error import DhLotteryError, DhWebTimeout
from .model import BuyGame, BuyReceipt, GameMode, History, Receipt, WeekHistory
from .util import get_random_nums

_LOGGER = logging.getLogger(__name__)


class DhLotteryWeb:
    """동행 복권."""

    def __init__(self, host: str):
        self.host = host
        self.driver: WebDriver | None = None

    def driver_init(self, _headless=False) -> None:
        """WebDriver 초기화."""
        options = Options()
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36",
        )
        options.set_preference("general.platform.override", "Win32")
        self.driver = webdriver.Remote(
            self.host, options=options, desired_capabilities=DesiredCapabilities.FIREFOX
        )

    def driver_quit(self):
        """WebDriver 종료."""
        if self.driver:
            self._remove_popup()

            self.driver.quit()
            self.driver = None

    def login(self, user_id: str, user_pw: str) -> bool:
        """로그인."""
        try:
            # 로그인 페이지 이동
            self.driver.get(const.DH_LOGIN_URL)
            # 아이디 입력
            self.driver.find_element(By.XPATH, '//input[@name="userId"]').send_keys(
                user_id
            )
            # 비밀번호 입력
            self.driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(
                user_pw
            )
            # 로그인 실행
            self.driver.execute_script("javascript:check_if_Valid3();")

            WebDriverWait(self.driver, 5).until(
                lambda d: d.current_url == const.DH_MAIN_URL
            )
            self._remove_popup()  # 팝업창 제거함수 호출
            return True
        except TimeoutException as timeout_error:
            raise DhWebTimeout("[로그인] 타임아웃") from timeout_error
        except UnexpectedAlertPresentException as alert_error:
            raise DhLotteryError(f"[로그인] 오류, {alert_error.alert_text}") from alert_error

    def get_deposit(self) -> int:
        """예치금 가져오기."""
        try:
            # 마이페이지로 이동
            self.driver.get(url=const.DH_MY_PAGE_URL)
            # 예치금 금액 읽음
            deposit = WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(
                    By.XPATH, '//p[@class="total_new"]/strong'
                ).text
            )
            return int(deposit.replace(",", ""))  # 천단위 쉼표 제거
        except TimeoutException as timeout_error:
            raise DhWebTimeout("[예치금] 타임아웃") from timeout_error

    def _remove_popup(self) -> None:
        """팝업 제거."""
        # 생성된 팝업창을 모두 닫음
        _tabs = self.driver.window_handles
        while len(_tabs) != 1:
            self.driver.switch_to.window(_tabs[1])
            self.driver.close()
            _tabs = self.driver.window_handles

        # 첫 창으로 돌아간다
        self.driver.switch_to.window(_tabs[0])

    def _parse_receipt(self, row_path: str, screen_path: str) -> Receipt:
        """로또 영수증 파서."""
        _rows = WebDriverWait(self.driver, 5).until(
            lambda d: d.find_elements(By.XPATH, row_path)
        )
        # 구매된 번호들을 인식
        games = [
            [
                int(col.text)
                for col in row.find_elements(By.XPATH, 'div[@class="nums"]/span')
            ]
            for row in _rows
        ]
        paper = self.driver.find_element(By.ID, screen_path)
        receipt = Receipt(games, paper.screenshot_as_png)
        self._remove_popup()
        return receipt

    def _prepare_buy_lotto(self) -> str:
        """로또 구매 준비."""
        try:
            # 메인 페이지로 이동
            self.driver.get(const.DH_MAIN_URL)
            WebDriverWait(self.driver, 5).until(lambda d: len(d.window_handles) >= 1)
            # 팝업창 닫음
            self._remove_popup()

            handle_cnt = len(self.driver.window_handles)
            # 로또 구매 페이지로 이동
            self.driver.execute_script("javascript:goLottoBuy(2);")
            # 생성된 구매 페이지로 전환
            WebDriverWait(self.driver, 5).until(
                lambda d: len(d.window_handles) > handle_cnt
            )
            self.driver.switch_to.window(self.driver.window_handles[1])
            # 내부 iframe으로 전환
            self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, "iframe"))

            return (
                WebDriverWait(self.driver, 10)
                .until(lambda d: d.find_element(By.ID, "curRound"))
                .text
            )

        except TimeoutException as timeout_error:
            raise DhWebTimeout("[구매 준비] 타임아웃") from timeout_error
        except UnexpectedAlertPresentException as alert_error:
            raise DhLotteryError(
                f"[구매 준비] 오류, {alert_error.alert_text}"
            ) from alert_error

    def _select_game(self, game: BuyGame) -> None:
        """로또 번호 선택."""

        def set_auto():
            self.driver.find_element(
                By.XPATH, '//label[@for="checkAutoSelect"]'
            ).click()

        def set_nums(nums: list[int]):
            for num in nums:
                self.driver.find_element(
                    By.XPATH, f'//label[@for="check645num{num}"]'
                ).click()
            if len(nums) < 6:
                set_auto()

        # 자동모드
        if game.mode == GameMode.AUTO:
            set_auto()
            return

        if game.mode == GameMode.MANUAL:  # 수동모드, 혼합모드 (숫자 일부 지정, 나머지 자동)
            set_nums(game.nums)
            return

        set_nums(get_random_nums())
        # 수량 입력 확인
        self.driver.find_element(By.XPATH, '//input[@id="btnSelectNum"]').click()

    def buy_lotto(self, items: list[BuyGame], dry=False) -> BuyReceipt:
        """로또 구매."""
        cur_round = self._prepare_buy_lotto()
        buy_receipt = BuyReceipt([], bytes(), cur_round)

        for item in items:
            self._select_game(item)

        if dry:
            #  dry run, 구매 번호 지정된 화면만 캡쳐 후 종료
            tag = self.driver.find_element(By.CLASS_NAME, "selected-games")
            buy_receipt.screen_shot = tag.screenshot_as_png
            self._remove_popup()
            return buy_receipt

        # 구매하기 버튼
        self.driver.find_element(By.XPATH, '//input[@id="btnBuy"]').click()
        # 최종 구매 확인
        self.driver.execute_script("javascript:closepopupLayerConfirm(true);")

        receipt = self._parse_receipt('//ul[@id="reportRow"]/li', "popReceipt")
        buy_receipt.games = receipt.games
        buy_receipt.screen_shot = receipt.screen_shot
        # iframe에서 기본 창으로 다시 변경
        self.driver.switch_to.default_content()
        return buy_receipt

    def get_history(self) -> WeekHistory:
        """구매내역."""

        def get_receipt() -> Receipt:
            handle_cnt = len(self.driver.window_handles)
            nums: WebElement = data[3].find_element(By.TAG_NAME, "a")
            self.driver.execute_script(nums.get_property("href"))
            WebDriverWait(self.driver, 5).until(
                lambda d: len(d.window_handles) > handle_cnt
            )
            self.driver.switch_to.window(self.driver.window_handles[handle_cnt])
            receipt = self._parse_receipt(
                '//*[@id="popup645paper"]/div[2]/ul/li', "popup645paper"
            )
            self.driver.switch_to.default_content()
            return receipt

        try:
            now = datetime.datetime.now()
            start_date = (now + datetime.timedelta(weeks=-1)).strftime("%Y%m%d")
            end_date = now.strftime("%Y%m%d")

            self.driver.get(
                DH_HISTORY_URL.format(start_date=start_date, end_date=end_date)
            )
            items = WebDriverWait(self.driver, 10).until(
                lambda d: d.find_elements(By.XPATH, "/html/body/table/tbody/tr")
            )
            week_history = WeekHistory(0, [])
            for rows in items:
                data = rows.find_elements(By.TAG_NAME, "td")
                if len(data) == 1:  # 조회 결과가 없습니다.
                    break
                history = History(data)
                if history.name != "로또6/45":
                    continue
                # history.receipt = get_receipt()

                week_history.items.append(history)
                week_history.count += history.count
            self.driver.switch_to.default_content()

            tag = self.driver.find_element(By.TAG_NAME, "table")
            week_history.screen_shot = tag.screenshot_as_png
            return week_history
        except TimeoutException as timeout_error:
            raise DhWebTimeout("[구매내역] 타임아웃") from timeout_error

    def get_none_grade_history(self) -> WeekHistory:
        """미추첨 구매내역."""
        history = self.get_history()
        history.items = list(filter(lambda x: "미추첨" in x.result, history.items))
        return history
