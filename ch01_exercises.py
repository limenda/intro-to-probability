# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 19:32:16 2021

@author: limenda
"""

import random

from collections import Counter
from typing import List
from typing import Tuple
import matplotlib.pyplot as plt


###    Exercise 1    ###

def CoinTosses_v1(n: int) -> None:
        
    heads = 0
    heads_proportion  = 0
    
    # let heads be 1, tails - 0.
    # since we are interested in heads only, we can just sum up 1's...
    for tosses in range(1, n+1):
        heads += random.randint(0, 1)
        if not tosses % 100:
            heads_proportion = heads/tosses
            print(f'{heads_proportion*100 :.4f}%:    {heads_proportion - 1/2 :.8f}    {heads - tosses/2 :.8f}')
    
    heads_proportion = heads/n
    print(f'{heads_proportion*100 :.4f}%:    {heads_proportion - 1/2 :.8f}    {heads - n/2 :.8f}')

print("\nExercise 1")
CoinTosses_v1(1000)    
#CoinTosses_v1(10000000) comment out this to speed up the execution

###    Exercise 2    ###

def CoinTosses_v2(n: int, low_bound: float = 0.1, high_bound: float = 0.5) -> bool:
    ''' The function tosses a coin {n} times and reports if the proportion of heads is between {low_bound} and {high_bound}.'''
    heads = 0
    
    for tosses in range(1, n+1):
        heads += random.randint(0, 1)
        
    return low_bound <= heads/n <= high_bound

print("\nExercise 2")
tosses = 100
experiments = 100
low_bound = 0.4
high_bound = 0.6
results = sum([CoinTosses_v2(tosses, low_bound, high_bound) for _ in range(experiments)])
print(f'{100*results/experiments}% heads are between {low_bound} and {high_bound} for {tosses} x {experiments}.')

###    Exercise 3    ###

def three_dice_roll() -> int:
    return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)

n = 100000
nines = 0
tens = 0
for _ in range(n):
    result = three_dice_roll()
    if result == 9:
        nines += 1
    elif result == 10:
        tens += 1
        
print("\nExercise 3")
print(f'the proportion of nines: {nines/n}')
print(f'the proportion of tens: {tens/n}')

###    Exercise 4    ###

win_points = 21

def win_volley(p: float = 0.5) -> bool:
    ''' The function takes the probability to win the volley and decides if a point is scored or not. '''
    return random.random() <= p

def player(s: int, p: float) -> int:
    ''' The function simulates how a player serves.
    It takes the scores player already has and the probability to win the volley.
    It returns the additional points player wins while serves.'''
    wins = 0
    for _ in range(win_points - s):
        if win_volley(p):
            wins += 1
        else:
            return wins
    return wins

def game() -> bool:
    ''' The function simulates game between two players. '''
    p1_scores = 0
    p2_scores = 0
    
    while p1_scores < win_points and p2_scores < win_points:
        p1_scores += player(p1_scores, 0.6)
        p2_scores += player(p2_scores, 0.5)
        
    return p1_scores == win_points

n = 1000
print("\nExercise 4")
wins = sum([game() for _  in range(n)])
print(f'The probability to win is {100*wins/n}%')

###    Exercise 5    ###

def triple_six(n: int) -> int:
    ''' The function simulates three dices rolling {n} times.
    Returns the 'happy' step, 0 otherwise.'''
    for m in range(1, n+1):
        if three_dice_roll() == 18: # 6 + 6 + 6
            return m
        
    return 0

def rolling(rolls: int, experiments: int) -> float:
    ''' The function runs rolling with {n} rolls {experiments} number of times.
    Returns the proportion of tries where triple six was found at least once.'''
    return sum([triple_six(rolls) != 0 for _ in range(experiments)])/experiments

print("\nExercise 5")
rolls = 100
experiments = 1000
sixth = rolling(rolls, experiments)
print(f"for {experiments} experiments per {rolls} rolls the probability of having three sixes is {100*sixth}%")
print("Let's try to figure out roughly the minimal number of rolls to have the probability at least 50%.")

while sixth < 0.5:
    rolls += 10 # some reasonable step for not making it run long
    sixth = rolling(rolls, experiments)
    
print(f"with {rolls} rolls the probability of having three sixes is {100*sixth}%")

###    Exercise 6    ###

def is_red() -> bool:
    ''' The function simulates spin the wheel, returns True if red slot, False otherwise. '''
    return random.random() <= 9/19 # reds are 18/38 slots. The probablity for single spin is actually the same

print("\nExercise 6")
spins = 1000
result = sum([1 if is_red() else -1 for _ in range(spins)])
print(f'{result}$ in {spins} spins.')

###    Exercise 7    ###

def is_17() -> bool:
    ''' The function simulates spin the wheel, returns True if 17, False otherwise. '''
    return random.random() <= 1/38

def turn_into_history(results: List[int]) -> List[int]:
    ''' This is a helper function. Transforms the list of win/loss on each step into the total sum of money.
    Needed to plot the history of spins properly. '''
    for i in range(1, len(results)):
        results[i] = results[i-1] + results[i]
    return results

print("\nExercise 7")

spins = 500
reds = [1 if is_red() else -1 for _ in range(spins)]
reds = turn_into_history(reds)
seventeens = [35 if is_17() else -1 for _ in range(spins)]
seventeens = turn_into_history(seventeens)
x = range(spins)
plt.plot(x, reds, 'r')
plt.plot(x, seventeens, 'b')
plt.show()

###    Exercise 8    ###

def toss() -> int:
    return random.choice([-1, 1])

def coin_tosses(n: int) -> List[int]:
    ''' The function returs the results of tossing a coin n times.
    Head: 1, Tail: -1''' 
    return [toss() for _ in range(n)]    

def check_intuition(game: int, experiments: int) -> Tuple[float, float]:
    ''' The function simulates coins tosses: {experiments} sets per {game} tosses in set.
    Returns the proportion of player ends up 0 and proportion of being player in lead'''
    always_lead = 0
    endup_zero = 0
    
    for _ in range(experiments):
        results = coin_tosses(game)
        
        # turn the results of single  tosses into list of total amount at each step
        for i in range(1, len(results)):
            results[i] += results[i-1]
        endup_zero += (results[-1] == 0) # if round ends up with 0
        
        # count 0 results in favour of previous step for better definition of lead
        for i in range(1, len(results)):
            if results[i] == 0:
                results[i] = results[i-1]
        always_lead += all(i >= 0 for i in results) # check if player was always in leads during the round
        
    return endup_zero/experiments, always_lead/experiments

experiments = 1000
n = 2

print("\nExercise 8")
zeroes, leads = check_intuition(n, experiments)
print(f'\nfor {n} tosses:')
print(f'Player ended up 0: {100*zeroes}% of time,\nwas always in leads: {100* leads}% of time.')

experiments = 1000
n = 4

zeroes, leads = check_intuition(n, experiments)
print(f'\nfor {n} tosses:')
print(f'Player ended up 0: {100*zeroes}% of time,\nwas always in leads: {100* leads}% of time.')

###    Exercise 9    ###

def labouchere(digits: List[int]) -> None:
    ''' Implements the Labouchere system as described in the book. 
    Takes the list of numbers. '''
    win = 0
    iterations = 0
    
    while len(digits):
        if len(digits) > 1:
            beat = digits[0] + digits[-1]
        else:
            beat = digits[0]
            
        if is_red():
            win += beat
            digits.pop(0)
            if len(digits):
                digits.pop(-1)
        else:
            win -= beat
            digits.append(beat)
        
        iterations += 1
        print(f'Iteration {iterations}: List: {digits}, score: {win}.')
        
        if iterations >= 5000: # to prevent the infinite loop
            break

print("\nExercise 9")
digits = [1, 2, 3, 4]
labouchere(digits)

###    Exercise 10   ###

def martingale():
    ''' Implements the martingale doubling system as described in the book'''
    scores = 0
    bet = 1
    iterations = 0
    
    while -100 <= scores <= 5:
        if is_red():
            scores += bet
            bet = 1
        else:
            scores -= bet
            bet *= 2
        
        iterations += 1
        # print(f'Iteration: {iterations}: bet {bet} next time') comment out to get the history
        
        if iterations >= 5000: # to prevent the infinite loop
            break
    
    print(f'Scored {scores} in {iterations} iterations')
    
print("\nExercise 10")
martingale()

n = 10
print("just out of curiosity - let's try to repeat the method {n} times")
for _ in range(n):
    martingale()
    
###    Exercise 11   ###

def HTSimulation(tosses: int, experiments: int) -> None:
    ''' The function counts the probabilities of even max winning
    running the given number of experimnets with the known number of tosses in one experiment.'''
    even_wins = []
    
    for _ in range(experiments):
        wins = [0] # for total loose, e.g. [-1, -1] the max number should be 0 - what player had _before_ the game
        wins.extend(coin_tosses(tosses)) # collecting all the other results
        # turn the results of single  tosses into list of total amount at each step
        for i in range(1, len(wins)):
            wins[i] += wins[i-1]   
            
        max_win = max(wins)        
        if not max_win % 2: # we are intested only in even max achievments
            even_wins.append(max_win)

    even_wins = Counter(even_wins)
    print("The proportions are:")
    for k, v in even_wins.items():
        print(f"{k}: {v/experiments}")
        
    # let's also plot the results for better trend visibility
    even_wins = {k: v/experiments for k, v in even_wins.items()}
    plt.bar(even_wins.keys(), even_wins.values())
    plt.show()

print("\nExercise 11")
tosses = 40
experiments = 10000
HTSimulation(tosses, experiments)

tosses = 2
experiments = 1000
even_wins = HTSimulation(tosses, experiments)

tosses = 4
experiments = 1000
even_wins = HTSimulation(tosses, experiments)
    
###    Exercise 12   ###

def vote_for_rep(chance: float) -> bool:
    ''' The function simulates a single vote. Takes a chance to vote for Republicans.
    Returns True if voted for Republicans, otherwise False.'''
    return random.random() <= chance

def sample(n: int, chance: float) -> Tuple[int, int]:
    ''' The function simulates sample of {n} votes with {chance} probability voting for Republicans.'''
    republicans = 0
    democrates = 0
    for _ in range(n):
        if vote_for_rep(chance):
            republicans += 1
        else:
            democrates += 1
            
    return republicans, democrates

def check_plan(n: int, experiments: int, chance: float) -> None:
    ''' The function validates a poster plan.
    It helps us to understand if the result we got from the first sample in {n} votes with {chance} probability to win for Democracies is consistent.
    Fot that we take {experiments} smaples, pre {n} votes each and check if the prediction stays the same.'''
    
    candidates = ("Republicans", "Democrates")
    republicans, democrates = sample(n, chance)
    winner = candidates[democrates > republicans] # trick to print the winner name correctly
    republicans_votes = 0
    democrates_votes = 0
    
    print(f'The sample is {n}, Republicans chance to win is {chance}:')
    print(f'\t{100*republicans/n}% voting for Republicans')
    print(f'\t{100*democrates/n}% voting for Democrates')
    print(f'\t{winner} should win')
    print(f'\nNow try to run same prediction {experiments} times:')
        
    for _ in range(experiments):
        republicans, democrates = sample(n, chance)
        if republicans > democrates:
            republicans_votes += 1
        else:
            democrates_votes += 1
            
    print(f"\tin {100*republicans_votes/experiments}% cases should win Republicans")
    print(f"\tin {100*democrates_votes/experiments}% cases should win Democrates\n")
    
n = 1000
experiments = 100
chance = 0.48
print("\nExercise 12")
check_plan(n, experiments, chance)

n = 1000
experiments = 100
chance = 0.49
check_plan(n, experiments, chance)

n = 3000
experiments = 100
chance = 0.49
check_plan(n, experiments, chance)

###    Exercise 13   ###

def is_boy() -> bool:
    ''' The function randomly reports if newborn was a boy.'''
    return random.random() <= 0.5

def born_per_day(n: int) -> int:
    ''' The function generates {n} babies.'''
    return sum([is_boy() for _ in range(n)])

def born_per_year(days: int, babies: int) -> int:
    ''' The function returns how many days where over 60% of boys were born.
    It takes number of days to consider. And number of babies expect to be born in a day.'''
    boy_days = [born_per_day(babies) for _ in range(days)]            
    return sum([boys/babies > 0.6 for boys in boy_days])
    
babies = 45
days = 365
print("\nExercise 13")
boy_days = born_per_year(days, babies)
print(f"Large hospital: ({babies} babies in a day).\n\t{boy_days} days, where over 60% of boys were born")


babies = 15
days = 365
boy_days = born_per_year(days, babies)
print(f"Small hospital: ({babies} babies in a day).\n\t{boy_days} days, where over 60% of boys were born")

###    Exercise 14   ###

def j_wins():
    ''' The function simulates the coin tossing until heads come up.
    Returns the step when that occurs.'''
    side = -1 # tail
    step = 0
    
    while side != 1:
        step += 1
        side = toss()
        
    return step
    
print("\nExercise 14")
plays = 1000
steps = []
for _ in range(plays):
    steps.append(j_wins())
    
steps = Counter(steps)

plt.bar(steps.keys(), steps.values())
plt.show()

print(f'in {plays} games you would win:')
for key, value in steps.items():
    print(f'\t{2**key}$: in {100*value/plays}% of cases.')
    
###    Exercise 15   ###

def is_hit():
    ''' The function randomly reports is there was a hit with the fifty-fifty chance'''
    return random.random() <= 0.5

def basketball_player(n: int) -> List[bool]:
    ''' The function returns the shots history for single player. 
    n: is the number of shots in the game.'''
    return [is_hit() for _ in range(n)]

def five_in_a_row(shots: List[bool]) -> bool:
    ''' The function takes the shots history and reports back if there was a streak of five.'''
    five_hits = 0
    for shot in shots:
        if shot:
            five_hits += 1
            if five_hits >= 5:
                return True
        else:
            five_hits = 0
            
    return False

games = 1000
hits = 20
five = 0

for _ in range(games):
    shots = basketball_player(hits)
    five += five_in_a_row(shots)
    
print("\nExercise 15")
print(f'The probability to have a streak of five is {100*five/games}%.')

###    Exercise 16   ###

def born_till_boy() -> int:
    ''' The function reports how many children might be born unless first boy comes.'''
    babies = 1
    while not is_boy():
        babies += 1
    return babies

def born_till() -> int:
    ''' The function reports how many children might be born unless boy and girl come.'''
    boy = 0
    girl = 0
    
    while not (boy & girl):
        if is_boy():
            boy +=1
        else:
            girl += 1
    
    return boy + girl

families = 100000

print("\nExercise 16")
babies = sum([born_till_boy() for _ in range(families)])
print(f'{babies} babies in {families} families expected to born while waiting for first boy.')
babies = sum([born_till() for _ in range(families)])
print(f'{babies} babies in {families} families expected to born while waiting for boy&girl.')

###    Exercise 16   ###

def next_1D_step() -> int:
    ''' The function decides next step from two possible directions.'''
    return random.choice([-1, 1])

def line_walk():
    ''' The function simulates the walk in two directions.
    Returns the number of steps need to return to the start point.'''
    walk = 1
    step = next_1D_step()
    while step:
        walk += 1
        step += next_1D_step()
        
        if step >= 10000: # to avoid infinite loop
            break;
            
    return walk

print("\nExercise 17")
walks = 100
steps = [line_walk() for _ in range(walks)]
plt.title('Case A: Line walk.')
plt.plot(range(walks), steps)
plt.show()

def next_2D_step() -> Tuple[int, int]:
    ''' The function decides next step from four possible directions.'''
    return random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])

def walk_2D() -> int:
    ''' The function simulates the walk in four directions.
    Returns the number of steps need to return to the start point.'''
    walk = 1
    position = next_2D_step()
    while position != (0, 0):
        walk += 1
        next_pos = next_2D_step()
        position = tuple(sum(x) for x in zip(position, next_pos)) # element-wise addition
        
        if walk >= 10000: # to avoid infinite loop
            break;
            
    return walk

steps = [walk_2D() for _ in range(walks)]
plt.title('Case B: 2D walk.')
plt.plot(range(walks), steps)
plt.show()

def next_3D_step() -> Tuple[int, int, int]:
    ''' The function decides next step from eight possible directions.'''
    return random.choice([(0, 0, 1), (0, 1, 0), (1, 0, 0),
                          (0, 0, -1), (0, -1, 0), (-1, 0, 0)])

def walk_3D(limit: int) -> int:
    ''' The function simulates the walk in eight directions.
    Takes the limit of steps possible - to avoid infinite walk.
    Returns the number of steps need to return to the start point.'''
    walk = 1
    position = next_3D_step()
    while position != (0, 0, 0):
        walk += 1
        next_pos = next_3D_step()
        position = tuple(sum(x) for x in zip(position, next_pos)) # element-wise addition
        
        if walk >= limit: # to avoid infinite loop
            break;
            
    return walk

limit = 1000000
steps = walk_3D(limit)
print(f"Case C: trying to complete the walk in {limit} steps. Actually taken: {steps}.")
