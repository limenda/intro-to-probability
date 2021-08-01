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

def coin_tosses(n: int) -> List[int]:
    ''' The function returs the results of tossing a coin n times.
    Head: 1, Tail: -1''' 
    return [random.choice([-1, 1]) for _ in range(n)]    

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
