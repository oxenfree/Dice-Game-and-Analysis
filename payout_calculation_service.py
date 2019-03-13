import config

key_labels = ['zero', 'one', 'two', 'jackpot']
jackpot_bonus = config.JACKPOT_BONUS
ante = config.ANTE
payback_schedule = config.PAYBACK_SCHEDULE


def calculate_payout(number_winning_die: int) -> float:
    """
    Calculates payout. Duh.
    Parameters
    ----------
    number_winning_die: int
        Total number of matches a player has made with the dealer's hand.
    Returns
    ----------
        A payout according to a schedule set in configurations. Typically
        no matching die means the player gets a quarter back, one match
        means the player gets their ante back, two means the player doubled,
        and three has a jackpot of 10 to 50 multiples of the ante.
        Typical schedule (can be changed in config):
            If ante is 1; zero match = $.25, one match = 1, two matche = 2 \
                three matches = 10
            If ante is 5; zero match = $1, one match = 5, two match = 10 \
                three matches = 50
    """
    match_winning_key = key_labels[number_winning_die]
    payback = payback_schedule[match_winning_key] * ante

    return payback
