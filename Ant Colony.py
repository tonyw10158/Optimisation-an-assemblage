import numpy as np

def send_ants(nodes, m, tau, eta, alpha, beta, start):
    history = []
    for ant in range(m):
        route = []
        visited = {start}
        current = start
        for node in range(len(nodes) - 1):
            tau_copy = np.array(tau[current])
            eta_copy = np.array(eta[current])
            tau_copy[list(visited)] = 0
            eta_copy[list(visited)] = 0
            attractiveness = np.multiply(np.power(tau_copy, 
            alpha), np.power(eta_copy, beta))
            probabilities = attractiveness / attractiveness.sum()
            following = np.random.choice(len(nodes), 
            p=probabilities)
            route.append((current, following))
            current = following
            visited.add(following)
        route.append((current, start))
        dist = 0
        for i in route:
            dist += nodes[i]
        history.append((route, dist))
    return history
  
def update_pheromones(graph, history, tau, rho):
    pheromones = np.copy(tau)
    pheromones *= (1.0-rho)
    for i in range(len(history)):
        for j in history[i][0]:
            pheromones[j] += (1.0 / graph[j])
    return pheromones
  
def ant_colony_optimization(nodes, m=10, alpha=1, beta=5, rho=0.75, k_max=500):
    best_route = (None, np.inf)
    trace_route = []
    tau = np.ones(nodes.shape) / len(nodes)     # Pheromone levels.
    eta = 1 / nodes                             # Prior edge weights.
    start = 0
    for k in range(k_max):
        history = send_ants(nodes, m, tau, eta, alpha, beta, start)
        tau = update_pheromones(nodes, history, tau, rho)
        shortest_route = min(history, key=lambda x: x[1])
        print(shortest_route)
        if shortest_route[1] < best_route[1]:
            best_route = shortest_route
        trace_route.append(shortest_route[1])
    return best_route, trace_route
