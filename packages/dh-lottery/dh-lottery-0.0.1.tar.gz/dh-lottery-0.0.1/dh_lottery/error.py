"""복권 오류"""


class DhLotteryError(Exception):
    """복권 사이트 오류"""

    def __init__(self, message):
        super().__init__(message)


class DhWebTimeout(DhLotteryError):
    """복권 타임아웃 오류"""
