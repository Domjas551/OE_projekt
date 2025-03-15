from Chromosom import Chromosom
import numpy as np

class Genetic:
    def __init__(self, population_size, chromosom_size, lower_border, upper_border,epochs):
        self.population_size=population_size
        self.chromosom_size=chromosom_size
        self.lower_border=lower_border
        self.upper_border=upper_border
        self.epochs=epochs
        self.population=[]

        for i in range(0,population_size):
            self.population.append(Chromosom(self.chromosom_size))

    def decode_specimen(self,specimen):
        return (self.lower_border+
                int(''.join(map(str,specimen.chromosom_value)),2)*
                (self.upper_border-self.lower_border)/
                (pow(2,self.chromosom_size)-1))

    def fitness_function(self):
        pass

    def select_best(self, amount):

        best_ind=[]

        for j in range(0, amount):
            x = 100
            ind = 0
            for i in range(0, len(a)):
                if i not in best_ind:
                    if abs(a[i]) < x:
                        x = a[i]
                        ind = i
            best_ind.append(ind)
        return best_ind

#TODO zapis nowej populacji
    def crossing(self,specimen1,specimen2,chance,type=1):

        """
        Type:
        1 - krzyżowanie jednopuktowe
        2 - krzyżowanie dwupunktowe
        3 - krzyżowanie jednorodne
        4 - krzyżowanie ziarniste - W JEGO WYNIKU TWORZONY JEST JEDEN OSOBNIK
        """

        alfa=np.random.randint(0, 100)

        if alfa<=chance:
            c1 = []
            c2 = []

            if type==1:
                cut_point=np.random.randint(0, self.chromosom_size)

                c1.extend(specimen1.chromosom_value[:cut_point])
                c1.extend(specimen2.chromosom_value[cut_point:])
                c2.extend(specimen2.chromosom_value[:cut_point])
                c2.extend(specimen1.chromosom_value[cut_point:])

            elif type==2:

                cut_point1 = 0
                cut_point2 = 0

                while cut_point1==cut_point2 or abs(cut_point1-cut_point2)==1:
                    cut_point1 = np.random.randint(0, self.chromosom_size)
                    cut_point2 = np.random.randint(0, self.chromosom_size)

                if cut_point1<cut_point2:
                    c1.extend(specimen1.chromosom_value[:cut_point1])
                    c1.extend(specimen2.chromosom_value[cut_point1:cut_point2])
                    c1.extend(specimen1.chromosom_value[cut_point2:])
                    c2.extend(specimen2.chromosom_value[:cut_point1])
                    c2.extend(specimen1.chromosom_value[cut_point1:cut_point2])
                    c2.extend(specimen2.chromosom_value[cut_point2:])
                else:
                    c1.extend(specimen1.chromosom_value[:cut_point2])
                    c1.extend(specimen2.chromosom_value[cut_point2:cut_point1])
                    c1.extend(specimen1.chromosom_value[cut_point1:])
                    c2.extend(specimen2.chromosom_value[:cut_point2])
                    c2.extend(specimen1.chromosom_value[cut_point2:cut_point1])
                    c2.extend(specimen2.chromosom_value[cut_point1:])

            elif type == 3:

                for i in range(0,self.chromosom_size):
                    alfa = np.random.randint(0, 100)

                    if alfa<50:
                        c1.append(specimen2.chromosom_value[i])
                        c2.append(specimen1.chromosom_value[i])
                    else:
                        c1.append(specimen1.chromosom_value[i])
                        c2.append(specimen2.chromosom_value[i])

            else:

                for i in range(0,self.chromosom_size):
                    alfa = np.random.randint(0, 100)

                    if alfa<50:
                        c1.append(specimen1.chromosom_value[i])
                    else:
                        c1.append(specimen2.chromosom_value[i])

    # TODO zapis nowej populacji
    def mutation(self,chance,type=1):

        """
        Type:
        1 - mutacja brzegowa
        2 - mutacja jednopunktowa
        3 - mutacja dwupunktowa
        """

        for i in range(0,self.population_size):
            alfa = np.random.randint(0, 100)

            if alfa <= chance:

                if type==1:
                    beta=np.random.randint(2)

                    if beta==0:

                        if self.population[i].chromosom_value[0]==0:
                            self.population[i].chromosom_value[0]=1
                        else:
                            self.population[i].chromosom_value[0]=0
                    else:
                        if self.population[i].chromosom_value[self.chromosom_size-1]==0:
                            self.population[i].chromosom_value[self.chromosom_size-1]=1
                        else:
                            self.population[i].chromosom_value[self.chromosom_size-1]=0

                elif type==2:
                    mut_point = np.random.randint(0, self.chromosom_size)

                    if self.population[i].chromosom_value[mut_point] == 0:
                        self.population[i].chromosom_value[mut_point] = 1
                    else:
                        self.population[i].chromosom_value[mut_point] = 0

                elif type==3:
                    mut_point1=0
                    mut_point2=0

                    while mut_point1==mut_point2:
                        mut_point1 = np.random.randint(0, self.chromosom_size)
                        mut_point2 = np.random.randint(0, self.chromosom_size)

                    if self.population[i].chromosom_value[mut_point1] == 0:
                        self.population[i].chromosom_value[mut_point1] = 1
                    else:
                        self.population[i].chromosom_value[mut_point1] = 0

                    if self.population[i].chromosom_value[mut_point2] == 0:
                        self.population[i].chromosom_value[mut_point2] = 1
                    else:
                        self.population[i].chromosom_value[mut_point2] = 0






    def adapt(self):

        for i in range(0,self.epochs):
            np.random.randint(0, self.population_size)