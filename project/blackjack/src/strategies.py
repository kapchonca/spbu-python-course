from abc import ABC, abstractmethod
from project.blackjack.src.objects import Card, Hand


class Strategy(ABC):
    """
    Base class for different playing strategies.
    """

    @abstractmethod
    def decide_hit(self, hand: Hand) -> bool:
        """
        Determines whether the player should hit based on their strategy.

        Raises:
            NotImplementedError: If not overridden by a subclass.
        """
        pass


class AccurateStrategy(Strategy):
    """
    Strategy where the player hits if the hand value is less than 14.
    """

    def decide_hit(self, hand: Hand) -> bool:
        """
        Decides whether to hit based on the current hand value.

        Args:
            hand (Hand): The player's current hand.

        Returns:
            bool: True if the hand value is less than 14, False otherwise.
        """
        return hand.value < 14


class AggressiveStrategy(Strategy):
    """
    Strategy where the player hits if the hand value is less than 17.
    """

    def decide_hit(self, hand: Hand) -> bool:
        """
        Decides whether to hit based on the current hand value.

        Args:
            hand (Hand): The player's current hand.

        Returns:
            bool: True if the hand value is less than 17, False otherwise.
        """
        return hand.value < 17


class CountingStrategy(Strategy):
    """
    Strategy that uses card counting to decide whether to hit.

    Attributes:
        _count (int): The count value that tracks the advantage in the deck.
    """

    def __init__(self) -> None:
        """
        Initializes a CountingStrategy with a count of zero.
        """
        self._count: int = 0

    def update_count(self, card: Card) -> None:
        """
        Updates the count based on the card dealt.

        Args:
            card (Card): The card to update the count with.
        """
        if card.rank in ["2", "3", "4", "5", "6"]:
            self._count += 1
        elif card.rank in ["10", "J", "Q", "K", "A"]:
            self._count -= 1

    def decide_hit(self, hand: Hand) -> bool:
        """
        Decides whether to hit based on the hand value and count.

        Args:
            hand (Hand): The player's current hand.

        Returns:
            bool: Decision to hit based on count and hand value.
        """
        if self._count > 2:
            return hand.value < 19
        elif self._count < -2:
            return hand.value < 16
        else:
            return hand.value < 17
