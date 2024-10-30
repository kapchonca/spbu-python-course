import random
from typing import Dict, List

SUITS: List[str] = ["♥", "♦", "♣", "♠"]
RANKS: List[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
VALUES: Dict[str, int] = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}


class Card:
    """
    Represents a playing card with a suit and rank.

    Attributes:
        _suit (str): The suit of the card.
        _rank (str): The rank of the card.
    """

    def __init__(self, suit: str, rank: str) -> None:
        """
        Initializes a card with a given suit and rank.

        Args:
            suit (str): The suit of the card.
            rank (str): The rank of the card.
        """
        self._suit: str = suit
        self._rank: str = rank

    @property
    def suit(self) -> str:
        """Returns the suit of the card."""
        return self._suit

    @property
    def rank(self) -> str:
        """Returns the rank of the card."""
        return self._rank

    def __str__(self) -> str:
        """
        Returns the string representation of the card.

        Returns:
            str: A string in the format 'RankSuit'.
        """
        return f"{self._rank}{self._suit}"


class Deck:
    """
    Represents a deck of playing cards.

    Attributes:
        _cards (List[Card]): A list of Card objects representing the deck.
    """

    def __init__(self) -> None:
        """
        Initializes the deck with a standard set of 52 cards and shuffles it.
        """
        self._cards: List[Card] = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self._cards)

    def deal_card(self) -> Card:
        """
        Deals a card from the deck. If the deck is empty, it reinitializes it.

        Returns:
            Card: The card dealt from the deck.
        """
        if not self._cards:
            self._cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
            random.shuffle(self._cards)
        return self._cards.pop()


class Hand:
    """
    Represents a player's hand in a card game.

    Attributes:
        _cards (List[Card]): A list of Card objects representing the hand.
        _value (int): The total value of the hand.
        _aces (int): The number of aces in the hand.
    """

    def __init__(self) -> None:
        """
        Initializes an empty hand.
        """
        self._cards: List[Card] = []
        self._value: int = 0
        self._aces: int = 0

    def add_card(self, card: Card) -> None:
        """
        Adds a card to the hand and adjusts the hand's value.

        Args:
            card (Card): The card to be added to the hand.
        """
        self._cards.append(card)
        self._value += VALUES[card.rank]
        if card.rank == "A":
            self._aces += 1
        self._adjust_for_ace()

    def _adjust_for_ace(self) -> None:
        """
        Adjusts the value of the hand if there are aces and the value exceeds 21.
        """
        while self._value > 21 and self._aces:
            self._value -= 10
            self._aces -= 1

    def __str__(self) -> str:
        """
        Returns the string representation of the hand and its value.

        Returns:
            str: A comma-separated string of the cards in the hand and the total value.
        """
        return ", ".join(str(card) for card in self._cards) + f" (Value: {self._value})"

    @property
    def value(self) -> int:
        """
        Returns the total value of the hand.

        Returns:
            int: The total value of the hand.
        """
        return self._value
