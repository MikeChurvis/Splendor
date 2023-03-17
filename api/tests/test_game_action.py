import pytest
from ..main import Game, Player, TokenColor, GemColor


@pytest.fixture
def default_player() -> Player:
    return Player(
        id="default-player",
        tokens={},
        cards_bought=[],
        cards_reserved=[],
        nobles=[],
    )


def test_take_3_tokens_of_different_colors_succeeds(default_player: Player):
    game = Game(
        turn=0,
        players=[default_player],
        cards={},
        nobles=[],
        tokens={
            GemColor.BLACK: 1,
            GemColor.RED: 1,
            GemColor.GREEN: 1,
        },
    )

    pytest.fail("Test not implemented.")

    # action = TakeThreeTokensAction(
    #     default_player.id, set((GemColor.BLACK, GemColor.RED, GemColor.GREEN))
    # )
