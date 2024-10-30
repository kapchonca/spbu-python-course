import pytest
from project.blackjack.src.game import Game
from project.blackjack.src.players import BotPlayer
from project.blackjack.src.strategies import (
    AccurateStrategy,
    AggressiveStrategy,
    CountingStrategy,
)


@pytest.fixture
def setup_game():
    """Fixture to set up a game instance for testing."""
    conservative = AccurateStrategy()
    aggressive = AggressiveStrategy()
    counting = CountingStrategy()

    players = [
        BotPlayer("AccurateBot", conservative),
        BotPlayer("AggressiveBot", aggressive),
        BotPlayer("CountingBot", counting),
    ]
    game = Game(players, max_rounds=5)
    return game


@pytest.mark.parametrize("rounds_played, expected_round", [(1, 1), (3, 3), (5, 5)])
def test_game_state_changes_over_time(setup_game, rounds_played, expected_round):
    """
    Test to ensure that the game's round counter and state change correctly over time.

    Args:
        setup_game (Game): The game instance initialized via fixture.
        rounds_played (int): Number of rounds to simulate playing.
        expected_round (int): Expected round counter value.
    """
    game = setup_game
    for _ in range(rounds_played):
        game.play_round()

    assert (
        game._round == expected_round
    ), f"Expected round to be {expected_round} but got {game._round}"


def test_deal_initial_cards(setup_game):
    """
    Test the deal_initial_cards method to verify that each player and the dealer receive initial cards.

    Args:
        setup_game (Game): The game instance initialized via fixture.
    """
    game = setup_game
    game.deal_initial_cards()

    for player in game._players:
        assert len(player.hand._cards) == 2, f"{player.name} did not receive 2 cards."
    assert (
        len(game._dealer.hand._cards) == 1
    ), "Dealer did not receive their visible card."
    assert (
        game._dealer._hidden_card is not None
    ), "Dealer did not receive a hidden card."


@pytest.mark.parametrize(
    "player_value, dealer_value, expected_result",
    [
        (22, 18, "lose"),  # Player busts
        (19, 22, "win"),  # Dealer busts
        (20, 19, "win"),  # Player wins
        (18, 20, "lose"),  # Dealer wins
        (20, 20, "push"),  # Tie
    ],
)
def test_settle_bets(setup_game, player_value, dealer_value, expected_result):
    """
    Test the settle_bets method to verify the correct outcome of a round based on player and dealer values.

    Args:
        setup_game (Game): The game instance initialized via fixture.
        player_value (int): Simulated value of the player's hand.
        dealer_value (int): Simulated value of the dealer's hand.
        expected_result (str): The expected result (win, lose, or push).
    """
    game = setup_game
    player = game._players[0]
    player.hand._value = player_value
    game._dealer.hand._value = dealer_value
    print(player.hand._value, game._dealer.hand._value)
    initial_chips = player.chips
    player._bet = 10

    game.settle_bets()
    print(player.chips)
    if expected_result == "win":
        assert (
            player.chips == initial_chips + 10
        ), "Player did not receive correct chips for a win."
    elif expected_result == "lose":
        assert (
            player.chips == initial_chips - 10
        ), "Player did not lose correct chips for a loss."
    elif expected_result == "push":
        assert (
            player.chips == initial_chips
        ), "Player did not get their bet back on a push."


def test_game_state_progress(setup_game):
    """
    Test to ensure that the game's state (round count, deck size, player chips, etc.) changes over time.

    Args:
        setup_game (Game): The game instance initialized via fixture.
    """
    game = setup_game

    initial_round = game._round
    initial_deck_size = len(game._deck._cards)

    rounds_to_play = 2
    for _ in range(rounds_to_play):
        game.play_round()

    assert (
        game._round == initial_round + rounds_to_play
    ), "Round count did not increment correctly."

    assert (
        len(game._deck._cards) < initial_deck_size
    ), "Deck size did not decrease after playing rounds."
