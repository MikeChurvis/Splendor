from enum import Enum

PlayerId = str
EntityId = str


class CardTier(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class GemColor(str, Enum):
    WHITE = "white"
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    BLACK = "black"


class TokenColor(GemColor):
    GOLD = "gold"


class Card:
    id: EntityId
    tier: CardTier
    points: int
    cost: dict[GemColor, int]


class Noble:
    id: EntityId
    cost: dict[GemColor, int]


class Token:
    id: EntityId
    color: TokenColor


class Player:
    id: PlayerId
    cards_purchased: list[Card]
    cards_reserved: list[Card]
    nobles_earned: list[Noble]
    tokens: list[Token]


class GameState:
    turn_number: int
    players: list[Player]
    decks: dict[CardTier, list[Card]]
    tokens: list[Token]
    nobles: list[Noble]
