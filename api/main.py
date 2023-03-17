from enum import Enum
from dataclasses import dataclass


class GemColor(str, Enum):
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    WHITE = "white"


class TokenColor(str, Enum):
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    WHITE = "white"
    GOLD = "gold"


class CardLevel(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3


@dataclass
class Card:
    id: str
    color: GemColor
    level: CardLevel
    cost: dict[GemColor, int]
    points: int


@dataclass
class Noble:
    id: str
    cost: dict[GemColor, int]


@dataclass
class Player:
    id: str
    tokens: dict[TokenColor, int]
    cards_bought: list[Card]
    cards_reserved: list[Card]
    nobles: list[Noble]


@dataclass
class Game:
    turn: int
    players: list[Player]
    tokens: dict[TokenColor, int]
    cards: dict[CardLevel, list[Card]]
    nobles: list[Noble]
