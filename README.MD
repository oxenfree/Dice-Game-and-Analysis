# Dice Game and Data Analysis
## Game Play
A game where players try to beat a dealer's dice roll.
A player antes a bet. The dealer and each player rolls one or more dice.
If a player's die matches 1 of the dealers, they win their ante back.
If a player's die matches 2 of the dealers, they win double.
If they match three, they win a jackpot.
## Configurations
All of these values are configurable:
- Number of players
- Number of dice for each player
- Number of dice for dealer
- Ante amount (initial bet)
- Jackpot bonus
- Number of dice to match for a jackpot
- Hours of game play by these players
- Number of rounds per hour
- Verbose printing (True, False) to std out to see how the players did
## Data Analysis
Each player's bankroll is persisted for each round of play to a csv file. 
A jupyter notebook "data_analysis.ipynb" is the central analytic file. 
Adjusting configurations will show how that config alters gameplay. 
