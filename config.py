NUMBER_OF_PLAYERS = 1
NUMBER_OF_DEALER_DICE = 3
NUMBER_OF_DICE_PER_PLAYER = 1
NUMBER_OF_HOURS = 1
ROUNDS_PER_HOUR = 240  # 60 is one round per minute
PLAYER_BANKROLL = 1000  # all players have the same bankroll for now
HOUSE_BANK = 1000
ANTE = 5
JACKPOT_MATCH_TOTAL = NUMBER_OF_DEALER_DICE
VERBOSE = True
JACKPOT_BONUS = 12
#  all paybacks are multiplited by ante
PAYBACK_SCHEDULE = {
    'zero': .25,
    'one': 1,
    'two': 4,
    'jackpot': JACKPOT_BONUS
}
