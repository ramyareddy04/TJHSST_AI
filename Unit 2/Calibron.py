from heapq import heappush, heappop, heapify
import sys

puzzle = sys.argv[1].split()
puzzle_height = int(puzzle[0]) # rows
puzzle_width = int(puzzle[1]) #cols

class Block:
    def __init__(self, currX, currY, width, height):
        self.X = currX
        self.Y = currY
        self.w = width
        self.h = height

    def setX(self, newX):
        self.X = newX

    def setY(self, newY):
        self.Y = newY

def goal_test(used):
    if len(used)==0: return False
    if used == [None]: return False
    return sum([i[2]*i[3] for i in used])==puzzle_height*puzzle_width

def assign(used, block):
    if len(used)==0: temp = (0,0,0,0)
    else: temp = used[-1]
    
    #if temp.X + temp.W + block.w < puzzle_Width and temp.Y + block.h < puzzle_height:
    #    return Block(temp.X+temp.w+1, temp.Y, block.w, block.h)
    #elif temp.X + temp.w + block.h < puzzle_width and temp.Y + block.w < puzzle_height:
    #    return Block(temp.X+temp.w+1, temp.Y, block.h, block.w)
    #elif temp.X + block.w < puzzle_Width and temp.Y + temp.h + block.h < puzzle_height:
    #    return Block(temp.X, temp.Y+temp.h+1, block.w, block.h)
    #elif temp.X + block.h < puzzle_Width and temp.Y + temp.h + block.w < puzzle_height:
    #    return Block(temp.X, temp.Y+temp.h+1, block.h, block.w)
    #else: return None
    if temp[0] + temp[2] + block[2] < puzzle_width and temp[1] + block[3] < puzzle_height:
        return Block(temp[0]+temp[2]+1, temp[1], block[2], block[3])
    elif temp[0] + temp[2] + block[3] < puzzle_width and temp[1] + block[2] < puzzle_height:
        return Block(temp[0]+temp[2]+1, temp[1], block[3], block[2])
    elif temp[0] + block[2] < puzzle_width and temp[1] + temp[3] + block[3] < puzzle_height:
        return Block(temp[0], temp[1]+temp[3]+1, block[2], block[3])
    elif temp[0] + block[3] < puzzle_width and temp[1] + temp[3] + block[2] < puzzle_height:
        return Block(temp[0], temp[1]+temp[3]+1, block[3], block[2])
    else: return None


def backtrack(used, remaining):
    if goal_test(used): 
        for i in used:
            print(i.X, i.Y, i.w, i.h)
        return used

    for block in remaining:
        print(block)
        newState = assign(used, block)
        temp = remaining.copy()
        temp.remove(block)
        if Block(-1,-1, block[3], block[2]) in remaining: temp.remove(Block(-1,-1, block[3], block[2]))
        result = backtrack(used+[newState], temp)
        if result is not None:
            return result

    return None

# You are given code to read in a puzzle from the command line.  The puzzle should be a single input argument IN QUOTES.
# A puzzle looks like this: "56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
rectangles = [(int(temp.split("x")[0]), int(temp.split("x")[1])) for temp in puzzle[2:]]

littleRect = sum([i[0]*i[1] for i in rectangles])
if puzzle_height*puzzle_width != littleRect:
    print("Containing rectangle incorrectly sized.")
else:
    blocks = [Block(-1,-1, dims[0], dims[1]) for dims in rectangles] + [Block(-1,-1, dims[1], dims[0]) for dims in rectangles]
    pieces = []
    for block in blocks: heappush(pieces, (block.X, block.Y, block.w, block.h))
    backtrack([], pieces)
    print(len(blocks))
#
# Then try to solve the puzzle.
# If the puzzle is unsolvable, output precisely this - "No solution."
#
# If the puzzle is solved, output ONE line for EACH rectangle in the following format:
# row column height width
# where "row" and "column" refer to the rectangle's top left corner.
#
# For example, a line that says:
# 3 4 2 1
# would be a rectangle whose top left corner is in row 3, column 4, with a height of 2 and a width of 1.
# Note that this is NOT the same as 3 4 1 2 would be.  The orientation of the rectangle is important.
#
# Your code should output exactly one line (one print statement) per rectangle and NOTHING ELSE.
# If you don't follow this convention exactly, my grader will fail.