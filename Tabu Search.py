def calculate_distance(graph, path_coord):
    distance = 0
    for i, j in enumerate(path_coord[:-1]):
        matrix_index = ((j, path_coord[i+1]))
        distance += graph[matrix_index]
    return distance

def initial_solution_greedy(graph):
    visited = set()
    path = list()
    start = 0
    following = 0
    path.append(start)
    visited.add(start)
    for i in range(len(graph) - 1):
        row = np.copy(graph[start])
        row[list(visited)] = np.inf
        following = np.where(row==np.amin(row))[0][0]
        visited.add(following)
        path.append(following)
        start = following
    path.append(0)
    return path

def initial_solution_random(graph):
    path = np.random.choice(range(1, len(graph)), len(graph)-1, False)
    path = list(path)
    path.insert(0, 0)
    path.append(0)
    return path

def get_neighbors(graph, solution, tabu, tenure, neighbors=4):
    switch = None
    switch_rev = None
    candidate = np.array(solution)
    tabu_dict = dict()
    solution_distance = calculate_distance(graph, solution)
    for i in range(neighbors):
        found = False
        while found == False:
            candidate_copy = np.copy(solution)
            switch = tuple(np.random.choice(range(1, len(graph)), 2, replace=False))
            switch_rev = (switch[1], switch[0])
            candidate_copy[switch[0]], candidate_copy[switch[1]] = candidate_copy[switch[1]], candidate_copy[switch[0]]
            candidate_distance = calculate_distance(graph, candidate_copy)
            if tabu[switch] < 1 and tabu[switch_rev] < 1:
                tabu_dict[switch] = candidate_distance
                found = True
            # Aspiration criteria; if the index is in tabu but the solution increases then accept the solution.
            elif tabu[switch] <= (tenure / 2) and tabu[switch_rev] <= (tenure / 2) and candidate_distance < solution_distance:
                tabu_dict[switch] = candidate_distance
                found = True
    best = sorted(tabu_dict, key=tabu_dict.get)[0]
    candidate[best[0]], candidate[best[1]] = candidate[best[1]], candidate[best[0]]
    switch = best
    switch_rev = (best[1], best[0])
    return candidate, switch, switch_rev
  
  def update_tabu(tabu, switch, switch_rev, tenure=3):
    tabu_copy = np.copy(tabu)
    tabu_copy -= 1
    tabu_copy[switch, switch_rev] = tenure
    return tabu_copy
  
  def tabu_search(graph, iterations=500, neighbors=15, tenure=10, init_method='random'):
    current = None
    if init_method == 'greedy':
        current = initial_solution_greedy(graph)
    else:
        current = initial_solution_random(graph)
    tabu_matrix = np.zeros(graph.shape)
    route = []
    route.append(calculate_distance(graph, current))
    for i in range(iterations):
        candidate, switch, switch_rev = get_neighbors(graph, current, tabu_matrix, neighbors)
        tabu_matrix = update_tabu(tabu_matrix, switch, switch_rev, tenure)
        print(candidate, calculate_distance(graph, candidate))
        route.append(calculate_distance(graph, candidate))
    return route
