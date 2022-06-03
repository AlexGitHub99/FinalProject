import random
import time


WIDTH = 10
HEIGHT = 15

FLAG_CHAR = "◘"
FULL_CHAR = "■"
MINE_CHAR = "*"
EMPTY_CHAR = " "

def generate_mines(width, height):
    mines = []
    for x in range(width):
        mines.append([])
        for y in range(height):
            rand = random.randrange(6)
            mines[x].append(True if rand == 0 else False)
    return mines

def generate_board(width, height):
    board = []
    for x in range(width):
        board.append([])
        for y in range(height):
            board[x].append(FULL_CHAR)
    return board

#debug only
def print_mines(mines):
    for y in range(len(mines[0])):
        for x in range(len(mines)):
            print(MINE_CHAR if mines[x][y] else EMPTY_CHAR, end="")
        print()

def print_board(board):
    dash_string = "  -----"
    for i in range(len(board)):
        dash_string += "--"
    print(dash_string)
    string = " |     "
    for i in range(len(board)):
        string += chr(ord("a") + i) + " "
    print(string + "|")
    string = " |     "
    for i in range(len(board)):
        string += "--"
    print(string + "|")
    for y in range(len(board[0])):
        print(" |", end="")
        if(y < 9): 
            #print additional space for single digit numbers
            print(" ", end = "")
        print(str(y + 1) + " | ", end="")
        
        for x in range(len(board)):
            print(board[x][y], end=" ")
        print("|")
    print(dash_string)

def check_win(board, mines):
    for x in range(len(board)):
        for y in range(len(board[0])):
            not_empty = board[x][y] == FULL_CHAR or board[x][y] == FLAG_CHAR or board[x][y] == MINE_CHAR
            has_mine = mines[x][y]
            if(not_empty and not has_mine):
                return False
    return True

#This function calculates the amount of mines in a 3x3 area
def calc_mines(mines, x, y):
    mine_count = 0
    for xi in range(x - 1, x + 2):
        for yi in range(y - 1, y + 2):
            #not middle square
            not_middle_square = not(xi == x and yi == y)
            on_board = 0 <= xi < len(mines) and 0 <= yi < len(mines[0])
            if(on_board and not_middle_square):
                if(mines[xi][yi]):
                    mine_count += 1

    return mine_count
        

#This function recursively clears out space until it reaches mines and also adds numbers saying how many mines are nearby (blank if zero)
def hit_zero(board, mines, x, y):
    mine_count = calc_mines(mines, x, y)
    if(mine_count == 0):
        board[x][y] = EMPTY_CHAR
        for xi in range(x - 1, x + 2):
            for yi in range(y - 1, y + 2):
                on_board = 0 <= xi < len(mines) and 0 <= yi < len(mines[0])
                if(not on_board):
                    continue
                not_middle_square = not(xi == x and yi == y)
                not_empty = board[xi][yi] == FULL_CHAR or board[xi][yi] == FLAG_CHAR
                if(not_middle_square and not_empty):
                    hit_zero(board, mines, xi, yi)
    else:
        board[x][y] = str(mine_count)

def reveal_mines(board, mines):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if(mines[x][y]):
                board[x][y] = MINE_CHAR
            else:
                board[x][y] = EMPTY_CHAR

mines = generate_mines(WIDTH, HEIGHT)
board = generate_board(WIDTH, HEIGHT)

#debug only
#print_mines(mines)
#print board
print_board(board)

#Start game
#Start monitoring time
start_time = time.monotonic()

message = ""
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
                message = "You lost"
                playing = False
            else:
                mine_count = calc_mines(mines, x, y)
                if(mine_count == 0):
                    hit_zero(board, mines, x, y)
                else:
                    board[x][y] = str(mine_count)
                print_board(board)
                if(check_win(board, mines)):
                    message = "You won"
                    playing = False;
            print(message + ".")
        else:
            print("Can't mine an empty square")
    elif(move == "f"):
        if(board[x][y] == FULL_CHAR):
            board[x][y] = FLAG_CHAR
            print_board(board)
        else:
            print("Can't place a flag on an empty square")

    print()

print("Mines:")
reveal_mines(board, mines)
print_board(board)
print(f"{message} in {round(time.monotonic() - start_time, 2)} seconds")