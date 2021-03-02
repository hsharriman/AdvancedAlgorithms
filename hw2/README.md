### DPLL Pseudocode
```
Pseudocode:
simplify(CNF, literal):
    emove all clauses containing literal w same sign
        for every clause:
            remove all CASES of literal with opposite sign

DPLL(CNF):
    if CNF has no clauses:
        return True
    for each clause in CNF:
        if clause is empty:
            return False
    for each lit in findPureLiteral(CNF):
        simplify(CNF, lit)
    for each lit in findUnitClause(CNF):
        simplify(CNF, lit)
    x = choose unassigned literal from CNF
    return DPLL(simplify CNF where x = 0) or DPLL(simplify CNF where x = 1)
```

### DPLL Pseudocode for Returning Output
The general idea is to track the assigned variables with a dictionary that gets passed around with recursive calls.
```
simplify(CNF, literal):
    emove all clauses containing literal w same sign
        for every clause:
            remove all CASES of literal with opposite sign

DPLL(CNF, assign={}):
    if CNF has no clauses:
        return True, assign
    for each clause in CNF:
        if clause is empty:
            return False, assign
    for each lit in findPureLiteral(CNF):
        assign[lit] = (if lit is +: 1 else lit = 0)
        simplify(CNF, lit)
    for each lit in findUnitClause(CNF):
        assign[lit] = (if lit is +: 1 else lit = 0)
        simplify(CNF, lit)
    x = choose unassigned literal from CNF
    res, assign = DPLL(simplify CNF where x = 0, assign{x:1})
    if res:
        return True, assign
    res, assign: DPLL(simplify CNF where x = 1, assign{x:0})
    if res:
        return True, assign
    return False, assign
```


#### Sample Input
```
1 -5 4 0
-1 5 3 4 0
-3 -4 0
```


#### Outputs
```
------------------- New Test: cnf1.txt ---------------------
new frame
[['+1', '-5', '+4', '+0'], ['-1', '+5', '+3', '+4', '+0'], ['-3', '-4', '+0']]
after handling pure lits
[['-1', '+5', '+3', '+4', '+0']]
after unit clauses
[['-1', '+5', '+3', '+4', '+0']]
picking clause:  -1
new frame
[]
Result:  True
------------------- New Test: cnf2.txt ---------------------
new frame
[['+a', '+b', '+c', '+d'], ['-a'], ['+a', '+b', '-c'], ['+a', '-b'], ['+b', '-d']]
after handling pure lits
[['+a', '+b', '+c', '+d'], ['-a'], ['+a', '+b', '-c'], ['+a', '-b'], ['+b', '-d']]
after unit clauses
[['+b', '+c', '+d'], ['+a', '+b', '-c'], ['-b'], ['+b', '-d']]
picking clause:  +b
new frame
[['+a', '+b', '-c'], []]
new frame
[['+a', '-c'], []]
picking clause:  +c
new frame
[['+a'], []]
new frame
[['+a'], []]
picking clause:  +d
new frame
[['+a'], []]
new frame
[['+a'], []]
Result:  False
------------------- New Test: cnf3.txt ---------------------
new frame
[['+a', '+b', '-c'], ['-a', '-b', '+c'], ['-a', '+b', '-c']]
after handling pure lits
[['+a', '+b', '-c'], ['-a', '-b', '+c'], ['-a', '+b', '-c']]
after unit clauses
[['+a', '+b', '-c'], ['-a', '-b', '+c'], ['-a', '+b', '-c']]
picking clause:  +a
new frame
[['-a', '-b', '+c'], ['+b', '-c']]
after handling pure lits
[['+b', '-c']]
after unit clauses
[['+b', '-c']]
picking clause:  +b
new frame
[]
Result:  True
------------------- New Test: cnf4.txt ---------------------
new frame
[['+a', '+b', '+c', '-d'], ['+a', '-b']]
after handling pure lits
[['+a', '-b']]
after unit clauses
[['+a', '-b']]
picking clause:  +a
new frame
[]
Result:  True
```
