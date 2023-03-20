from dataclasses import dataclass
from enum import Enum
from typing import Literal


CardLevel = Literal[1, 2, 3]


class GemColor(str, Enum):
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    WHITE = "white"


TokenColor = GemColor | Literal["gold"]


@dataclass
class Noble:
    id: str
    cost: dict[GemColor, int]


@dataclass
class Card:
    id: str
    level: CardLevel
    points: int
    color: GemColor
    cost: dict[GemColor, int]


@dataclass
class PlayerData:
    cards_owned: dict[GemColor, list[Card]]
    cards_reserved: list[Card]
    tokens: dict[TokenColor, int]
    nobles: list[Noble]


@dataclass
class GameData:
    round_number: int
    this_turns_player_index: int
    players: list[PlayerData]
    cards: dict[CardLevel, list[Card]]
    tokens: dict[TokenColor, int]
    nobles: list[Noble]


def validate_action__actor_is_this_turns_player(
    game: GameData, player_index: int
) -> list[str]:
    """
    Returns a list of the problems with the proposed action.
    If the list is empty, there are no problems.
    """
    errors = []

    # The actor must be the player whose turn it is.
    if game.this_turns_player_index != player_index:
        errors.append("It is not your turn.")

    return errors


def validate_action_take_tokens(
    game: GameData,
    player_index: int,
    tokens_taken: list[GemColor],
    tokens_put_back: list[GemColor],
) -> list[str]:
    """
    Returns an exhaustive list of the problems with the proposed Take Tokens action.
    If the list is empty, there are no problems.
    """
    # Check that it's your turn.
    errors = validate_action__actor_is_this_turns_player(game, player_index)

    # Check rule violations.
    colors_of_tokens_taken = set(tokens_taken)

    taking_more_than_3_tokens = len(tokens_taken) > 3

    taking_3_with_more_than_one_of_a_color = (
        len(tokens_taken) == 3 and len(colors_of_tokens_taken) != 3
    )

    taking_2_of_same_color_when_fewer_than_4_exist = (
        len(tokens_taken) == 2
        and len(colors_of_tokens_taken) == 1
        and len(game.tokens[tokens_taken[0]]) < 4
    )

    if taking_more_than_3_tokens:
        errors.append("You may not take more than three tokens.")
    elif taking_3_with_more_than_one_of_a_color:
        errors.append("You must take all different colors when taking three tokens.")
    elif taking_2_of_same_color_when_fewer_than_4_exist:
        errors.append(
            "You may not take two tokens of the same color if fewer than four are available."
        )

    # Check game inventory.
    for color in colors_of_tokens_taken:
        if game.tokens[color] == 0:
            errors.append(f"There are no {color} tokens available.")

    # TODO: Check hand limit and tokens returned

    # TODO: Check tokens returned

    return errors
