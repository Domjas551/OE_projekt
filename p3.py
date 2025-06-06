#na podstawie przykładu: https://pypi.org/project/pygad/1.0.18/
import logging
import pygad
import numpy
import benchmark_functions as bf

#Konfiguracja algorytmu genetycznego

num_genes = 2
func = bf.Rastrigin(num_genes)
def fitness_func(ga_instance, solution, solution_idx):
    fitness = func(solution)
    return 1./fitness

fitness_function = fitness_func
num_generations = 100
sol_per_pop = 80
num_parents_mating = 50
#boundary = func.suggested_bounds() #możemy wziąć stąd zakresy
init_range_low = -5.12
init_range_high = 5.12
mutation_num_genes = 1
parent_selection_type = "tournament"
crossover_type = "uniform"
mutation_type = "random"


#Konfiguracja logowania

level = logging.DEBUG
name = 'logfile.txt'
logger = logging.getLogger(name)
logger.setLevel(level)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_format = logging.Formatter('%(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

def on_generation(ga_instance):
    ga_instance.logger.info("Generation = {generation}".format(generation=ga_instance.generations_completed))
    solution, solution_fitness, solution_idx = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)
    ga_instance.logger.info("Best    = {fitness}".format(fitness=1./solution_fitness))
    ga_instance.logger.info("Individual    = {solution}".format(solution=repr(solution)))

    tmp = [1./x for x in ga_instance.last_generation_fitness] #ponownie odwrotność by zrobić sobie dobre statystyki

    ga_instance.logger.info("Min    = {min}".format(min=numpy.min(tmp)))
    ga_instance.logger.info("Max    = {max}".format(max=numpy.max(tmp)))
    ga_instance.logger.info("Average    = {average}".format(average=numpy.average(tmp)))
    ga_instance.logger.info("Std    = {std}".format(std=numpy.std(tmp)))
    ga_instance.logger.info("\r\n")


#Właściwy algorytm genetyczny

ga_instance = pygad.GA(num_generations=num_generations,
          sol_per_pop=sol_per_pop,
          num_parents_mating=num_parents_mating,
          num_genes=num_genes,
          fitness_func=fitness_func,
          init_range_low=init_range_low,
          init_range_high=init_range_high,
          mutation_num_genes=mutation_num_genes,
          parent_selection_type=parent_selection_type,
          crossover_type=crossover_type,
          mutation_type=mutation_type,
          keep_elitism= 1,
          K_tournament=3,
          random_mutation_max_val=32.768,
          random_mutation_min_val=-32.768,
          logger=logger,
          on_generation=on_generation,
          parallel_processing=None)

ga_instance.run()


best = ga_instance.best_solution()
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=1./solution_fitness))


# sztuczka: odwracamy my narysował nam się oczekiwany wykres dla problemu minimalizacji
ga_instance.best_solutions_fitness = [1. / x for x in ga_instance.best_solutions_fitness]
ga_instance.plot_fitness()

num_genes=32
func = bf.Rastrigin(1)
def fitness_func_binary(ga_instance, solution, solution_idx):
    for i, x in enumerate(solution):
        if x >= 2.0:
            solution[i] = 1.99
    decode = -5.12+int(''.join(map(str, numpy.array(solution).astype(int))),2)*(5.12+5.12)/(pow(2,num_genes)-1)
    if func([decode]) == 0.0:
        return 9999999999.
    return 1./func([decode])
init_pop = []
for i in range(0, sol_per_pop):
    init_pop.append(numpy.random.randint(0,2,size=num_genes))

ga_instance = pygad.GA(num_generations=num_generations,
          initial_population=init_pop,
          sol_per_pop=sol_per_pop,
          num_parents_mating=num_parents_mating,
          num_genes=num_genes,
          fitness_func=fitness_func_binary,
          init_range_low=init_range_low,
          init_range_high=init_range_high,
          mutation_num_genes=mutation_num_genes,
          parent_selection_type=parent_selection_type,
          crossover_type=crossover_type,
          mutation_type=mutation_type,
          keep_elitism= 1,
          K_tournament=3,
          random_mutation_max_val=1,
          random_mutation_min_val=0,
          logger=logger,
          on_generation=on_generation,
          parallel_processing=None)

ga_instance.run()


best = ga_instance.best_solution()
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=numpy.array(solution).astype(int)))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=1./solution_fitness))


# sztuczka: odwracamy my narysował nam się oczekiwany wykres dla problemu minimalizacji
ga_instance.best_solutions_fitness = [1. / x for x in ga_instance.best_solutions_fitness]
ga_instance.plot_fitness()