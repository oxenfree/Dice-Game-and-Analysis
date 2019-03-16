import csv
import os
import os.path
from typing import List, Dict
from datetime import datetime as dt
import config
from main import Dealer

current_dir: str = os.getcwd()
defaullt_dir: str = os.path.join(current_dir, 'data')


def get_file_names(data_dir=None) -> List:
    """
    Reads all file_names from a given directory.
    Parameters
    ----------
    data_dir: str
        The directory to read. Default is 'data' in present working directory.
    Returns
    -------
    list of file_names
        Each csv is its own name in the list.
    """
    if data_dir is None:
        data_dir = defaullt_dir
    return [
        name for name in os.listdir(data_dir)
        if os.path.isfile(os.path.join(data_dir, name))
    ]


def read_in_each_file_as_one(file_name: str, data_dir=None) -> List:
    """
    Reads all csv's from a given directory.
    Parameters
    ----------
    directory: str
        The directory to read. Default is 'data' in present working directory.
    Returns
    -------
    list of OrderedDictionaries
        Each csv is its own list entry. Each ordered dict is the csv data.
    """
    if data_dir is None:
        data_dir = defaullt_dir
    result: List[Dict] = []
    with open(os.path.join(data_dir, file_name), newline='') as csv_file:
        reader: csv.DictReader = csv.DictReader(csv_file)
        for row in reader:
            result.append(row)

    return result


def write_out_game_data(
            data: List[Dict],
            field_names: List,
            folder='data'
        ) -> int:
    """
    Writes out csv's from a list of dictionaries.
    Parameters
    ----------
    data: list of dictionaries
        Each dict is a row in the csv with columns matching the fields names.
        Fields names should match the dictionary keys.
    field_names: list of str
        Field names should match dict keys. These become columns in the csv.
    folder: str
        The directory to write out. Default is 'data' in pwd.
    Returns
    -------
    int
        Number of csvs written out. The return is for error checking.
        1 or more (should be 1 though) for it worked.
        0 for it did not work.
    """
    now = dt.now()
    right_now: str = f'{now.minute}{now.second}_config_ante_{config.ANTE}'
    data_dir: str = os.path.join(current_dir, folder)
    file_name = os.path.join(data_dir, f'{right_now}.csv')

    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    counter = 0
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)
        counter += 1

    csv_file.close()

    return counter


def verbose_print(players: List, dealer: Dealer) -> None:
    """
    Specialized print function for dealer and player totals.
    Parameters
    ----------
    players: list of Player
        All players in the game.
    dealer: Dealer
        The dealer in the game.
    Returns
    -------
    None
        Not buffered in any way. If there's an error it will write to stdout.
    """
    print('\n')
    print('#' * 30)
    print(f'{config.NUMBER_OF_HOURS * config.ROUNDS_PER_HOUR}\
         rounds played in {config.NUMBER_OF_HOURS} hours')
    print(f'House winnings: ${dealer.house_bank - config.HOUSE_BANK}')
    print('#' * 30)
    print('\n')
    for idx, player in enumerate(players):
        idx += 1
        longest_streak: int = 0
        for streak in player.streaks:
            streak_count, _ = streak.traverse_count()
            if streak_count > longest_streak:
                longest_streak = streak_count
        print(f'Player {idx} bankroll: ${player.bankroll}')
        print(f'Player {idx} hit the jackpot: {player.jackpots_won} times.')
        print(f"Player {idx} won regular hands:"
              f"{player.regular_hands_won} times.")
        print(f'Player {idx} lost: {player.hands_lost} times.')
        print(f'Player {idx} went to the atm: {player.had_to_use_atm} times.')
        print(f'Player {idx} longest streak: {longest_streak}')
        print('\n')
