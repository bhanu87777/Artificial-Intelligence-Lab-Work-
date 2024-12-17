def alpha_beta_pruning(node, depth, alpha, beta, maximizing_player, tree, log):
    if node not in tree:
        return node

    if maximizing_player:
        best = -float('inf')
    else:
        best = float('inf')

    for child in tree[node]:
        if maximizing_player:
            val = alpha_beta_pruning(child, depth + 1, alpha, beta, False, tree, log)
            best = max(best, val)
            alpha = max(alpha, best)
        else:
            val = alpha_beta_pruning(child, depth + 1, alpha, beta, True, tree, log)
            best = min(best, val)
            beta = min(beta, best)

        log.append({
            "Node": node,
            "Child": child,
            "Alpha": alpha,
            "Beta": beta,
            "Pruned": beta <= alpha
        })

        if beta <= alpha:
            break

    return best

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [3, 5],
    'E': [6, 9],
    'F': [1, 2],
    'G': [0, -1]
}

log = []
root_value = alpha_beta_pruning('A', 0, -float('inf'), float('inf'), True, tree, log)

print(f"Value of the root node: {root_value}")

print("\nAlpha-Beta Log:")
for entry in log:
    print(entry)
