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
    g2=Genetic2(20,1,-5.12,5.12,1)

    """
    fl=g2.przelicz(g2.population)
        print(fl)
        print(g2.przelicz(g2.selection_roullete(10,fl)))
    """
    print(g2.population[0].chromosom_values)
    print(g2.population[1].chromosom_values)
    a=g2.crossing(g2.population[0],g2.population[1],100,4)
    print(a[0].chromosom_values)










