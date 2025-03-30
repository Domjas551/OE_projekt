import math

from Chromosom import Chromosom
import numpy as np
import random

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
        return [self.lower_border+
                int(''.join(map(str,specimen.chromosom_value)),2)*
                (self.upper_border-self.lower_border)/
                (pow(2,self.chromosom_size)-1)]

    def fitness_function(self,specimen) -> float:
        x=self.decode_specimen(specimen)
        N=len(x)
        return 10*N+np.sum(xi**2-10*np.cos(2*np.pi*xi) for xi in x)

    def selection_best(self, amount, population):

        """
        population - lista z wynikami funkcji celu
        amount - liczba wybieranych osobników
        """

        best_ind=[]
        new_pop=[]

        for j in range(0, amount):
            x = 100
            ind = 0
            for i in range(0, len(population)):
                if i not in best_ind:
                    if abs(population[i]) < x:
                        x = population[i]
                        ind = i
            best_ind.append(ind)

        for i in best_ind:
            new_pop.append(self.population[i])

        return new_pop

    def selection_roullete(self,amount, population):
        """
        population - lista z wynikami funkcji celu
        amount - liczba wybieranych osobników
        """

        # lista odwróconej fitness function, dla funkcji minimalizacji
        pop2=[]
        # lista prawdopodobieństw
        prawd=[]
        # lista dystrybuant
        dyst=[]
        # nowa populacja
        new_pop=[]

        # odwrócenie fitness function
        for i in range(0,len(population)):
            pop2.append(1/population[i])

        #obliczenie sumy odwróconej fitness function
        S=sum(pop2)

        # utworzenie listy prawdopodobnieństw
        for i in range(0,len(pop2)):
            prawd.append(pop2[i]/S)

        #utworzenie listy dystrybuant
        for i in range(0,len(sorted(prawd))):
            if i==0:
                dyst.append(sorted(prawd)[i])
            else:
                dyst.append(dyst[i-1]+sorted(prawd)[i])


        #utworzenie nowej populacji
        for j in range(0, amount):
            alfa = random.uniform(0, 1)
            for i in range(0,len(dyst)):
                if alfa<dyst[i]:
                    new_pop.append(self.population[prawd.index(sorted(prawd)[i])])
                    break

        return new_pop

    def selection_tournament(self, amount, t_size, t_amount, population):
        """
        amount - liczba wybieranych osobników
        t_size - po ile osobników na turniej (k)
        t_amount - liczba turniejów (n)
        population - liczba wybieranych osobników
        """
        #return [item for item in list1 if item not in list2]
        new_pop=[]
        pop3=[]

        #powtarzaj aż do wylosowania 10 osobników
        while len(pop3)<amount:
            pop2=population.copy()
            #każdy obieg to jedna runda
            for j in range(0,t_amount):
                t = []
                #grupowanie na zespoły turniejowe
                for i in range(0,math.ceil(len(pop2)/t_size)):
                    t.append([])
                    while len(t[i]) < t_size and len(pop2)>0:
                        alfa = np.random.randint(0, len(pop2))
                        t[i].append(pop2[alfa])
                        pop2.pop(alfa)
                #wybranie zwycięzców
                for i in t:
                    pop2.append(min(i))

            #załadowanie ostatecznych zwyciezców do pop3
            for i in pop2:
                if len(pop3)<amount:
                    pop3.append(i)
                else:
                    break
        #załadowanie osobników na bazie wartości zwycięzców
        for i in pop3:
            new_pop.append(self.population[population.index(i)])

        return new_pop

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

                ch1=Chromosom(len(c1))
                ch2=Chromosom(len(c1))
                ch1.set_chromosom(c1)
                ch2.set_chromosom(c2)

                return [ch1,ch2]

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

                ch1 = Chromosom(len(c1))
                ch2 = Chromosom(len(c1))
                ch1.set_chromosom(c1)
                ch2.set_chromosom(c2)

                return [ch1, ch2]

            elif type == 3:

                for i in range(0,self.chromosom_size):
                    alfa = np.random.randint(0, 100)

                    if alfa<50:
                        c1.append(specimen2.chromosom_value[i])
                        c2.append(specimen1.chromosom_value[i])
                    else:
                        c1.append(specimen1.chromosom_value[i])
                        c2.append(specimen2.chromosom_value[i])

                ch1 = Chromosom(len(c1))
                ch2 = Chromosom(len(c1))
                ch1.set_chromosom(c1)
                ch2.set_chromosom(c2)

                return [ch1, ch2]

            elif type==4:

                for i in range(0,self.chromosom_size):
                    alfa = np.random.randint(0, 100)

                    if alfa<50:
                        c1.append(specimen1.chromosom_value[i])
                    else:
                        c1.append(specimen2.chromosom_value[i])

                ch1 = Chromosom(len(c1))
                ch1.set_chromosom(c1)

                return [ch1]
        else:
            return -1

    def mutation(self,population,chance,type=1):

        """
        Type:
        1 - mutacja brzegowa
        2 - mutacja jednopunktowa
        3 - mutacja dwupunktowa
        """

        for i in range(0,len(population)):
            alfa = np.random.randint(0, 100)

            if alfa <= chance:

                if type==1:
                    beta=np.random.randint(2)

                    if beta==0:

                        if population[i].chromosom_value[0]==0:
                            population[i].chromosom_value[0]=1
                        else:
                            population[i].chromosom_value[0]=0
                    else:
                        if population[i].chromosom_value[self.chromosom_size-1]==0:
                            population[i].chromosom_value[self.chromosom_size-1]=1
                        else:
                            population[i].chromosom_value[self.chromosom_size-1]=0

                elif type==2:
                    mut_point = np.random.randint(0, self.chromosom_size)

                    if population[i].chromosom_value[mut_point] == 0:
                        population[i].chromosom_value[mut_point] = 1
                    else:
                        population[i].chromosom_value[mut_point] = 0

                elif type==3:
                    mut_point1=0
                    mut_point2=0

                    while mut_point1==mut_point2:
                        mut_point1 = np.random.randint(0, self.chromosom_size)
                        mut_point2 = np.random.randint(0, self.chromosom_size)

                    if population[i].chromosom_value[mut_point1] == 0:
                        population[i].chromosom_value[mut_point1] = 1
                    else:
                        population[i].chromosom_value[mut_point1] = 0

                    if population[i].chromosom_value[mut_point2] == 0:
                        population[i].chromosom_value[mut_point2] = 1
                    else:
                        population[i].chromosom_value[mut_point2] = 0

    def inversion(self,population, chance):

        for i in range(0,len(population)):
            alfa = np.random.randint(0, 100)

            if alfa<= chance:

                cut_point1 = 0
                cut_point2 = 0

                while cut_point1 == cut_point2 or abs(cut_point1 - cut_point2) == 1:
                    cut_point1 = np.random.randint(0, self.chromosom_size)
                    cut_point2 = np.random.randint(0, self.chromosom_size)

                if cut_point1 < cut_point2:
                    c1=population[i].chromosom_value[cut_point1:cut_point2]
                    c2=list(reversed(c1))
                    population[i].chromosom_value[cut_point1:cut_point2]=c2
                else:
                    c1 = population[i].chromosom_value[cut_point2:cut_point1]
                    c2 = list(reversed(c1))
                    population[i].chromosom_value[cut_point2:cut_point1] = c2

    def adapt(self,type_s,type_c,type_m,chance_c,chance_m,chance_in,elite_amount=2,t_size=3,t_amount=2):

        """
        type_s - typ selekcji, 1 - best, 2 - roullete, 3 - tournament
        type_c - typ krzyżowania, 1 - jednopunktowe, 2 - dwupunktowe, 3 - jednorodne, 4 - ziarniste
        type_m - typ mutacji, 1 - brzegowa, 2 - jednopunktowa, 3 - dwupunktowa
        chance_c - szansa na krzyżowanie
        chance_m - szansa mutacji
        chance_in - szansa na inwersje
        elite_amount - ilość osobników wybieranych w strategi elitarnej
        t_size - ilość osobników w grupach w selekcji turniejowej
        t_amount - ilość rund w selekcji turniejowej
        """

        for e in range(0,self.epochs):

            fitness_list=[]
            pop2=[]
            new_pop=[]
            base_pop=[]

            #utworzenie tablicy z obliczonymi wartościami fitness function
            for i in range(0, self.population_size):
                fitness_list.append(self.fitness_function(self.population[i]))

            #strategia elitarna
            new_pop.extend(self.selection_best(elite_amount,fitness_list))

            #selekcja
            if type_s==1:
                base_pop.extend(self.selection_best(self.population_size//2, fitness_list))
            elif type_s==2:
                base_pop.extend(self.selection_roullete(self.population_size//2, fitness_list))
            elif type_s==3:
                base_pop.extend(self.selection_tournament(self.population_size//2,t_size,t_amount,fitness_list))

            #krzyżowanie
            while len(new_pop)<self.population_size:

                spec1=0
                spec2=0

                while spec1==spec2:
                    spec1 = np.random.randint(0, len(base_pop))
                    spec2 = np.random.randint(0, len(base_pop))

                if type_c==1:
                    if len(new_pop)==self.population_size-1:
                        a=self.crossing(base_pop[spec1], base_pop[spec2], chance_c, 1)[0]
                        if a!=-1:
                            new_pop.extend(a)
                    else:
                        a = self.crossing(base_pop[spec1], base_pop[spec2], chance_c, 1)
                        if a!=-1:
                            new_pop.extend(a)
                elif type_c==2:
                    if len(new_pop) == self.population_size - 1:
                        a = self.crossing(base_pop[spec1], base_pop[spec2], chance_c, 2)[0]
                        if a!=-1:
                            new_pop.extend(a)
                    else:
                        a = self.crossing(base_pop[spec1], base_pop[spec2], chance_c, 2)
                        if a!=-1:
                            new_pop.extend(a)
                elif type_c==3:
                    if len(new_pop) == self.population_size - 1:
                        a = self.crossing(base_pop[spec1], base_pop[spec2], chance_c, 3)[0]
                        if a!=-1:
                            new_pop.extend(a)
                    else:
                        a = self.crossing(base_pop[spec1], base_pop[spec2], chance_c, 3)
                        if a!=-1:
                            new_pop.extend(a)
                elif type_c==4:
                    a = self.crossing(base_pop[spec1], base_pop[spec2], chance_c, 4)
                    if a!=-1:
                        new_pop.extend(a)

            #mutacja
            self.mutation(new_pop,chance_m,type_m)

            #inwersja
            self.inversion(new_pop,chance_in)

            #zapisanie nowej populacji
            self.population=new_pop

            # sprawdzenie uzyskanych wartości
            for i in range(0, self.population_size):
                fitness_list.append(self.fitness_function(new_pop[i]))
            print(fitness_list)

        #wypisanie najlepszego rozwiązania
        fl=[]
        for i in range(0, self.population_size):
            fl.append(self.fitness_function(self.population[i]))
        solution=self.selection_best(1,fl)[0]
        print(solution)
        print(solution.chromosom_value)
        print(self.fitness_function(solution))

