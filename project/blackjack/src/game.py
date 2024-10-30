import random
from typing import List
from project.blackjack.src.objects import Deck, Hand
from project.blackjack.src.players import BotPlayer, Dealer


class Game:
    """
    Represents a game of blackjack with multiple players and a dealer.

    Attributes:
        _deck (Deck): The deck of cards used in the game.
        _players (List[Player]): A list of Player objects representing the players in the game.
        _dealer (Dealer): The dealer of the game.
        _round (int): The current round number.
        _max_rounds (int): The maximum number of rounds to be played in the game.
    """

    def __init__(self, players: List[BotPlayer], max_rounds: int = 100) -> None:
        """
        Initializes the Game with a deck, players, and a dealer.

        Args:
            players (List[Player]): A list of Player objects participating in the game.
            max_rounds (int): The maximum number of rounds to play. Defaults to 100.
        """
        self._deck: Deck = Deck()
        self._players: List[BotPlayer] = players
        self._dealer: Dealer = Dealer()
        self._round: int = 0
        self._max_rounds: int = max_rounds

    def take_bets(self) -> None:
        """
        Allows each player to place a bet. Players with no chips are skipped.
        """
        for player in self._players:
            if player.chips <= 0:
                continue
            bet = random.randint(1, min(100, player.chips))
            player.place_bet(bet)
            print(f"{player.name} bets {bet} chips.")

    def deal_initial_cards(self) -> None:
        """
        Deals two cards to each player and the dealer, with one card hidden for the dealer.
        """
        for player in self._players:
            player.hand = Hand()
            player.hand.add_card(self._deck.deal_card())
            player.hand.add_card(self._deck.deal_card())
            player.update_count(player.hand._cards[-2])
            player.update_count(player.hand._cards[-1])
            print(f"{player}")

        self._dealer.hand = Hand()
        self._dealer.hand.add_card(self._deck.deal_card())
        self._dealer._hidden_card = self._deck.deal_card()
        print(f"{self._dealer}")

    def player_turns(self) -> None:
        """
        Executes each player's turn, allowing them to hit or stand based on their strategy.
        """
        for player in self._players:
            if player.chips <= 0:
                continue
            print(f"\n{player.name}'s turn:")
            while True:
                decision = player.decide_hit()
                if decision:
                    card = self._deck.deal_card()
                    player.hand.add_card(card)
                    print(
                        f"{player.name} hits and receives {card}. Hand: {player.hand}"
                    )
                    player.update_count(card)
                    if player.hand.value > 21:
                        print(f"{player.name} busts!")
                        break
                else:
                    print(f"{player.name} stands with {player.hand.value} points.")
                    break

    def dealer_turn(self) -> None:
        """
        Executes the dealer's turn, revealing the hidden card and continuing to hit until the dealer's hand value reaches 17 or higher.
        """
        print("Dealer's turn:")
        if self._dealer._hidden_card:
            self._dealer.hand.add_card(self._dealer._hidden_card)
            print(
                f"Dealer reveals hidden card: {self._dealer._hidden_card}. Hand: {self._dealer.hand}"
            )
        while self._dealer.hand.value < 17:
            card = self._deck.deal_card()
            self._dealer.hand.add_card(card)
            print(f"Dealer hits and receives {card}. Hand: {self._dealer.hand}")
            if self._dealer.hand.value > 21:
                print("Dealer busts!")
                break
        if 17 <= self._dealer.hand.value <= 21:
            print(f"Dealer stands with {self._dealer.hand.value} points.\n")

    def settle_bets(self) -> None:
        """
        Settles all bets at the end of the round, comparing each player's hand with the dealer's hand.
        """
        dealer_value = self._dealer.hand.value
        for player in self._players:
            if player.chips <= 0 and player._bet == 0:
                continue
            player_value = player.hand.value
            if player_value > 21:
                print(f"{player.name} loses their bet of {player._bet} chips.")
                player.lose_bet()
            elif dealer_value > 21:
                print(f"{player.name} wins! Receives {player._bet} chips.")
                player.win_bet()
            elif player_value > dealer_value:
                print(f"{player.name} wins! Receives {player._bet} chips.")
                player.win_bet()
            elif player_value < dealer_value:
                print(f"{player.name} loses their bet of {player._bet} chips.")
                player.lose_bet()
            else:
                print(f"{player.name} pushes. Bet of {player._bet} chips returned.")
                player.push_bet()

    def show_game_state(self) -> None:
        """
        Displays the current game state, including each player's chips and hand, as well as the dealer's hand.
        """
        print("\n--- Current Game State ---")
        for player in self._players:
            print(player)
        print(self._dealer)
        print("--------------------------\n")

    def liquidate_broke_players(self) -> None:
        """
        Removes players who have run out of chips from the game.
        """
        self._players = [player for player in self._players if player.chips > 0]

    def play_round(self) -> None:
        """
        Plays a single round of the game, including taking bets, dealing initial cards, executing player and dealer turns, and settling bets.
        """
        self.take_bets()
        self.deal_initial_cards()
        self.player_turns()
        self.show_game_state()
        self.dealer_turn()
        self.settle_bets()
        self.liquidate_broke_players()
        self._round += 1

    def play_game(self) -> None:
        """
        Plays the entire game up to the maximum number of rounds or until all players are out of chips.
        """
        while self._round < self._max_rounds and len(self._players) > 0:
            print(f"\n=== Round {self._round} ===")
            self.play_round()
        print("\n=== Game Over ===")
        for player in self._players:
            print(f"{player.name} has {player.chips} chips.")
