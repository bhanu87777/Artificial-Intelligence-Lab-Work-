import math
import random


def simulated_annealing(initial_state, cost_function, neighbor_function, temperature, cooling_rate, min_temperature):
    current_state = initial_state
    current_cost = cost_function(current_state)

    best_state = current_state
    best_cost = current_cost

    while temperature > min_temperature:
     
        new_state = neighbor_function(current_state)
        new_cost = cost_function(new_state)

        delta_cost = new_cost - current_cost

        if delta_cost < 0 or random.random() < math.exp(-delta_cost / temperature):
            current_state = new_state
            current_cost = new_cost

            if current_cost < best_cost:
                best_state = current_state
                best_cost = current_cost

        temperature *= cooling_rate

    return best_state, best_cost


def tsp_cost(state):
    cost = 0
    for i in range(len(state)):
        cost += distance[state[i]][state[(i + 1) % len(state)]]
    return cost


def tsp_neighbor(state):
    a, b = random.sample(range(len(state)), 2)
    state[a], state[b] = state[b], state[a]
    return state

distance = [
    [0, 2, 9, 10, 7],
    [2, 0, 8, 5, 6],
    [9, 8, 0, 4, 3],
    [10, 5, 4, 0, 1],
    [7, 6, 3, 1, 0]
]

initial_state = list(range(len(distance)))
random.shuffle(initial_state)

initial_temperature = 100
cooling_rate = 0.95
min_temperature = 1e-3

best_state, best_cost = simulated_annealing(
    initial_state, tsp_cost, tsp_neighbor, initial_temperature, cooling_rate, min_temperature
)

print("Best state (city order):", best_state)
print("Best cost (shortest distance):", best_cost)
