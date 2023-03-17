from enum import Enum


class GemColor(str, Enum):
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    WHITE = "white"


class TokenColor(GemColor):
    GOLD = "gold"


class CardLevel(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class Card:
    id: str
    color: GemColor
    level: CardLevel
    cost: dict[GemColor, int]
    points: int


class Noble:
    id: str
    cost: dict[GemColor, int]


class Player:
    id: str
    tokens: dict[TokenColor, int]
    cards_bought: list[Card]
    cards_reserved: list[Card]
    nobles: list[Noble]


class Game:
    turn: int
    players: list[Player]
    tokens: dict[TokenColor, int]
    cards: dict[CardLevel, list[Card]]
    nobles: list[Noble]
