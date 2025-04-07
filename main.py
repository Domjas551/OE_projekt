import math
import random

import numpy as np

from Chromosom import Chromosom, Chromosom2
from Genetic import Genetic, Genetic2
from GeneticUI import GeneticUI


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



if __name__ == '__main__':
    """g=Genetic(20,20,-5.12,5.12,2)
    g.adapt(3,4,3,70,20,10)"""
    c=Chromosom2(1,-5.12,5.12)
    g2=Genetic2(10,1,-5.12,5.12,1)

    g2.adapt(1,1,2,70,20)
    a=[]
    a.append(c)








