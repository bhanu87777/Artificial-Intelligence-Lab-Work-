def unify(x, y):
    substitutions = {}
    stack = [(x, y)]

    while stack:
        a, b = stack.pop()

        if a == b:
            continue

        elif is_variable(a):
            substitutions = unify_variable(a, b, substitutions)

        elif is_variable(b):
            substitutions = unify_variable(b, a, substitutions)

        elif is_compound(a) and is_compound(b):
            if function_name(a) != function_name(b) or arity(a) != arity(b):
                raise UnificationError(f"Cannot unify {a} and {b}")
            stack.extend(zip(arguments(a), arguments(b)))

        else:
            raise UnificationError(f"Cannot unify {a} and {b}")

    return substitutions


def unify_variable(var, term, substitutions):
    if var in substitutions:
        return unify(substitute(var, substitutions), substitute(term, substitutions))

    elif term in substitutions:
        return unify(substitute(var, substitutions), substitute(term, substitutions))

    elif occurs_check(var, term, substitutions):
        raise UnificationError(f"Occurs check failed: {var} occurs in {term}")

    else:
        substitutions[var] = term
        return substitutions


def substitute(term, substitutions):
    while is_variable(term) and term in substitutions:
        term = substitutions[term]
    if is_compound(term):
        return (function_name(term), [substitute(arg, substitutions) for arg in arguments(term)])
    return term


def occurs_check(var, term, substitutions):
    if var == term:
        return True
    elif is_compound(term):
        return any(occurs_check(var, arg, substitutions) for arg in arguments(term))
    return False


def is_variable(term):
    return isinstance(term, str) and term.islower()


def is_compound(term):
    return isinstance(term, tuple) and len(term) > 1


def function_name(term):
    return term[0] if is_compound(term) else None


def arguments(term):
    return term[1:] if is_compound(term) else []


def arity(term):
    return len(arguments(term))


class UnificationError(Exception):
    pass


if __name__ == "__main__":
    term1 = ("P", ("f", "x"), "y")
    term2 = ("P", ("f", "a"), "b")

    try:
        result = unify(term1, term2)
        print("Unification successful! Substitutions:", result)
    except UnificationError as e:
        print("Unification failed:", e)
