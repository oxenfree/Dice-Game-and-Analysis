import config
from typing import List, Dict
import data_io
from models import Dealer, Player
import payout_calculation_service


def start_session() -> dict:
    """
    Creates all the participants at the table.
    Parameters
    ----------
    None
    Returns
    ----------
    dictionary with a dealer and the players.
        Total player number is determined by config file.
    """
    dealer: Dealer = Dealer()
    players: List[Player] = []
    for i in range(0, config.NUMBER_OF_PLAYERS):
        players.append(Player())

    return {'dealer': dealer, 'players': players}


def play_round(dealer: Dealer, players: List, current_round: int) -> Dict:
    """
    Plays a round of hands.
    Parameters
    ----------
    dealer: Dealer
        The Dealer object which rolls its own hand, evaluates player hands,
            and collects antes and delivers payouts.
    players: List of Player
        The Player objects. Roll their own hands. Chip their own antes.
            If they run out of money they go to the atm.
            The number of players is determined in the config file.
    current_round: int
        Counter for how many rounds have been played.
    Returns
    -------
    Dict
    """
    round_data = {'round': current_round}
    dealer_hand: List[int] = dealer.roll_hand()
    for idx, player in enumerate(players):
        ante: int = player.ante()
        dealer.gather_ante(ante)
        player_hand: List[int] = player.roll_hand()
        winning_die_count: int = dealer.evaluate_player_hand(
            dealer_hand,
            player_hand
        )
        payout = payout_calculation_service.calculate_payout(winning_die_count)
        dealer.payout_winner(player.gather_winnings(payout))

        if winning_die_count == 0:
            player.evaluate_bankroll()
        if winning_die_count == config.JACKPOT_MATCH_TOTAL:
            player.won_jackpot(payout)
        round_data.update({f'player {idx} bankroll': player.bankroll})
        round_data.update({f'house {idx} bank': dealer.house_bank})

    return round_data


if __name__ == '__main__':
    table: dict = start_session()
    dealer: Dealer = table['dealer']
    players: List[Player] = table['players']
    number_of_rounds: int = config.NUMBER_OF_HOURS * config.ROUNDS_PER_HOUR
    current_round: int = 0
    write_out_data = []

    while current_round <= number_of_rounds:
        current_round += 1
        write_out_data.append(play_round(dealer, players, current_round))

    data_io.write_out_game_data(write_out_data, write_out_data[0].keys())
    if config.VERBOSE:
        data_io.verbose_print(players, dealer)
