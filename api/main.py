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


class PurchasableCardLocation(int, Enum):
    FIRST_COLUMN = 0
    SECOND_COLUMN = 1
    THIRD_COLUMN = 2
    FOURTH_COLUMN = 3
    TOP_OF_DECK = 4


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
    decks: dict[CardLevel, list[Card]]
    trade_rows: dict[
        CardLevel, tuple[Card | None, Card | None, Card | None, Card | None]
    ]
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


def validate_action__take_tokens(
    game: GameData,
    player_index: int,
    *,
    tokens_taken: list[GemColor],
    tokens_returned: list[TokenColor] = [],
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

    # Check tokens returned.
    if len(tokens_returned) > len(tokens_taken):
        errors.append("You may not return more tokens than you have taken.")

    combined_token_counts = game.players[player_index].tokens.copy()

    for color in tokens_taken:
        combined_token_counts[color] += 1

    for color in tokens_returned:
        combined_token_counts[color] -= 1

    for color, count in combined_token_counts.items():
        if count < 0:
            errors.append(f"You don't have enough {color} tokens to return that many.")

    # Check token count at end of round.
    total_token_count_after_action = sum(combined_token_counts.values())

    if total_token_count_after_action > 10:
        errors.append(
            f"You must put back {total_token_count_after_action - 10} more tokens to bring your total down to 10."
        )

    return errors


def validate_action__purchase_card(
    game: GameData,
    player_index: int,
    *,
    card_location: CardLevel | Literal["reserve"],
    card_index: int,
    tokens_returned: list[GemColor] = [],
) -> list[str]:
    """
    Returns a list of the problems with the proposed Purchase Card action.
    If the list is empty, there are no problems.
    """
    errors = validate_action__actor_is_this_turns_player(game, player_index)

    player = game.players[player_index]

    # Check that the card is available.
    card_to_buy = None

    # Check the player's reserve for the card.
    if card_location == "reserve":
        if card_index not in range(3):
            errors.append(
                f"Position {card_index} is out of bounds for a reserved card."
            )
        elif len(player.cards_reserved) <= card_index:
            errors.append(f"You do not have a reserved card at position {card_index}.")
        else:
            card_to_buy = player.cards_reserved[card_index]

    # Check the trade rows for the card.
    elif card_location in CardLevel:
        if card_index not in range(4):
            errors.append(
                f"Position {card_index} is out of bounds for a card in the trade row."
            )
        elif game.trade_rows[card_location] is None:
            errors.append(
                f"There is no card at position {card_index} in the trade row at level {card_location}."
            )
        else:
            card_to_buy = game.trade_rows[card_location][card_index]

    # There are no other places the card can be.
    else:
        errors.append(
            f'{card_location} is not a valid location wherein cards may be purchased. Valid locations are "reserve", 1, 2, or 3.'
        )

    if card_to_buy is None:
        return errors

    # Now that the card is located, check that the player can pay for it.
    gems_on_cards_owned = {
        gem_color: len(card_list) for gem_color, card_list in player.cards_owned.items()
    }

    tokens_needed_to_buy_card = card_to_buy.cost.copy()

    for color, count in gems_on_cards_owned.items():
        tokens_needed_to_buy_card[color] -= count

    tokens_needed_to_buy_card = {
        color: count for color, count in tokens_needed_to_buy_card.items() if count > 0
    }

    # TODO: Compare the token cost of the card against the player's inventory.

    return errors


def validate_action__reserve_card(
    game: GameData,
    player_index: int,
    *,
    card_id: str | None = None,
    top_of_deck: CardLevel | None = None,
    tokens_returned: list[TokenColor] = [],
) -> list[str]:
    """
    Returns a list of the problems with the proposed action.
    If the list is empty, there are no problems.
    """
    errors = validate_action__actor_is_this_turns_player(game, player_index)

    # Check that the player can pay for the card.

    return errors
