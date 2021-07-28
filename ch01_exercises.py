# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 19:32:16 2021

@author: limenda
"""

import random

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