class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

def forward_reasoning(KB, query):
    inferred = set()
    while True:
        new_inferred = set()
        for rule in KB.rules:
            for fact in KB.facts:
                result = rule(fact)
                if result and result not in KB.facts:
                    new_inferred.add(result)
        if not new_inferred:
            break
        KB.facts.update(new_inferred)
        inferred.update(new_inferred)
        if query in inferred:
            return True
    return False

if __name__ == "__main__":
    KB = KnowledgeBase()
    KB.add_fact("Human(Socrates)")
    KB.add_rule(lambda fact: "Mortal(Socrates)" if fact == "Human(Socrates)" else None)
    query = "Mortal(Socrates)"
    result = forward_reasoning(KB, query)
    if result:
        print(f"The query '{query}' is TRUE.")
    else:
        print(f"The query '{query}' is FALSE.")
