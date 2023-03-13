from dataclasses import dataclass
from enum import Enum
from itertools import groupby

GameId = str
PlayerId = str
EntityId = str

POINTS_NEEDED_TO_TRIGGER_ENDGAME = 15
NOBLE_POINT_VALUE = 3


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


@dataclass
class Card:
    id: EntityId
    tier: CardTier
    points: int
    cost: dict[GemColor, int]


@dataclass
class Noble:
    id: EntityId
    cost: dict[GemColor, int]


@dataclass
class Token:
    id: EntityId
    color: TokenColor


@dataclass
class Player:
    id: PlayerId
    cards_purchased: list[Card]
    cards_reserved: list[Card]
    nobles: list[Noble]
    tokens: list[Token]

    @property
    def total_points(self) -> int:
        points_from_cards = sum(card.points for card in self.cards_purchased)
        points_from_nobles = len(self.nobles) * NOBLE_POINT_VALUE
        return points_from_cards + points_from_nobles


@dataclass
class GameState:
    id: GameId
    turn_number: int
    players: list[Player]
    decks: dict[CardTier, list[Card]]
    tokens: list[Token]
    nobles: list[Noble]

    @property
    def endgame_is_triggered(self) -> bool:
        if any(
            player.total_points >= POINTS_NEEDED_TO_TRIGGER_ENDGAME
            for player in self.players
        ):
            return True

        return False

    @property
    def index_of_current_player(self) -> int:
        return self.turn_number % self.player_count

    @property
    def player_count(self) -> int:
        return len(self.players)

    @property
    def winner(self) -> list[PlayerId]:
        """
        There is no winner if endgame has not been triggered.
        The player with the most points wins.
        If tied for points, the player with the fewest cards purchased wins.
        If tied for cards, all tied players win.
        """

        if not self.endgame_is_triggered:
            return []

        raise NotImplementedError("This method is incomplete.")
