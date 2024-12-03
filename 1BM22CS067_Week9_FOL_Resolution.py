import re
import collections
import itertools
import copy
import time
import queue

def standardization(sentence, variable_map, counter):
    sentence_list = list(sentence)
    for i in range(len(sentence_list)):
        if sentence_list[i] == ',' or sentence_list[i] == '(':
            if sentence_list[i+1].islower():
                if sentence_list[i+1] not in variable_map:
                    variable_map[sentence_list[i+1]] = f"var{counter}"
                    sentence_list[i+1] = f"var{counter}"
                    counter += 1
                else:
                    sentence_list[i+1] = variable_map[sentence_list[i+1]]
    return "".join(sentence_list), variable_map, counter

def is_variable(x):
    return isinstance(x, str) and x.islower()

def unify(x, y, theta):
    if theta is None:
        return None
    elif x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    else:
        return None

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    else:
        theta[var] = x
        return theta

def negate(literal):
    if literal[0] == '~':
        return literal[1:]
    else:
        return '~' + literal

def substitute(expr, theta):
    if is_variable(expr):
        if expr in theta:
            return theta[expr]
        else:
            return expr
    else:
        return expr

def resolve_clauses(clause1, clause2):
    for literal1 in clause1:
        for literal2 in clause2:
            theta = unify(literal1, negate(literal2), {})
            if theta is not None:
                new_clause = []
                for literal in clause1:
                    new_literal = substitute(literal, theta)
                    if new_literal not in new_clause and new_literal != negate(literal2):
                        new_clause.append(new_literal)
                for literal in clause2:
                    new_literal = substitute(literal, theta)
                    if new_literal not in new_clause and new_literal != literal2:
                        new_clause.append(new_literal)
                if not new_clause:
                    return 'NIL'
                return new_clause
    return None

def resolve(kb, query):
    q = queue.Queue()
    q.put(query)
    processed_clauses = set()

    while not q.empty():
        clause = q.get()
        clause_tuple = tuple(clause)
        if clause_tuple in processed_clauses:
            continue
        processed_clauses.add(clause_tuple)

        for clause2 in kb:
            resolvent = resolve_clauses(clause, clause2)
            if resolvent == 'NIL':
                return True
            if resolvent is not None and tuple(resolvent) not in processed_clauses:
                q.put(resolvent)
    
    return False

def prove_query(kb, query):
    negated_query = negate(query)
    
    if resolve(kb, [negated_query]):
        return False
    else:
        return True

kb = {
    'Likes': {1: [["Likes(John, x)", "~Food(x)"]]},
    'Food': {1: [["Food(Apple)", "Food(Vegetables)", "Food(Peanuts)"]]},
    'Eats': {1: [["Eats(Anil, Peanuts)"]]},
    'Killed': {1: [["~Killed(Anil)"]]}
}

queries = ['Likes(John, Peanuts)']

for query in queries:
    if prove_query(kb, query):
        print(f"Query '{query}' is provable.")
    else:
        print(f"Query '{query}' is not provable.")
