""" Const """

BUY_LIMIT_COUNT = 5

DH_URL = "https://www.dhlottery.co.kr"
DH_LOTTO_NUMBER_URL = f"{DH_URL}/common.do?method=getLottoNumber&drwNo=861"
DH_LOGIN_URL = f"{DH_URL}/user.do?method=login&returnUrl="
DH_MY_PAGE_URL = f"{DH_URL}/userSsl.do?method=myPage"
DH_MAIN_URL = f"{DH_URL}/common.do?method=main"
DH_HISTORY_URL = (
    f"{DH_URL}/myPage.do?method=lottoBuyList&lottoId=LO40&nowPage=1"
    "&searchStartDate={start_date}&searchEndDate={end_date}"
)
