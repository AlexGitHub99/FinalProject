import random
import time


WIDTH = 2
HEIGHT = 2

FLAG_CHAR = "P"
FULL_CHAR = "■"
MINE_CHAR = "*"
EMPTY_CHAR = " "

def generate_mines(width, height):
    board = []
    for x in range(width):
        board.append([])
        for y in range(height):
            rand = random.randrange(5)
            board[x].append(True if rand == 0 else False)
    return board

def generate_board(width, height):
    board = []
    for x in range(width):
        board.append([])
        for y in range(height):
            board[x].append(FULL_CHAR)
    return board

#debug only
def print_mines(board):
    for y in range(len(board[0])):
        for x in range(len(board)):
            print(MINE_CHAR if board[x][y] else EMPTY_CHAR, end="")
        print()

def print_board(board):
    dash_string = "  ---"
    for i in range(len(board)):
        dash_string += "--"
    print(dash_string)
    string = " |   "
    for i in range(len(board)):
        string += chr(ord("a") + i) + " "
    print(string)
    for y in range(len(board[0])):
        print(" |", end="")
        if(y < 10): 
            #print additional space for single digit numbers
            print(" ", end = "")
        print(str(y + 1) + " ", end="")
        
        for x in range(len(board)):
            print(board[x][y], end=" ")
        print()
    print(dash_string)

def check_win(board, mines):
    for x in range(len(board)):
        for y in range(len(board[0])):
            not_empty = board[x][y] == FULL_CHAR or board[x][y] == FLAG_CHAR or board[x][y] == MINE_CHAR
            has_mine = mines[x][y]
            if(not_empty and not has_mine):
                return False
    return True

def hit_zero(board, mines, x, y):



mines = generate_mines(WIDTH, HEIGHT)
board = generate_board(WIDTH, HEIGHT)

print_board(board)

#Start game
#Start monitoring time
start_time = time.monotonic()

playing = True
while(playing):
    print()
    move = input("Enter d for dig or f for flag: ")
    loc = input("Enter coordinates in the form (letter)(number): ")
    letter = loc[0]
    x = int(ord(letter) - ord('a'))
    y = int(loc[1:]) - 1
    message = ""
    if(move == "d"):
        if(board[x][y] == FULL_CHAR):
            if(mines[x][y] == True):
                board[x][y] = MINE_CHAR
                print_board(board)
                message = "You Lost."
                playing = False
            else:
                board[x][y] = EMPTY_CHAR
                print_board(board)
                if(check_win(board, mines)):
                    message = "You Won!"
                    playing = False;
        else:
            print("Can't mine an empty square")
    elif(move == "f"):
        if(board[x][y] == FULL_CHAR):
            board[x][y] = FLAG_CHAR
            print_board(board)
        else:
            print("Can't place a flag on an empty square")

    print()

print(f"Total time: {round(time.monotonic() - start_time, 2)} seconds")