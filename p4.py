import numpy as np
from mealpy.human_based.BRO import DevBRO
from mealpy import FloatVar

def fitness_func(solution):
    N=solution.size
    return 10*N+np.sum(xi**2-10*np.cos(2*np.pi*xi) for xi in solution)

problem_dict = {
    "bounds": FloatVar(lb = -5.12, ub = 5.12),
    "obj_func": fitness_func,
    "minmax": "min"
}

epoch = 100
pop_size = 10
threshold = 3

model = DevBRO(epoch, pop_size, threshold)
best = model.solve(problem_dict)
print(best)
