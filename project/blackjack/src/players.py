from typing import Optional
from project.blackjack.src.strategies import CountingStrategy, Strategy
from project.blackjack.src.objects import Card, Hand


class Player:
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

    def place_bet(self, amount: int) -> None:
        """
        Places a bet for the player, subtracting the amount from their chips.

        Args:
            amount (int): The amount to bet.
        """
        amount = min(amount, self.chips)
        self._bet = amount

    def win_bet(self, multiplier: int = 1) -> None:
        """
        Awards the player with a win multiplier on their bet.

        Args:
            multiplier (int): The multiplier for the bet. Defaults to 2.
        """
        self.chips += self._bet * multiplier
        self._bet = 0

    def lose_bet(self) -> None:
        """
        Resets the player's bet after a loss.
        """
        self.chips -= self._bet
        self._bet = 0

    def push_bet(self) -> None:
        """
        Returns the player's bet after a tie.
        """
        self._bet = 0

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
        _counting_strategy (Optional[CountingStrategy]): The counting strategy, if applicable.
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
        self._counting_strategy: Optional[CountingStrategy] = (
            strategy if isinstance(strategy, CountingStrategy) else None
        )

    def decide_hit(self) -> bool:
        """
        Decides whether to hit based on the bot's strategy.

        Returns:
            bool: Decision to hit.
        """
        return self._strategy.decide_hit(self.hand)

    def update_count(self, card: Card) -> None:
        """
        Updates the card count if using a counting strategy.

        Args:
            card (Card): The card to update the count with.
        """
        if self._counting_strategy:
            self._counting_strategy.update_count(card)


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

    def __str__(self) -> str:
        """
        Returns the string representation of the dealer's hand, with one card hidden.

        Returns:
            str: A string describing the dealer.
        """
        return f"Dealer: {self.hand._cards[0]}, Hidden"
