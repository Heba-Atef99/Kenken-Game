
import csp
# @ stderr: reporting errors
from sys import stderr
from itertools import product, permutations
from functools import reduce
from random import random, shuffle, randint, choice
from time import time

def adjacent(xy1, xy2):
    """
    Checks whether two positions represented in 2D coordinates are adjacent
    """
    x1, y1 = xy1
    x2, y2 = xy2

    dx, dy = x1 - x2, y1 - y2

    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

def operation(operator):
    """
    A function determines the operation corresponding to the operator 
    """
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None

def generate(size):
    """
    Generate a random kenken puzzle of the given size
      * Initially create a latin square of size 'size' and elements the values [1...size]
      * Shuffle the board by rows and columns in order to get a somewhat random
        board that still satisfies the different row-col constraint of kenken
      * Initialize the 'uncaged' set with all cell coordinates
      * Proceed in creating cliques:
        * Randomly choose a clique size in the range [1..4]
        * Set the first cell in the 'uncaged' set in row major order as
          the root cell of the clique and remove it from the 'uncaged' set
        * Randomly visit at most 'clique-size' 'uncaged' adjacent cells
          in random directions while adding them to the current clique
          and removing them from the 'uncaged' cells
        * The size of the resulting clique is:
          * == 1:
            there is no operation to be performed and the target of the clique
            is equal to the only element of the clique
          * == 2:
            * if the two elements of the clique can be divided without a remainder
              then the operation is set to division and the target is the quotient
            * otherwise, the operation is set to subtraction and the target is the
              difference of the elements
          * >  2:
           randomly choose an operation between addition and multiplication.
            The target of the operation is the result of applying the decided
            operation on all the elements of the clique
        * Continue until the 'uncaged' set is empty i.e. there is no cell belonging
          to no clique
    """

    board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]

    for _ in range(size):
        shuffle(board)

    for c1 in range(size):
        for c2 in range(size):
            if random() > 0.5:
                for r in range(size):
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    board = {(j + 1, i + 1): board[i][j] for i in range(size) for j in range(size)}

    uncaged = sorted(board.keys(), key=lambda var: var[1])

    cliques = []
    while uncaged:

        cliques.append([])

        csize = randint(1, 4)

        cell = uncaged[0]

        uncaged.remove(cell)

        cliques[-1].append(cell)

        for _ in range(csize - 1):

            adjs = [other for other in uncaged if adjacent(cell, other)]

            cell = choice(adjs) if adjs else None

            if not cell:
                break

            uncaged.remove(cell)
            
            cliques[-1].append(cell)
            
        csize = len(cliques[-1])
        
        if csize == 1:
            cell = cliques[-1][0]
            cliques[-1] = ((cell, ), '.', board[cell])
            continue
        elif csize == 2:
            fst, snd = cliques[-1][0], cliques[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                operator = "/" 
            else:
                operator = "-" 
        else:
            operator = choice("+*")

        target = reduce(operation(operator), [board[cell] for cell in cliques[-1]])

        cliques[-1] = (tuple(cliques[-1]), operator, int(target))

    return size, cliques

def validate(size, cliques):
    """
    Validate the integrity of the input as a kenken board
      * For each of the cliques:
        * Remove duplicate members of the clique at hand
        * Check whether the specified operator is acceptable or not
        * Check if any of the members of the clique are out of bounds
        * Check if any member of the clique is mentioned in any other clique
      * Check if the given cliques cover the whole board or not
    """
    IsoutOfBounds = lambda xy: xy[0] < 1 or xy[0] > size or xy[1] < 1 or xy[1] > size

    mentioned = set()
    for i in range(len(cliques)):
        members, operator, target = cliques[i]

        cliques[i] = (tuple(set(members)), operator, target)

        members, operator, target = cliques[i]

        if operator not in "+-*/.":
            print("Operation", operator, "of clique", cliques[i], "is unacceptable", file=stderr)
            exit(1)

        problem = list(filter(IsoutOfBounds, members))
        if problem: #check if all members of clique are in bounds of the board
            print("Members", problem, "of clique", cliques[i], "are out of bounds of the board", file=stderr)
            exit(2)

        problem = mentioned.intersection(set(members))
        if problem: #check that there is not a member that's in 2 different cliques
            print("Members", problem, "of clique", cliques[i], "are in more than one clique", file=stderr)
            exit(3)

        mentioned.update(set(members)) #add members of the validated clique

    indexes = range(1, size + 1)

    problem = set([(x, y) for y in indexes for x in indexes]).difference(mentioned)

    if problem: #check that all positions of the board are included in the cliques
        print("Positions", problem, "were not mentioned in any clique", file=stderr)
        exit(4)

def RowXorCol(xy1, xy2):
    """
    Evaluates to true if the given positions are in the same row / column
    but are in different columns / rows
    """
    return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])

def conflicting(A, a, B, b):
    """
    Evaluates to true if:
      * there exists mA so that ma is a member of A and
      * there exists mb so that mb is a member of B and
      * RowXorCol(mA, mB) evaluates to true and
      * the value of mA in 'assignment' a is equal to
        the value of mb in 'assignment' b
    """
    for i in range(len(A)):
        for j in range(len(B)):
            mA = A[i]
            mB = B[j]

            ma = a[i]
            mb = b[j]
            if RowXorCol(mA, mB) and ma == mb:
                return True

    return False

def satisfies(values, operation, target):
    """
    Evaluates to true if the result of applying the operation
    on a permutation of the given values is equal to the specified target
    """
    for p in permutations(values):
        if reduce(operation, p) == target:
            return True

    return False

def gdomains(size, cliques):
    """
    @ https://docs.python.org/2/library/itertools.html
    @ product('ABCD', repeat=2) = [AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD]

    For every clique in cliques:
        * Initialize the domain of each variable to contain every product
        of the set [1...board-size] that are of length 'clique-size'.
        For example:

            board-size = 3 and clique-size = 2

            products = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

        * Discard any value (assignment of the members of the clique) that:
        * is resulting in the members of the clique 'conflicting' with each other
        * does not 'satisfy' the given operation
    """
    domains = {}
    for clique in cliques:
        members, operator, target = clique

        domains[members] = list(product(range(1, size + 1), repeat=len(members))) #all combinations possible for members


        qualifies = lambda values: not conflicting(members, values, members, values) and satisfies(values, operation(operator), target)
        #filter from all combinations just the combinations that satisfy target
        domains[members] = list(filter(qualifies, domains[members]))

    return domains

def gneighbors(cliques):
    """
    Determine the neighbors of each variable for the given puzzle
        For every clique in cliques
        * Initialize its neighborhood as empty
        * For every clique in cliques other than the clique at hand,
            if they are probable to 'conflict' they are considered neighbors
    """
    neighbors = {}
    for members, _, _ in cliques:
        neighbors[members] = []

    for A, _, _ in cliques:
        for B, _, _ in cliques:
            if A != B and B not in neighbors[A]:
                if conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                    neighbors[A].append(B)
                    neighbors[B].append(A)

    return neighbors


class Kenken(csp.CSP):

    def __init__(self, size, cliques):
        validate(size, cliques)

        variables = [members for members, _, _ in cliques]

        domains = gdomains(size, cliques)

        neighbors = gneighbors(cliques)

        csp.CSP.__init__(self, variables, domains, neighbors, self.constraint)

        self.size = size

        # Used in benchmarking
        self.checks = 0

        # Used in displaying
        self.padding = 0

        self.meta = {}
        for members, operator, target in cliques:
            self.meta[members] = (operator, target)
            self.padding = max(self.padding, len(str(target)))        


    def constraint(self, A, a, B, b):
        """
        Any two variables satisfy the constraint if they are the same
        or they are not conflicting 
        """
        self.checks += 1

        return A == B or not conflicting(A, a, B, b)

    
if __name__ == "__main__":


    # dt = time()
    # size, cliques = generate(3)
    # print(cliques)
    #
    # ken = Kenken(size, cliques)
    #
    # assignment = csp.backtracking_search(ken)
    # dt = time() - dt
    #
    # print(dt)
    dt = time()
    for i in range(100):
        size, cliques = generate(3)
        ken = Kenken(size, cliques)
        assignment = csp.backtracking_search(ken, inference=csp.mac)
        ken.display(assignment)
    dt = time() - dt
    print("time for 100 boards in backtracking search with arc consistency= ", dt, "second")
