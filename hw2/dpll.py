import os

class Literal:
    """
    sign = either positive (True), or negative (False)
    name = character representing a variable i.e. a, b, c
    """
    def __init__(self, str_representation="", ref=None):
        if ref:
            #copy literal if provided
            self.sign = ref.sign
            self.name = ref.name
        else:
            self.sign = True
            if str_representation.startswith("-"):
                str_representation = str_representation[1:]
                self.sign = False
            self.name = str_representation #a, b, or c...
    
    def __str__(self):
        sign = "+" if self.sign else "-"
        return f"{sign}{self.name}"

    def equals(self, literal):
        return self.sign == literal.sign and self.name == literal.name

    def opposite(self):
        self.sign = not self.sign
        return self
    
    def is_opposite(self, literal):
        return self.sign != literal.sign and self.name == literal.name

def print_cnf(cnf, label):
    print(label)
    print([[l.__str__() for l in clause] for clause in cnf])

def read_cnf(path, has2spaces=False):
    """
    Expected format: nested array of Literals: i.e. [[Literal()], [Literal(), Literal()]]
    """
    cnf = []
    with open(path, 'r') as f:
        cnf_str = f.read()
    char_spacer = "  " if has2spaces else " "
    return [[Literal(char) for char in line.split(char_spacer)] for line in cnf_str.split("\n")]
    
def handle_pure_literals(cnf):
    """
    Return all pure literals in the cnf
    """
    pure = dict()
    for clause in cnf:
        for lit in clause:
            match = pure.get(lit.name, None)
            if type(match) == type(lit) and not match.equals(lit):
                pure[lit.name] = "invalid"
            if not match:
                pure[lit.name] = lit

    for lit in pure.values():
        if lit == "invalid":
            continue
        cnf = simplify(cnf, lit) 
    return cnf

def handle_unit_clauses(cnf):
    """
    Return all unit clauses in cnf.
    """
    units = set()
    for clause in cnf:
        if len(clause) == 1:
            units.add(clause[0])
    for unit in units:
        cnf = simplify(cnf, unit)
    return cnf

def simplify(cnf, lit):
    """
    Based on selected literal, simplify the cnf
    """
    for clause in cnf:
        for l in clause:
            if l.equals(lit):
                cnf.remove(clause)
                break
            elif l.is_opposite(lit):
                clause.remove(l)
    return cnf


def dpll(cnf):
    print_cnf(cnf, "new frame")
    if len(cnf) == 0: return True 
    for clause in cnf:
        if len(clause) == 0: return False 
    cnf = handle_pure_literals(cnf)
    print_cnf(cnf, "after handling pure lits")
    cnf = handle_unit_clauses(cnf)
    print_cnf(cnf, "after unit clauses")
    for clause in cnf:
        for l in clause:
            #pick first available clause
            print("picking clause: ", l)
            opp_l = Literal(ref=l).opposite()
            res = dpll(simplify(cnf, l)) or dpll(simplify(cnf, opp_l))
            if res: return True #found a satisfiable assignment
    #none of the available literals were satisfiable
    return False


    
if __name__ == "__main__":
    def e2e(path, has2spaces=False):
        print(f"------------------- New Test: {path} ---------------------")
        full_path = os.path.join("tests", path)
        print("Result: ", dpll(read_cnf(full_path, has2spaces=has2spaces)))
    e2e("cnf1.txt")
    e2e("cnf2.txt")
    e2e("cnf3.txt")
    e2e("cnf4.txt")
    e2e("cnf5.txt", has2spaces=True)