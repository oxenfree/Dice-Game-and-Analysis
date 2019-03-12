from models import Streak, StreakWin
from data_io import read_in_all_files_as_one, write_out_game_data
from typing import Callable, List
from collections import OrderedDict

TEST_DIR = 'data/test'
DATA_FIXTURE = [
    {'mountain': 'Everest', 'height': '8848'},
    {'mountain': 'K2 ', 'height': '8611'},
    {'mountain': 'Kanchenjunga', 'height': '8586'}
]
FIELD_NAME_FIXTURE = ['mountain', 'height']


def print_passing(function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        func_name: str = function.__name__
        print(f'Starting: {func_name}')
        try:
            function(*args, **kwargs)
            print(f'{func_name} passed\n')
        except Exception as e:
            print('#' * 25)
            print(f'{func_name} failed')
            print('#' * 25)
            print(e)
            print('\n')

    return wrapper


@print_passing
def test_streak_and_win_logic() -> None:
    streaks: List[Streak] = []
    for i in range(0, 10):
        streak: Streak = Streak()
        win_1: StreakWin = StreakWin(1)
        win_2: StreakWin = StreakWin(1)
        win_3: StreakWin = StreakWin(8)
        streak.head_win: StreakWin = win_1
        win_1.next: StreakWin = win_2
        win_2.next: StreakWin = win_3
        streaks.append(streak)

    for streak in streaks:
        wins, last_win = streak.traverse_count()
        assert(wins == 3)
        assert(last_win.ante == 8)


@print_passing
def test_read_in_all_csv_files(directory) -> None:
    result_ordered_dict: OrderedDict = read_in_all_files_as_one(directory)
    assert result_ordered_dict


@print_passing
def test_write_out_data(data, field_names, directory) -> None:
    written_rows = write_out_game_data(data, field_names, directory)
    assert written_rows == 1


test_write_out_data(DATA_FIXTURE, FIELD_NAME_FIXTURE, TEST_DIR)
test_read_in_all_csv_files(TEST_DIR)
test_streak_and_win_logic()
