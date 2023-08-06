"""동행 복권."""
import logging

from dh_lottery.const import BUY_LIMIT_COUNT
from dh_lottery.dh_lottery_web import DhLotteryWeb
from dh_lottery.error import DhLotteryError
from dh_lottery.model import BuyGame, BuyReceipt, GameMode

_LOGGER = logging.getLogger(__name__)


class DhLottery(DhLotteryWeb):
    """동행 복권."""

    def buy_count(self, count: int, dry=False) -> BuyReceipt:
        """동행 복권 구매."""
        items = [BuyGame(GameMode.SEL_AUTO) for _ in range(count)]
        return self.buy(items, dry)

    def buy(self, items: list[BuyGame], dry=False) -> BuyReceipt:
        """동행 복권 구매."""
        none_grade_cnt = self.get_none_grade_history()

        available_count = BUY_LIMIT_COUNT - none_grade_cnt.count
        if available_count <= 0:
            raise DhLotteryError(f"일일 구매 한도 {BUY_LIMIT_COUNT}개를 초과하였습니다.")
        if available_count - len(items) < 0:
            _LOGGER.warning("일일 구매 한도를 초과하여, 앞에 %d개만 구매합니다.", available_count)
            items = items[:available_count]

        deposit = self.get_deposit()
        buy_money = len(items) * 1000
        if buy_money > deposit:
            raise DhLotteryError(f"예치금이 부족합니다. {buy_money}/{deposit}원")

        buy_receipt = self.buy_lotto(items, dry)
        message = f"{buy_receipt.cur_round}회 {len(buy_receipt.games)}게임 구매 성공, {buy_receipt.games}"
        _LOGGER.info(message)
        return buy_receipt
