# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 19:32:16 2021

@author: limenda
"""

import random

from typing import Callable
from typing import List
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
    return random.random() <= 9/19 # reds are 18/38 slots. The probablity for single spin is actually the same

def spin_the_wheel(spins: int, bet: Callable[[], bool]) -> List[int]:
    return [1 if bet() else -1 for _ in range(spins)]

print("\nExercise 6")
spins = 1000
result = sum(spin_the_wheel(spins, is_red))
print(f'{result}$ in {spins} spins.')

###    Exercise 7    ###

def is_17() -> bool:
    return random.random() <= 1/38

def history(results: List[int]) -> List[int]:
    for i in range(1, len(results)):
        results[i] = results[i-1] + results[i]
    return results

print("\nExercise 7")

spins = 500
reds = spin_the_wheel(spins, is_red)
seventeens = spin_the_wheel(spins, is_17)
x = range(spins)
plt.plot(x, reds, 'r')
#plt.plot(x, seventeens, 'b')
plt.show()