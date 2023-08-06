"""Model"""
from dataclasses import dataclass
from enum import Enum, auto

from selenium.webdriver.remote.webelement import WebElement


class GameMode(Enum):
    """로또 구매 모드."""

    AUTO = auto()
    MANUAL = auto()
    SEL_AUTO = auto()


@dataclass
class BuyGame:
    """로또 1게임."""

    mode: GameMode
    nums: list[int] | None = None


@dataclass
class Receipt:
    """로또 구입 영수증"""

    games: list[list[int]]
    screen_shot: bytes


@dataclass
class BuyReceipt(Receipt):
    """로또 구매."""

    cur_round: str


@dataclass
class History:
    """로또 구입 내역"""

    def __init__(self, row: list[WebElement]):
        self.buy_date = row[0].text
        self.name = row[1].text
        self.round = row[2].text
        self.nums = row[3].text
        self.count = int(row[4].text)
        self.result = row[5].text
        self.winnings = row[6].text
        self.lottery_date = row[7].text
        self.receipt: Receipt | None = None


@dataclass
class WeekHistory:
    """미추첨 구매내역."""

    count: int
    items: list[History]
    screen_shot: bytes | None = None
