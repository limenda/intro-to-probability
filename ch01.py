# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 21:50:03 2021

@author: limenda
"""

import random
from collections import Counter
from typing import List
from typing import Tuple

from matplotlib import pyplot as plt

##########################################
#
# Example 1.1 (Random Number Generation)
#
##########################################

def random_numbers(n: int) -> List[float]:
    ''' The function generates n random real numbers in the interval [0, 1]'''
    return [random.random() for _ in range(n)]

print("/nEx. 1.1")
print(random_numbers(20))

##########################################
#
# Example 1.2 (Coin Tossing)
#
##########################################

def coin_tosses(n: int) -> List[str]:
    ''' The function returs the results of tossing a coin n times'''
    coin = ['H', 'T']
    tosses = [random.choice(coin) for _ in range(n)]    
    return tosses

def get_results(tosses: List[str]) -> Tuple[int, int]:
    ''' The function says how many heads and tails were in the game'''
    results = Counter(tosses)
    return results['H'], results['T']

def tossing(n: int) -> None:
    ''' just a helper function to print out the results of several experiments'''
    heads = get_results(coin_tosses(n))[0]
    print(f'tossing {n} times. Heads: {heads}/{n} = {heads/n}')
    
print("\nEx. 1.2")
tossing(20)
tossing(1000)
tossing(100000)

##########################################
#
# Example 1.3 (Dice Rolling)
#
##########################################

def rolls(n: int) -> List[int]:
    ''' The function rolls a die n times and returns the list of results.'''
    die = range(1, 7)
    return [random.choice(die) for _ in range(n)]
    
def de_mere_1(n: int) -> int:
    ''' The function returns the number of times a six turns up in four rolls of a die
    for n experiments.'''
    return sum([6 in rolls(4) for _ in range(n)])

def play_single_dice(n: int) -> None:
    ''' just a helper function to print out the results of several experiments'''
    six = de_mere_1(n)
    print(f'for {n} rolls six turns up {six} times or {100*six/n}%')

print("\nEx. 1.3")
print("\n1 dice:")
play_single_dice(1000)
play_single_dice(10000)

def rolls_2(n: int) -> bool:
    ''' The function rolls two dices and responds back if there was a pair of sixes
    at least once.'''
    win = (6, 6)
    for _ in range(n):
        roll = (random.choice(range(1, 7)), random.choice(range(1, 7)))
        if (roll == win):
            return True
    return False

def de_mere_2(m: int, n: int) -> int:
    ''' The function returns the number of times a pair of sixes turns up
    in m rolls of two dices for n experiments.'''
    return sum([rolls_2(m) for _ in range(n)])

def play_double_dice(m: int, n: int) -> None:
    ''' just a helper function to print out the results of several experiments'''
    six = de_mere_2(m, n)
    print(f'The probabilty a pair of sixes will occur in {m} rolls is {100*six/n}% for {n} tries')

print("\n2 dices:")

play_double_dice(24, 1125) # 27000
play_double_dice(25, 1080) # 27000

##########################################
#
# Example 1.3 (Heads or Tails)
#
##########################################

def get_history(results: List[str]) -> List[int]:
    ''' The function turns the plain results into the list of scores Peter got over the game at each toss.
        0 counts in favour to previous toss as per convention.'''
        
    # turns ['H', 'H', 'T' ... ] into [1, 1, -1, ...]
    results = [1 if result == 'H' else -1 for _, result in enumerate(results)]
    
    # figuring out when Peter was above 0:
    # turn ['1', '1', '-1' ... ] into [1, 2, 1, ...]
    for i in range(1, len(results)):
        results[i] += results[i-1]

    # setting zeroes as per convention:
    # turn [..., 1, 0, -1, ...] to [..., 1, 1, -1, ...]
    for i in range(1, len(results)):
        if results[i] == 0:
            results[i] = results[i-1] 

    return results

def plot_game(history: List[int]) -> None:
    ''' The function plots a game as per the score history.'''
    plt.title(f"Peter’s winnings in {len(history)} plays of heads or tails.")
    plt.plot(range(len(history)), history)    
    plt.show()

def HTSimulation(game: int, experiments: int):
    ''' The function runs the game (number of tosses in a single run)
    {experiments} number of times and returns the list of scores and
    the list of number of times being in the leads.'''
    
    wins = []
    leads = []
    for _ in range(experiments):
        tosses = coin_tosses(game)
        heads, tails = get_results(tosses)        
        wins.append(heads - tails)
        history = get_history(tosses)
        leads.append(sum(result > 0 for result in history))

    return Counter(wins), Counter(leads)

def Spikegraph(wins, leads):
    ''' the function draws the distributions of results'''
    plt.figure(1)
    plt.title("Distribution of winnings")
    plt.bar(wins.keys(), wins.values())

    plt.figure(2)
    plt.title("Distribution of number of times in the lead")
    plt.bar(leads.keys(), leads.values())

    plt.show()

game = 40
# Plot one game
history = get_history(coin_tosses(game))
plot_game(history)

# run the game multiple times
experiments = 10000
wins, leads = HTSimulation(game, experiments)
# Normalize results
wins = {k: v/experiments for k, v in wins.items()}
leads = {k: v/experiments for k, v in leads.items()}
Spikegraph(wins, leads)
