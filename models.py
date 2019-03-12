import random
import config
from typing import List


def roll_die() -> int:
    return random.randint(1, 6)


class StreakWin:
    def __init__(self, ante: int):
        self.ante: int = ante
        self.next: StreakWin = None


class Streak:
    def __init__(self) -> None:
        self.head_win: StreakWin = None

    def traverse_count(self):
        count: int = 0
        if self.head_win is not None:
            count += 1
        current_win: StreakWin = self.head_win
        while current_win.next is not None:
            count += 1
            current_win = current_win.next

        return count, current_win


class Player:
    def __init__(
        self, bankroll=config.PLAYER_BANKROLL, 
        number_of_dice=config.NUMBER_OF_DICE_PER_PLAYER
    ) -> None:
        self.bankroll: int = bankroll
        self.number_of_dice: int = number_of_dice
        self.jackpots_won: int = 0
        self.had_to_use_atm: int = 0
        self.regular_hands_won: int = 0
        self.hands_lost: int = 0
        self.hands_pushed: int = 0
        self.streaks: List[Streak] = []
        self.start_new_streak: bool = True

    def roll_hand(self) -> List:
        hand: List[int] = []
        for die in range(0, self.number_of_dice):
            hand.append(roll_die())

        return hand

    def ante(self, ante=config.ANTE) -> int:
        self.bankroll -= ante

        return ante

    def gather_winnings(self, number_of_matches: int, ante=config.ANTE) -> int:
        total_payout: int = number_of_matches * ante

        if number_of_matches > 0:
            self.bankroll += total_payout
            self.regular_hands_won += 1
            streak_win: StreakWin = StreakWin(total_payout)

            # If there are streaks already and start a new streak is false.
            if len(self.streaks) and self.start_new_streak is False:
                # get the last streak and add to it
                streak: Streak = self.streaks[-1] 
                _, last_win = streak.traverse_count()
                last_win.next = streak_win

            # If start a new streak is True, we start one. 
            # Previous streak is overwritten.
            if self.start_new_streak:
                streak: Streak = Streak()
                streak.head_win: StreakWin = streak_win
                self.streaks.append(streak)

            # If player won, this is the streak. Don't start a new one.
            self.start_new_streak = False

        return total_payout

    def won_jackpot(self, jackpot_bonus=config.JACKPOT_BONUS) -> int:
        self.bankroll += jackpot_bonus
        self.jackpots_won += 1

        return jackpot_bonus

    def evaluate_bankroll(self) -> None:
        # Player only evaluates bankroll after losing. We start a new streak.
        self.start_new_streak = True
        if self.bankroll <= 0:
            self.bankroll = config.PLAYER_BANKROLL
            self.had_to_use_atm += 1


class Dealer:
    def __init__(
        self, house_bank=config.HOUSE_BANK,
        number_of_dice=config.NUMBER_OF_DEALER_DICE
     ) -> None:
        self.house_bank: int = house_bank
        self.number_of_dice: int = number_of_dice

    def gather_ante(self, ante: int) -> None:
        self.house_bank += ante

    def payout_winner(self, payout: int) -> None:
        self.house_bank -= payout

    def roll_hand(self) -> List:
        hand: List[int] = []
        for die in range(0, self.number_of_dice):
            hand.append(roll_die())

        return hand

    def evaluate_player_hand(self, dealer_hand: List, player_hand: List) -> int:
        won: int = 0
        for die in player_hand:
            won += dealer_hand.count(die)

        return won
