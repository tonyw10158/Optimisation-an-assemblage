def annealing_schedule(schedule, temperature, temperature_init, iteration, gamma=0.75):
    temperature_prev = temperature
    if schedule == 'logarithmic':
        temperature = temperature_init * log(2) / log((iteration + 1) + 1)
    elif schedule == 'exponential':
        temperature = gamma * temperature_prev
    elif schedule == 'fast':
        temperature = temperature_init / (iteration + 1)
    return temperature
  
  def simulated_annealing(f, dim=20, schedule='exponential', temperature=10000000, gamma = 0.75, init_method='gaussian', k_max=25000):
    x = None
    if init_method == 'cauchy':
        x = np.random.standard_cauchy(dim)
    if init_method == 'gaussian':
        x = np.random.normal(0, 2, dim)
    if init_method == 'uniform':
        x = np.random.uniform(-2, 2, dim)
    temp_current = temperature
    y = f(x)
    f_evals = []
    f_evals.append(y)
    for i in range(k_max):
        std_dev = statistics.stdev(x)
        x_new = x + np.random.normal(0, std_dev, dim)
        y_new = f(x_new)
        delta_y = y_new - y
        if delta_y <= 0:
            x = x_new
            y = y_new
        else:
            temp_new = annealing_schedule(schedule, temp_current, temperature, i, gamma)
            criterion = np.exp(-delta_y / temp_new)
            temp_current = temp_new
            acceptance = min(criterion, 1)
            draw = np.random.uniform()
            if draw <= acceptance:
                x = x_new
                y = y_new
        f_evals.append(y_new)
    return f_evals
