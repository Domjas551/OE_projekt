import numpy as np

from Chromosom import Chromosom
from Genetic import Genetic


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



if __name__ == '__main__':
    g=Genetic(20,20,1,1,1)
    g.mutation(30,3)






