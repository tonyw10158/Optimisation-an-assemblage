import numpy as np

def selection(f, population, select='tournament', num=6):
    parent = None
    if select == 'tournament':
        raw_sample = np.random.choice(list(population), num)
        parent = sorted(raw_sample, key=f)
        parent = parent[0]
    # Roulette selection is currently bugged due to NaN probabilities.
    elif select == 'roulette':
        sorted_population = sorted(population, key=f)
        sorted_fitness = [f(individual) for individual in sorted_population]
        fitness_list = sorted_fitness / np.sum(sorted_fitness)
        fitness_list = fitness_list[::-1]
        parent = np.random.choice(population, 1, p=fitness_list)        
    elif select == 'truncation':
        sorted_population = sorted(population, key=f)
        sorted_population = sorted_population[:num]
        parent = np.random.choice(sorted_population, 1)
    return parent
  
  def crossover(parent1, parent2, population, scalar=0.5, cross='single'):
    offspring = np.zeros(len(population))
    if cross == 'single':
        rand = np.random.randint(0, len(population))
        offspring[:rand] = parent1
        offspring[rand:] = parent2
    elif cross == 'double':
        rand1 = np.random.randint(0, len(population) - 1)
        rand2 = np.random.randint(rand1, len(population))
        offspring[:rand1] = parent1
        offspring[rand1+1:rand2] = parent2
        offspring[rand2:] = parent1
    elif cross == 'uniform':
        for i in range(len(offspring)):
            rand = np.random.randint(0, 1)
            if rand <= 0.5:
                offspring[i] = parent1
            else:
                offspring[i] = parent2
    elif cross == 'real':
        x = ((1 - scalar) * parent1) + scalar * parent2
        offspring.fill(x)
    return offspring
  
  def mutate(offspring):
    rate = 1 / len(offspring)
    for i in range(len(offspring)):
        draw = np.random.uniform(0, 1)
        if draw <= rate:
            offspring[i] += np.random.normal(0, 1)
    return offspring
  
  def genetic_algorithm(f, dim=20, select='tournament', cross='single', init_method='cauchy', scalar=0.5, k_max=25000):
    x_init = None
    if init_method == 'cauchy':
        x_init = np.random.standard_cauchy(dim)  
    if init_method == 'gaussian':
        x_init = np.random.normal(0, 1, dim)
    if init_method == 'uniform':
        x_init = np.random.uniform(-3, 3, dim)
    f_evals = []
    for k in range(k_max):
        parent_1 = selection(f, population=x_init, select=select, num=7)
        parent_2 = selection(f, population=x_init, select=select, num=7)
        offspring = crossover(parent1=parent_1, parent2=parent_2, population=x_init, cross=cross)
        offspring = mutate(offspring)
        x_init = offspring
        f_evals.append(f(x_init))
    return f_evals
