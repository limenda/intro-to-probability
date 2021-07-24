# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 21:50:03 2021

@author: limenda
"""

import random
from collections import Counter
from typing import List

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
    ''' The function returs number of heads for tossing a coin n times'''
    coin = ['H', 'T']
    tosses = [random.choice(coin) for _ in range(n)]
    result = Counter(tosses)
    return result['H']

def tossing(n: int) -> None:
    ''' just a helper function to print out the results of several experiments'''
    heads = coin_tosses(n)
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
    die = range(1, 7)
    return [random.choice(die) for _ in range(n)]
    
def de_mere_1(n: int) -> int:
    return sum([6 in rolls(4) for _ in range(n)])

def play_single_dice(n: int) -> None:
    six = de_mere_1(n)
    print(f'for {n} rolls six turns up {six} times or {100*six/n}%')

print("\nEx. 1.3")
print("\n1 dice:")
play_single_dice(1000)
play_single_dice(10000)

def rolls_2(n: int) -> bool:
    win = (6, 6)
    for _ in range(n):
        roll = (random.choice(range(1, 7)), random.choice(range(1, 7)))
        if (roll == win):
            return True
    return False

def de_mere_2(m: int, n: int) -> int:    
    return sum([rolls_2(m) for _ in range(n)])

def play_double_dice(m: int, n: int) -> None:
    six = de_mere_2(m, n)
    print(f'The probabilty a pair of sixes will occur in {m} rolls is {100*six/n}% for {n} tries')

print("\n2 dices:")

play_double_dice(24, 1125) # 27000
play_double_dice(25, 1080) # 27000
