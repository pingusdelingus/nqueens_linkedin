import Square
import random
from copy import deepcopy


class Board():
    def __init__(self, colors_l, square_len, setup=True):
        print('running constructor')
        self.rep = [[0 for _ in range(square_len)] for _ in range(square_len)]
        self.squareLen = square_len
        self.colors = colors_l
        
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
        ans = ""
        for i in range(self.squareLen):
            for j in range(self.squareLen):
                curr = self.rep[i][j]
                ans  += f"{curr} | " 
            ans += "\n"
        return ans


def coin_flip():
    # Returns True if the random number is less than 0.5, False otherwise
    return random.random() < 0.5


def generateRandomBoardsOnRow(sidelen:int, numColors:int, colormap:list[int]):
    row = deepcopy(colormap)

    for i in range(len(row)):
        curr = row[i]
        if coin_flip:
            curr.setQueen()
        else:
            curr.setEmpty()
    return row





def generateRandomBoardsFromColorMap(numDesired:int , sidelen:int, numColors:int, colormap:list[list[int]])->list[Board]:
    lob = []

    assert(len(colormap[0]) == sidelen)
    assert(len(colormap) == sidelen)

    for _ in range(numDesired):
        curr = []
        for i in range(numDesired):
            curr.append(generateRandomBoardsOnRow(sidelen, numColors, colormap[i]))
        lob.append(Board(curr,sidelen, False))
    return lob

def generateRandomBoards(numDesired:int, sidelen:int, numColors:int )-> list[Board]:
    lob = []

    for _ in range(numDesired):
        curr = []
        for i in range(numDesired):
            curr.append(generateRandomRow(sidelen, numColors))
        lob.append(Board(curr,sidelen,False))
    return lob


def fitness(b:Board) -> int:
    # fitness priority
#   1. color confict
#   2. queen move conflict
    color_conflicts = 0
    queen_conflicts = 0


    queen_pos = []
    for i in range(b.squareLen):
        for j in range(b.squareLen):
            curr = b.rep[i][j]
            if curr.hasQueen == True:
                queen_pos.append((i,j, curr))


    numQueens = len(queen_pos)
    print(f"{numQueens} is num queens ")

    for i in range(numQueens):

        for j in range(i + 1, numQueens):

            r1, c1, color1 = queen_pos[i]
            r2, c2, color2 = queen_pos[j]

            # Conflict: Same Row
            if r1 == r2: queen_conflicts += 1
            
            # Conflict: Same Column
            if c1 == c2: queen_conflicts += 1

            # Conflict: Same Color Zone
            if color1 == color2: color_conflicts += 1

            # Conflict: Adjacency (Queens cannot touch each other)
            # This checks the 3x3 area around a queen
            if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
                queen_conflicts += 1
    

        # If the board doesn't have N queens, it's a major failure.
    expected_queens = b.squareLen
    if numQueens != expected_queens:
        queen_conflicts += abs(numQueens - expected_queens) * 10

    return (color_conflicts * 3 ) + queen_conflicts



def generateRandomRow(sidelen:int, numColors:int) -> list[int]:
    ans = []
    for i in range(sidelen):
        ans.append(Square.Square(random.randint(0,numColors - 1), random.randint(0,1) ))
    return ans

def areRepsEqual(a:Board, b:Board):
    for i in range(a.squareLen):
        for j in range(a.squareLen):
            if a.rep[i][j] != b.re[i][j]:
                return False
    return True




#test board
l = [
    [0,0,0,1,1,0,0],
    [0,2,2,1,0,0,0],
    [0,0,3,3,0,0,0],
    [0,0,3,0,0,0,0],
    [0,0,0,0,4,4,4],
    [0,0,0,0,0,0,5],
    [6,6,6,0,0,0,5]
]

def getUniqueColorCount(b:Board):
    lngths = []
    for i in range(b.squareLen):
        someset = set(b.rep[i])
        lngths.append(len(someset))
    return max(lngths)


def cmp_board(a:Board, b:Board):
    return a.fitness - b.fitness



def main():
    b = Board(l,len(l))
    numColors = 7
    print(b)

    print("unique colors : " + str(getUniqueColorCount(b)))
    print(f"fitness is {fitness(b)}")    

    list_of_randon_boards = generateRandomBoards(100, 7, numColors)


    list_of_random_boards_from_colormap = generateRandomBoardsFromColorMap(100, 7, numColors, l)
    print(list_of_random_boards_from_colormap[2])
    print(list_of_random_boards_from_colormap[3])
    print(list_of_random_boards_from_colormap[50])

    print("^ all should have same color layout")


if __name__ == "__main__":
    main()

