import numpy as np

class Chromosom:
    def __init__(self,number_of_bits,random=True):
        self.number_of_bits=number_of_bits
        self.chromosom_value=[]

        if random:
            self.chromosom_value=np.random.randint(2,size=self.number_of_bits)

        def set_chromosom(self,chromosom_value):
            self.chromosom_value=chromosom_value