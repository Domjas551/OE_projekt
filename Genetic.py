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

    def crossing(self,specimen1 ,specimen2,chance,type=1):

        alfa=np.random.randint(0, 100)

        if alfa<=chance:
            c1 = []
            c2 = []

            if type==1:
                cut_point=np.random.randint(0, self.chromosom_size)
                print(cut_point)

                c1.extend(specimen1.chromosom_value[:cut_point])
                c1.extend(specimen2.chromosom_value[cut_point:])
                c2.extend(specimen2.chromosom_value[:cut_point])
                c2.extend(specimen1.chromosom_value[cut_point:])

                print("c1 "+str(c1))
                print("c2 "+str(c2))

            elif type==2:

                cut_point1 = 0
                cut_point2 = 0

                while cut_point1==cut_point2 or abs(cut_point1-cut_point2)==1:
                    cut_point1 = np.random.randint(0, self.chromosom_size)
                    cut_point2 = np.random.randint(0, self.chromosom_size)

                print(cut_point1)
                print(cut_point2)

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
                print("c1 " + str(c1))
                print("c2 " + str(c2))

            elif type == 3:

                for i in range(0,self.chromosom_size):
                    alfa = np.random.randint(0, 100)

                    if alfa<50:
                        c1.append(specimen2.chromosom_value[i])
                        c2.append(specimen1.chromosom_value[i])
                    else:
                        c1.append(specimen1.chromosom_value[i])
                        c2.append(specimen2.chromosom_value[i])
                print("c1 " + str(c1))
                print("c2 " + str(c2))

            else:

                for i in range(0,self.chromosom_size):
                    alfa = np.random.randint(0, 100)

                    if alfa<50:
                        c1.append(specimen1.chromosom_value[i])
                    else:
                        c1.append(specimen2.chromosom_value[i])
                print("c1 " + str(c1))



    def adapt(self):

        for i in range(0,self.epochs):
            np.random.randint(0, self.population_size)