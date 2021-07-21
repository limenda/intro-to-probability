# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 21:50:03 2021

@author: limenda
"""

import random
from typing import List

##########################################
#
# Example 1.1 (Random Number Generation)
#
##########################################

def random_numbers(n: int) -> List[float]:
    ''' The function generates n random real numbers in the interval [0, 1]'''
    return [random.random() for _ in range(n)]

print(random_numbers(20))