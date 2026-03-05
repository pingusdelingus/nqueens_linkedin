import Square
import random
from copy import deepcopy
import functools
from colorama import Fore, init, Style
init()

tf = [True,False]


class Board():
    def __init__(self, colors_l, square_len, setup=True):
#        print('running constructor')
        self.rep = [[0 for _ in range(square_len)] for _ in range(square_len)]
        self.squareLen = square_len
        self.colors = colors_l
        self.queen_conf = 0
        self.color_conf = 0
        
        if setup:
            self.setup(colors_l)
        else:
            self.rep = colors_l
            assert( isinstance(self.rep[0][0], Square.Square))
    

    def __lt__(self, other):
            if isinstance(other, Board):
                return self.fitness < other.fitness
            return NotImplemented # Optional: handle comparisons with other types

    def __gt__(self, other):
            if isinstance(other, Board):
                return self.fitness > other.fitness
            return NotImplemented # Optional: handle comparisons with other types

    def initFitness(self):
        return fitness(self)
    def getFitness(self):
        return self.fitness
        
    # Overload the == operator (equal to)
    def __eq__(self, other):
        """Checks if two Person objects are equal based on name and age."""
        if isinstance(other, Board):
            return self.fitness == other.fitness and self.squareLen == other.squareLen and areRepsEqual(self,other)
        return NotImplemented
        

    def setup(self, lol):
        print('runing setup')
        for i in range(self.squareLen):
            for j in range(self.squareLen):
                self.rep[i][j] = Square.Square(lol[i][j], False)
        self.fitness = self.initFitness()

    def __str__(self):
        ans = "********************************************\n"
        for i in range(self.squareLen):
            for j in range(self.squareLen):
                curr = self.rep[i][j]
                ans  += f"{curr} | " 
            ans += "\n"
        ans += "\n"
        ans += f"fitness ^ is {self.fitness}\n"
        ans += f"queen_conflicts: {self.queen_conf}\n"
        ans += f"color_conflicts: {self.color_conf}\n"
        ans += "********************************************\n"

        return ans


def coin_flip():
    # Returns True if the random number is less than 0.5, False otherwise
    return random.random() < 0.5


def generateRandomBoardsOnRow(sidelen:int, numColors:int, colormap:list[int]):
    """Generate a row with EXACTLY one queen at a random position"""
    ans = []
    queen_col = random.randint(0, sidelen - 1)  # Pick ONE column for the queen
    
    for i in range(sidelen):
        is_queen = (i == queen_col)
        curr = Square.Square(colormap[i], is_queen)
        if is_queen:
            curr.setQueen()
        else:
            curr.setEmpty()
        ans.append(curr)
    
    return ans




def generateRandomBoardsFromColorMap(numDesired:int , sidelen:int, numColors:int, colormap:list[list[int]])->list[Board]:
    lob = []

    assert(len(colormap[0]) == sidelen)
    assert(len(colormap) == sidelen)

    for _ in range(numDesired):
        curr = []
        for i in range(len(colormap)):
            curr.append(generateRandomBoardsOnRow(sidelen, numColors, colormap[i]))
        b = Board(curr,sidelen, False)
        b.fitness = fitness(b)
        lob.append(b)
    return lob

def generateRandomBoards(numDesired:int, sidelen:int, numColors:int )-> list[Board]:
    lob = []

    for _ in range(numDesired):
        curr = []
        for i in range(numDesired):
            curr.append(generateRandomRow(sidelen, numColors))
        lob.append(Board(curr,sidelen,False))
    return lob

def fitness(b: Board) -> int:
    color_conflicts = 0
    queen_conflicts = 0
    queen_pos = []

    # Collect all queen positions
    for i in range(b.squareLen):
        for j in range(b.squareLen):
            curr = b.rep[i][j]
            if curr.hasQueen(): 
                queen_pos.append((i, j, curr))

    numQueens = len(queen_pos)
    expected_queens = b.squareLen
    
    # MASSIVE penalty for wrong number of queens
    if numQueens != expected_queens:
        queen_conflicts += abs(numQueens - expected_queens) * 1000
    
    # Only check conflicts if we have queens to check
    for i in range(numQueens):
        for j in range(i + 1, numQueens):
            r1, c1, sq1 = queen_pos[i]
            r2, c2, sq2 = queen_pos[j]

            # Row conflict
            if r1 == r2: 
                queen_conflicts += 10
            
            # Column conflict
            if c1 == c2: 
                queen_conflicts += 10
            
            # Color conflict
            if sq1.color_int == sq2.color_int: 
                color_conflicts += 10
            
            # Adjacency conflict (touching)
            if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
                queen_conflicts += 10

    b.queen_conf = queen_conflicts
    b.color_conf = color_conflicts
    
    return color_conflicts + queen_conflicts



def generateRandomRow(sidelen:int, numColors:int) -> list[int]:
    ans = []
    for i in range(sidelen):
        ans.append(Square.Square(random.randint(0,numColors - 1), 0.10 < random.random() ))
    return ans

def areRepsEqual(a:Board, b:Board):
    for i in range(a.squareLen):
        for j in range(a.squareLen):
            if a.rep[i][j] != b.rep[i][j]:
                return False
    return True

Fore.ORANGE = '\x1b[38;5;208m'

int_to_color = [
        #0         #1        #3            #4        #5             #6                # 7         #8          #9           #10
      Fore.GREEN, Fore.RED,Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.LIGHTCYAN_EX, Fore.WHITE,Fore.BLACK, Fore.ORANGE,  Fore.RESET
]

#test board
l = [
    [4,4,4,4,4,4,4,4],
    [4,2,3,3,3,3,3,4],
    [4,2,3,3,3,3,0,4],
    [6,6,6 ,3,3,3,0,4],
    [1,6,3,3,3,0,0,0],
    [1,6,3,3,3,9,5,9],
    [1,1,1,1,9,9,5,9],
    [1,1,1,1,9,9,9,9]
]

m = [[row[i] for row in l] for i in range(len(l[0]))]
m = [[row[i] for row in m] for i in range(len(m[0]))]
m = [[row[i] for row in m] for i in range(len(m[0]))]
m = [[row[i] for row in m] for i in range(len(m[0]))]






def getUniqueColorCount(b:Board):
    lngths = []
    for i in range(b.squareLen):
        someset = set(b.rep[i])
        lngths.append(len(someset))
    return max(lngths)


def cmp_board(a:Board, b:Board):
    return a.fitness - b.fitness


def board_cmp(this:Board, that:Board):
    if this.fitness < that.fitness:
        return -1
    elif this.fitness > that.fitness:
        return 1
    else:
        return 0

def swapInPlace(rowA: list, rowB: list, snip: int):
    rowA[snip:], rowB[snip:] = rowB[snip:], rowA[snip:]


def crossover(this:Board, that:Board):
    split_point = random.randint(0, this.squareLen - 1)

    # Swap entire row references from the split point to the end
    # This ensures if Parent A had 1 queen per row, the child still does.
    this.rep[split_point:], that.rep[split_point:] = \
        that.rep[split_point:], this.rep[split_point:]
    
    # Recalculate fitness for both
    this.fitness = this.initFitness()
    that.fitness = that.initFitness()
    return





def crossover_population(sorted_population: list[Board]):
    """FIXED: Proper elitism and child retention"""
    pop_size = len(sorted_population)
    elite_size = pop_size // 4  # Keep top 25%
    
    # Keep elite unchanged
    new_population = sorted_population[:elite_size]
    
    # Generate offspring to fill the rest
    while len(new_population) < pop_size:
        # Select two parents from elite
        parent1 = random.choice(sorted_population[:elite_size])
        parent2 = random.choice(sorted_population[:elite_size])
        
        child1, child2 = smart_crossover(parent1, parent2)
        child1.fitness = child1.initFitness()
        child2.fitness = child2.initFitness()
        
        new_population.append(child1)
        if len(new_population) < pop_size:
            new_population.append(child2)
    
    # Replace old population
    sorted_population[:] = new_population



def mutate(board:Board, mutation_rate = 0.1):
    if random.random() < mutation_rate:

        row_idx = random.randint(0, board.squareLen - 1)
        row = board.rep[row_idx]
        
        # Find where the current queen is and remove it
        for sq in row:
            sq.setEmpty()
            sq.hasQ = False
            
        # Place it in a new random column in the same row
        new_col = random.randint(0, board.squareLen - 1)
        row[new_col].setQueen()
        row[new_col].hasQ = True
        
        board.fitness = board.initFitness()

NUM_MUTATION = 100
def do_mutate(population, num_mutations=None):
    """Mutate a percentage of the population"""
    if num_mutations is None:
        num_mutations = len(population) // 2  # Mutate 50%
    
    # Don't mutate the very best solution
    for _ in range(num_mutations):
        idx = random.randint(1, len(population) - 1)
        smart_mutate(population[idx], rate=0.5)



def smart_crossover(parentA: Board, parentB: Board):
    # 1. Create children as deep copies to avoid modifying parents directly
    childA_rep = deepcopy(parentA.rep)
    childB_rep = deepcopy(parentB.rep)
    
    split = random.randint(1, parentA.squareLen - 2)
    
    # 2. Swap the segments
    childA_rep[split:], childB_rep[split:] = childB_rep[split:], childA_rep[split:]
    
    # 3. HEURISTIC REPAIR: 
    # If a child now has 2 queens in one color, move one of them 
    # to a row/column in that same row that belongs to a missing color.
    # (This is complex to code but makes the GA 10x faster)
    
    return Board(childA_rep, parentA.squareLen, setup=False), Board(childB_rep, parentA.squareLen, setup=False)

def check_spot_conflicts(board: Board, row_idx: int, col_idx: int) -> int:
    """Calculate conflicts for a queen at (row_idx, col_idx)"""
    conflicts = 0
    target_color = board.rep[row_idx][col_idx].color_int

    for r in range(board.squareLen):
        if r == row_idx:  # Skip the current row
            continue
            
        for c in range(board.squareLen):
            sq = board.rep[r][c]
            if sq.hasQueen():
                # Column conflict
                if c == col_idx:
                    conflicts += 10
                
                # Color zone conflict
                if sq.color_int == target_color:
                    conflicts += 10
                
                # Adjacency conflict
                if abs(r - row_idx) <= 1 and abs(c - col_idx) <= 1:
                    conflicts += 10
                    
    return conflicts






def set_queen_at(board: Board, row_idx: int, best_col: int):
    # You must clear the row first!
    for c in range(board.squareLen):
        board.rep[row_idx][c].setEmpty()
        board.rep[row_idx][c].hasQ = False
    
    # Now set the new one
    board.rep[row_idx][best_col].setQueen()
    board.rep[row_idx][best_col].hasQ = True


def smart_mutate(board: Board, rate=0.5):
    if random.random() > rate: 
        return
    
    row_idx = random.randint(0, board.squareLen - 1)
    
    # Find column with minimum conflicts
    best_col = 0
    min_conflicts = float('inf')
    
    for c in range(board.squareLen):
        conf = check_spot_conflicts(board, row_idx, c)
        if conf < min_conflicts:
            min_conflicts = conf
            best_col = c
    
    # Clear all queens in this row
    for c in range(board.squareLen):
        board.rep[row_idx][c].setEmpty()
        board.rep[row_idx][c].hasQ = False
    
    # Set queen at best position
    board.rep[row_idx][best_col].setQueen()
    board.rep[row_idx][best_col].hasQ = True
    
    # IMPORTANT: Actually update the fitness!
    board.fitness = fitness(board)





def main():
    b = Board(m, len(m))
    print(b)

    # Generate initial population
    list_of_random_boards = generateRandomBoardsFromColorMap(
        500,  # Smaller population for speed
        len(m[0]), 
        getUniqueColorCount(b), 
        m
    )

    generations = 5000
    best_ever = float('inf')
    stagnant_count = 0
    
    while generations > 0:
        # Sort population
        list_of_random_boards.sort(key=lambda x: x.fitness)
        
        current_best = list_of_random_boards[0].fitness
        
        # Check for solution
        if current_best == 0:
            print(f"SOLUTION FOUND at generation {5000 - generations}!")
            print(list_of_random_boards[0])
            break
        
        # Track stagnation
        if current_best >= best_ever:
            stagnant_count += 1
        else:
            stagnant_count = 0
            best_ever = current_best
        
        # Increase mutation if stuck
        if stagnant_count > 50:
            print(f"⚠ Stuck at fitness {current_best}, increasing mutation...")
            do_mutate(list_of_random_boards, len(list_of_random_boards))
            stagnant_count = 0
        
        print(f"Gen {5000-generations}: Best fitness = {current_best} "
                f"(Q:{list_of_random_boards[0].queen_conf} "
                f"C:{list_of_random_boards[0].color_conf})")
        print(list_of_random_boards[0])

        print()
        print()

        print(f"Gen {5000-generations}: WORST fitness = {list_of_random_boards[-1].fitness} "
                f"(Q:{list_of_random_boards[-1].queen_conf} "
                f"C:{list_of_random_boards[-1].color_conf})")

        #print(list_of_random_boards[-1])

        # Evolve
        crossover_population(list_of_random_boards)
        do_mutate(list_of_random_boards)
        
        generations -= 1
    
    if generations == 0:
        print("No solution found. Best result:")
        print(list_of_random_boards[0])



if __name__ == "__main__":
    main()

