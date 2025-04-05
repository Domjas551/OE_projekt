import numpy as np
import random

class Chromosom:
    def __init__(self,number_of_bits,random=True):
        self.number_of_bits=number_of_bits
        self.chromosom_value=[]

        if random:
            self.chromosom_value=np.random.randint(2,size=self.number_of_bits)

    def set_chromosom(self,chromosom_value):
        self.chromosom_value=chromosom_value

class Chromosom2:
    def __init__(self,number_of_values,min,max,accuracy=2,rnd=True):
        self.chromosom_values=[]

        if rnd:
            for i in range(0,number_of_values,1):
                self.chromosom_values.append(round(random.uniform(min,max),accuracy))

    def set_chromosom(self,chromosom_value,index=0):

        if index>len(self.chromosom_values):
            print("Podany indeks jest poza zakresem")
        else:
            self.chromosom_values[index]=chromosom_value