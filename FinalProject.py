#######################################################################   
# Program Filename: FinalProject.py
# Author: Alex King
# Date: 6/3/22
# Description: A console based minesweeper game
# Input: a command to dig or flag, and an alphanumeric coordinate
# Output: Interactive minesweeper game represented by an ascii map
####################################################################### 

import random
import time

#Constants
WIDTH = 10
HEIGHT = 15
#make this larger for an easier game
EMPTY_TO_BOMB_RATIO = 10
FLAG_CHAR = "◘"
FULL_CHAR = "■"
MINE_CHAR = "*"
EMPTY_CHAR = " "

#######################################################################  
# Function: check_move
# Description: checks if a string is the letter d or f
# Parameters: text
# Return values: True or False
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################  
def check_move(text):
    if(text == "d" or text == "f"):
        return True
    return False

#######################################################################  
# Function: check_loc
# Description: checks if a string is in the format (letter)(number), 
# for example, b12
# Parameters: text
# Return values: True/False
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################  
def check_loc(text):
    if(len(text) == 0):
        return False
    if(ord("a") <= ord(text[0]) <= ord("z") and text[1:].isdigit()):
        return True
    return False

#######################################################################  
# Function: generate_mines
# Description: generates a random 2d array of boolean values, with True
# values representing mines
# Parameters: width, height
# Return values: mines
# Pre-Conditions: None
# Post-Conditions: None
#######################################################################  
def generate_mines(width, height):
    mines = []
    for x in range(width):
        mines.append([])
        for y in range(height):
            rand = random.randrange(EMPTY_TO_BOMB_RATIO)
            mines[x].append(True if rand == 0 else False)
    return mines

#######################################################################  
# Function: generate_board
# Description: generates a 2d array of characters determined by FULL_CHAR
# Parameters: width, height
# Return values: board
# Pre-Conditions:  FULL_CHAR is defined
# Post-Conditions: None
#######################################################################  
def generate_board(width, height):
    board = []
    for x in range(width):
        board.append([])
        for y in range(height):
            board[x].append(FULL_CHAR)
    return board

#######################################################################  
# Function: print_mines
# Description: A debug function not used in the final program. This prints
# a crude printout of the mine locations without editing the main board
# Parameters:   mines
# Return values:  none
# Pre-Conditions:  none
# Post-Conditions:   a printed out map of mine locations
#######################################################################  
def print_mines(mines):
    for y in range(len(mines[0])):
        for x in range(len(mines)):
            print(MINE_CHAR if mines[x][y] else EMPTY_CHAR, end="")
        print()

#######################################################################  
# Function:   print_board
# Description:  prints the board to console, with pre defined constants
# representing full blocks, empty blocks, flags, and mines.
# Parameters:   board
# Return values:  none
# Pre-Conditions:  none
# Post-Conditions:   The board printed to console
#######################################################################  
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

#######################################################################  
# Function:   check_win
# Description:  checks if every empty block has been dug
# Parameters:   board, mines
# Return values:  True / False
# Pre-Conditions:  properly generated board and mines arrays
# Post-Conditions:   none
#######################################################################  
def check_win(board, mines):
    for x in range(len(board)):
        for y in range(len(board[0])):
            not_empty = board[x][y] == FULL_CHAR or board[x][y] == FLAG_CHAR or board[x][y] == MINE_CHAR
            has_mine = mines[x][y]
            if(not_empty and not has_mine):
                return False
    return True

#######################################################################  
# Function:   calc_mines
# Description:  calculates the amount of mines in 3x3 area around a coord
# Parameters:   mines, x, y
# Return values:  mine_count
# Pre-Conditions:  none
# Post-Conditions:   none
#######################################################################  
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
        
#######################################################################  
# Function:   hit_zero
# Description:  This function recursively clears out space until it 
# reaches mines and also adds numbers saying how many mines are nearby (blank if zero)
# Parameters:   board, mines, x, y
# Return values:  none
# Pre-Conditions:   x and y are an empty block
# Post-Conditions:   cleared out area of space with mine counts on the edges
#######################################################################  
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

#######################################################################  
# Function:   reveal_mines
# Description:  edits main board array to leave only mines and empty space
# Parameters:   board, mines
# Return values:  none
# Pre-Conditions:  board with blocks, empty space, flags, and/or mines
# Post-Conditions:   board with only empty space and mines
#######################################################################  
def reveal_mines(board, mines):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if(mines[x][y]):
                board[x][y] = MINE_CHAR
            else:
                board[x][y] = EMPTY_CHAR

#generate mines and board
mines = generate_mines(WIDTH, HEIGHT)
board = generate_board(WIDTH, HEIGHT)

#Start game
print("""
=================================================================
      __  __ _                                            
     |  \/  (_)_ _  ___   ____ __ _____ ___ _ __  ___ _ _ 
     | |\/| | | ' \/ -_) (_-< V  V / -_) -_) '_ \/ -_) '_|
     |_|  |_|_|_||_\___| /__/\_/\_/\___\___| .__/\___|_|  
                                           |_|             
=================================================================
""")

#debug only
#print_mines(mines)
#print board
print_board(board)

#Start monitoring time
start_time = time.monotonic()

message = ""
playing = True
while(playing):
    print()
    move = input("Enter d for dig or f for flag: ")
    while(not check_move(move)):
        move = input("Incorrect format. Enter d for dig or f for flag (lowercase): ")
    loc = input("Enter coordinates in the form (letter)(number): ")
    while(not check_loc(loc)):
        loc = input("Incorrect format. Enter coordinates in the form (letter)(number). For example, b12: ")
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
                    #clear space around x y
                    hit_zero(board, mines, x, y)
                else:
                    board[x][y] = str(mine_count)
                print_board(board)
                if(check_win(board, mines)):
                    message = "You won"
                    playing = False;
            print(message)
        elif(board[x][y] == FLAG_CHAR):
            print("Can't mine a flagged spot. Flag again to unflag.")
        else:
            print("Can't mine an empty square")
    elif(move == "f"):
        if(board[x][y] == FULL_CHAR):
            board[x][y] = FLAG_CHAR
            print_board(board)
        elif(board[x][y] == FLAG_CHAR):
            board[x][y] = FULL_CHAR
            print_board(board)
        else:
            print("Can't place a flag on an empty square")

    print()

print("Mines:")
reveal_mines(board, mines)
print_board(board)
print(f"{message} in {round(time.monotonic() - start_time, 2)} seconds")