from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional
from project.blackjack.src.strategies import Strategy
from project.blackjack.src.objects import Card, Hand


class BetStates(Enum):
    WIN = 1
    LOSE = 2
    PUSH = 3


class Player(ABC):
    """
    Represents a player in the game.

    Attributes:
        name (str): The name of the player.
        hand (Hand): The player's current hand.
        chips (int): The number of chips the player has.
        bet (int): The player's current bet.
    """

    def __init__(self, name: str, chips: int = 1000) -> None:
        """
        Initializes a Player with a given name and initial chips.

        Args:
            name (str): The name of the player.
            chips (int): The initial number of chips the player has. Defaults to 1000.
        """
        self.name: str = name
        self.hand: Hand = Hand()
        self.chips: int = chips
        self._bet: int = 0

    def settle_bet(self, bet_state: BetStates) -> None:
        if bet_state == BetStates.WIN:
            self.chips += self._bet
        elif bet_state == BetStates.LOSE:
            self.chips -= self._bet
        elif bet_state == BetStates.PUSH:
            pass
        self._bet = 0

    def place_bet(self, amount: int) -> None:
        """
        Places a bet for the player, subtracting the amount from their chips.

        Args:
            amount (int): The amount to bet.
        """
        amount = min(amount, self.chips)
        self._bet = amount

    @abstractmethod
    def decide_hit(self) -> bool:
        pass

    def __str__(self) -> str:
        """
        Returns the string representation of the player, their hand, and their chips.

        Returns:
            str: A string describing the player.
        """
        return f"{self.name}: {self.hand} | Chips: {self.chips}"


class BotPlayer(Player):
    """
    Represents a bot player with a strategy.

    Attributes:
        _strategy (Strategy): The bot's strategy for playing.
    """

    def __init__(self, name: str, strategy: Strategy, chips: int = 1000) -> None:
        """
        Initializes a BotPlayer with a name, strategy, and initial chips.

        Args:
            name (str): The name of the bot player.
            strategy (Strategy): The strategy for the bot.
            chips (int): The initial number of chips the bot has. Defaults to 1000.
        """
        super().__init__(name, chips)
        self._strategy: Strategy = strategy

    def decide_hit(self) -> bool:
        """
        Decides whether to hit based on the bot's strategy.

        Returns:
            bool: Decision to hit.
        """
        return self._strategy.decide_hit(self.hand)


class Dealer(Player):
    """
    Represents the dealer in the game.

    Attributes:
        _hidden_card (Optional[Card]): The dealer's hidden card.
    """

    def __init__(self) -> None:
        """
        Initializes the Dealer with a default name of "Dealer".
        """
        super().__init__("Dealer")
        self._hidden_card: Optional[Card] = None

    def reveal_hidden_card(self) -> Optional[Card]:
        """
        Reveals the dealer's hidden card.

        Returns:
            Optional[Card]: The dealer's hidden card.
        """
        return self._hidden_card

    def decide_hit(self) -> bool:
        """
        Dealer hits until the hand value is 17 or higher.
        """
        return self.hand.value < 17

    def __str__(self) -> str:
        """
        Returns the string representation of the dealer's hand, with one card hidden.

        Returns:
            str: A string describing the dealer.
        """
        return f"Dealer: {self.hand._cards[0]}, Hidden"
