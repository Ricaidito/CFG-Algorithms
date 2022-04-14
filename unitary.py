from typing import Dict, List, Tuple

'''
CFG without null productions to CFG without unitary productions
Ref: https://ccia.ugr.es/~rosa/tutormc/teoria/gra_lib_cont.html#prod_unitarias
'''

# List of tuples to store the key of a production with unitary values, the production to swap and their equivalence
unitary_list: List[Tuple[str, str, str]] = []

# Check if there's any unitary productions in the grammar
def check_for_unitary(grammar: Dict[str, List[str]]) -> bool:
    for key in grammar.keys():
        for production in grammar[key]:
            if len(production) == 1 and "A" <= production <= "Z":
                return True
    return False

# Get all unitary keys of a grammar (key, production, equivalence)
def get_unitary_keys(grammar: Dict[str, List[str]]):
    unitary_list.clear()
    for key in grammar.keys():
        for production in grammar[key]:
            if len(production) == 1 and "A" <= production <= "Z":
                unitary_list.append((key, production, grammar[production]))

# Swap the unitary productions with their equivalence
def do_swap(grammar: Dict[str, List[str]], key: str, prod_to_swap: str, swap_value: List[str]):
    grammar[key].remove(prod_to_swap)
    for prod in swap_value:
        grammar[key].append(prod)

# Helper method to remove all the unitary productions
def remove_unitary(grammar: Dict[str, List[str]], allow_duplicates: bool):
    while check_for_unitary(grammar):
        for swap_occur in unitary_list:
            do_swap(grammar, swap_occur[0], swap_occur[1], swap_occur[2])
        get_unitary_keys(grammar)
    if not allow_duplicates:
        remove_duplicates(grammar)

# Remove duplicate productions
def remove_duplicates(grammar: Dict[str, List[str]]):
    for key in grammar.keys():
        grammar[key] = list(dict.fromkeys(grammar[key]))

# Check for unitary productions and transform them
def remove_unitary_productions(grammar: Dict[str, List[str]], allow_duplicates: bool = False):
    if check_for_unitary(grammar):
        get_unitary_keys(grammar)
        remove_unitary(grammar, allow_duplicates)

# Driver code
def main():
    # Example grammar to transform
    grammar: Dict[str, List[str]] = {
        "S": ["ABb", "Ab", "Bb", "ABC", "AB", "AC", "BC", "A", "B", "C"],
        "C": ["abC", "ab", "AB", "A", "B"],
        "B": ["bB", "b"],
        "A": ["aA", "a"]
    }
    print("\nOriginal:\n")
    print(grammar)
    remove_unitary_productions(grammar, allow_duplicates=True)
    print("\nAfter removing the unit productions:\n")
    print(grammar)

if __name__ == "__main__":
    main()
