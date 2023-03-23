from enum import Enum
from typing import Literal
from pydantic import BaseModel


class Color(str, Enum):
    WHITE = "white"
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    BLACK = "black"
    GOLD = "gold"


GEM_COLORS = {Color.WHITE, Color.BLUE, Color.GREEN, Color.RED, Color.BLACK}
TOKEN_COLORS = {*GEM_COLORS, Color.GOLD}


class PlayerNecessity(str, Enum):
    PERFORM_TURN_ACTION = "act"
    DISCARD_EXCESS_TOKENS = "discard_tokens"
    SELECT_A_NOBLE = "pick_noble"
    END_TURN = "end_turn"


class TokenInventory(BaseModel):
    def add(self, tokens: list[Color]):
        raise NotImplementedError

    def remove(self, tokens: list[Color]):
        raise NotImplementedError

    @property
    def count(self) -> int:
        raise NotImplementedError


class PlayerData(BaseModel):
    tokens: TokenInventory


class Game(BaseModel):
    round_number: int
    turn_number: int
    current_player_needs: set[PlayerNecessity]
    players: list[PlayerData]
    tokens: TokenInventory

    def advance_to_next_turn(self) -> None:
        """
        CAUTION: invoking this while `self.current_player_needs_to` is not empty will skip the current player's turn.
        """
        self.turn_number += 1

        if self.turn_number >= len(self.players):
            self.round_number += 1
            self.turn_number = 0

        self.current_player_needs.clear()
        self.current_player_needs.add(PlayerNecessity.PERFORM_TURN_ACTION)
        self.current_player_needs = self.current_player_needs.union(
            self.get_current_player_additional_needs()
        )

    def get_current_player_additional_needs(self) -> set[PlayerNecessity]:
        """
        NOTE: This does NOT add PlayerNecessity.PERFORM_TURN_ACTION to the set of needs returned.
        """
        self.current_player_needs.clear()

        # TODO: Check if the player needs to act.

        raise NotImplementedError


class ErrorDetail(BaseModel):
    check_failed: str
    detail: str


ValidationSuccessResponse = tuple[Literal[True], Game]
ValidationErrorResponse = tuple[Literal[False], list[ErrorDetail]]
ValidationResponse = ValidationErrorResponse | ValidationSuccessResponse


def do_current_player_action_take_tokens(
    game: Game, tokens_to_take: list[Color]
) -> ValidationResponse:
    """
    Returns a tuple with two values:
    - If the action succeeded, then the first value is True and the second value is the game's state after the change.
    - If the action failed, then the first value is False and the second value is a list of reasons why the action failed.
    """
    errors = [
        error_detail
        for error_detail in [
            check_current_player_must_take_action(game),
            check_tokens_are_gem_colors(tokens_to_take),
            check_no_more_than_3_tokens_taken(tokens_to_take),
            check_3_tokens_taken_must_be_all_different_colors(tokens_to_take),
            check_2_tokens_taken_of_same_color_4_must_remain(game, tokens_to_take),
            check_tokens_are_available(game, tokens_to_take),
        ]
        if error_detail is not None
    ]

    if errors:
        return False, errors

    # Perform the action.
    game_after_action = game.copy()
    player_after_action = game.players[game.turn_number].copy()

    game_after_action.tokens.remove(tokens_to_take)
    player_after_action.tokens.add(tokens_to_take)

    game_after_action.players[game.turn_number] = player_after_action

    # Indicate whether or not the player now needs to discard tokens.
    if player_after_action.tokens.count > 10:
        game_after_action.current_player_needs.add(
            PlayerNecessity.DISCARD_EXCESS_TOKENS
        )

    # Indicate that the player has acted.
    game_after_action.current_player_needs.discard(PlayerNecessity.PERFORM_TURN_ACTION)

    # If nothing remains to be done, advance to the next turn.
    if all(
        possible_need not in game_after_action.current_player_needs
        for possible_need in [
            PlayerNecessity.DISCARD_EXCESS_TOKENS,
            PlayerNecessity.SELECT_A_NOBLE,
        ]
    ):
        game_after_action.advance_to_next_turn()

    return True, game_after_action


def check_current_player_must_take_action(game: Game) -> ErrorDetail | None:
    raise NotImplementedError


def check_no_more_than_3_tokens_taken(
    tokens_to_take: list[Color],
) -> ErrorDetail | None:
    raise NotImplementedError


def check_tokens_are_gem_colors(tokens_to_take: list[Color]) -> ErrorDetail | None:
    raise NotImplementedError


def check_3_tokens_taken_must_be_all_different_colors(
    tokens_to_take: list[Color],
) -> ErrorDetail | None:
    raise NotImplementedError


def check_2_tokens_taken_of_same_color_4_must_remain(
    game: Game,
    tokens_to_take: list[Color],
) -> ErrorDetail | None:
    raise NotImplementedError


def check_tokens_are_available(
    game: Game, tokens_to_take: list[Color]
) -> ErrorDetail | None:
    raise NotImplementedError
