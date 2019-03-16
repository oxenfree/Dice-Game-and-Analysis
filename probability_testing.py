from models import roll_die
import config

key_labels: list = ['zero', 'one', 'two', 'jackpot']
jackpot_bonus: int = config.JACKPOT_BONUS
ante: int = config.ANTE
payback_schedule: dict = config.PAYBACK_SCHEDULE
round_winnings: dict = {
    'zero': 0,
    'one': 0,
    'two': 0,
    'jackpot': 0
}
total_rounds: int = 100000

for _ in range(0, total_rounds):
    ante: int = ante
    hand_1: int = roll_die()
    hand_2: int = [roll_die() for idx in range(0, 3)]
    match_winning_key: int = key_labels[hand_2.count(hand_1)]
    payback: int = payback_schedule[match_winning_key] * ante
    round_winnings[match_winning_key] += payback

summation: int = 0
for k, v in round_winnings.items():
    summation += v
    print(f'{k}-match winnings: ${v} total')

print(f'Cumulative win: ${summation:,.2f}')
print(f'Out of: ${total_rounds * ante:,.2f} anted')