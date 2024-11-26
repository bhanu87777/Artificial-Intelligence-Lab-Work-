import heapq

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                  4: (1, 0), 5: (1, 1), 6: (1, 2),
                  7: (2, 0), 8: (2, 1), 0: (2, 2)}

moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def is_goal(state):
    return state == goal_state

def get_zero_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def swap(state, pos1, pos2):
    new_state = [row[:] for row in state]
    new_state[pos1[0]][pos1[1]], new_state[pos2[0]][pos2[1]] = new_state[pos2[0]][pos2[1]], new_state[pos1[0]][pos1[1]]
    return new_state

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:
                goal_i, goal_j = goal_positions[tile]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

def a_star_manhattan(initial_state):
    priority_queue = []
    heapq.heappush(priority_queue, (manhattan_distance(initial_state), initial_state, 0, None))
    visited = set()
    parent_map = {}
    
    while priority_queue:
        _, current_state, g, parent = heapq.heappop(priority_queue)
        
        if is_goal(current_state):
            path = []
            while current_state:
                path.append(current_state)
                current_state = parent_map.get(tuple(map(tuple, current_state)))
            return path[::-1]
        
        current_state_tuple = tuple(map(tuple, current_state))
        if current_state_tuple in visited:
            continue
        visited.add(current_state_tuple)
        
        zero_x, zero_y = get_zero_position(current_state)
        
        for move_x, move_y in moves:
            new_x, new_y = zero_x + move_x, zero_y + move_y
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = swap(current_state, (zero_x, zero_y), (new_x, new_y))
                new_state_tuple = tuple(map(tuple, new_state))
                
                if new_state_tuple not in visited:
                    h = manhattan_distance(new_state)
                    f = g + 1 + h
                    heapq.heappush(priority_queue, (f, new_state, g + 1, current_state))
                    parent_map[new_state_tuple] = current_state
    
    return None

def print_puzzle(state):
    for row in state:
        print(row)
    print()

if __name__ == "__main__":
    initial_state = [[1, 2, 3],
                     [4, 0, 6],
                     [7, 5, 8]]
    
    print("Initial State:")
    print_puzzle(initial_state)
    
    solution = a_star_manhattan(initial_state)
    
    if solution:
        print("Solution found! Steps:")
        for step in solution:
            print_puzzle(step)
    else:
        print("No solution found.")
