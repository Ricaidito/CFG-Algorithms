import re
from typing import Dict, List, Tuple
from unitary import remove_unitary_productions

'''
CFG to CNF
Ref: https://ccia.ugr.es/~rosa/tutormc/teoria/gra_lib_cont.html#for_nor_chomsky
'''

# List of tuples to store the key of a production with variables, the variables to swap and their index in the list
variables_occurrences: List[Tuple[str, str, int]] = []

# Check if the grammar needs to remove unitary productions
def unitary_check(grammar: Dict[str, List[str]]):
    remove_unitary_productions(grammar)

# Check if all the variables are the same
def check_same(string: str):
    return len(set(string)) == 1

# Replace terminals with 'C_letter'
def replace_terminals(grammar: Dict[str, List[str]]):
    for productions in grammar.values():
        for production in productions:
            production_index = productions.index(production)
            for char in production:
                if "a" <= char <= "z":
                    productions[production_index] = production.replace(char, f"C_{char}")

# Get all of the occurrences of the variables that need to be replace
def get_variables_occurrences(grammar: Dict[str, List[str]]):
    variables_occurrences.clear()
    for key in grammar.keys():
        for production in grammar[key]:
            find = re.findall("[A-Z]{2,}", production)
            index = grammar[key].index(production)
            if len(find) == 1 and check_same(find[0]):
                variables_occurrences.append((key, find[0], index))

# Replace the variables with the new rules
def replace_variables(grammar: Dict[str, List[str]], variables_occurrences: List[Tuple[str, str, int]], rules_set: Dict[str, str]):
    for variable in variables_occurrences:
        replace_value = str()
        if variable[1] in rules_set.keys():
            replace_value = rules_set[variable[1]]
        else:
            replace_value = "X"
        grammar[variable[0]][variable[2]] = re.sub(variable[1], replace_value, grammar[variable[0]][variable[2]])

# Print the rules
def print_ruleset(rule_set: Dict[str, str]):
    print("\nRules:\n")
    for value, rule in rule_set.items():
        print(rule + " -> " + value)

# Convert from Context Free Grammar (CFG) to Chomsky Normal Form (CNF)
def cfg_to_chomsky(grammar: Dict[str, List[str]], rules: Dict[str, str] = {}):
    unitary_check(grammar)
    replace_terminals(grammar)
    get_variables_occurrences(grammar)
    replace_variables(grammar, variables_occurrences, rules)
    if len(rules.keys()) > 0:
        print_ruleset(rules)

# Driver code
def main():
    # Example grammar to convert from CFG to CNF
    grammar: Dict[str, List[str]] = {
        "S": ["bA", "aB"],
        "A": ["bAA", "AS", "a"],
        "B": ["aBB", "bS", "b"]
    }
    # Defined rules to replace the variables
    rules: Dict[str, str] = {
        "AA": "D",
        "BB": "E"
    }
    print("\nOriginal:\n")
    print(grammar)
    cfg_to_chomsky(grammar, rules)
    print("\nChomsky Normal Form:\n")
    print(grammar)

if __name__ == "__main__":
    main()
