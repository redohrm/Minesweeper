#!/usr/bin/env python3

# Programmer: Ruth Dohrmann
# Date: 7/17/2023
# Description: This program allows someone to play a Minesweeper game in the terminal. The program 
# implements a 9x9 board with 10 randomly placed mines. After winning or losing, the program displays
# the entire board uncovered and writes out, to a separate text file, the full board uncovered, and
# the list of moves made by the user.
import random

def main():

    dimension = 9
    # set up 2 2d lists, one for containing the actual values hidden in the cells
    # and the other for the user to view
    board = [[0 for i in range(dimension)] for j in range(dimension)]
    board_for_display = [['+' for i in range(dimension)] for j in range(dimension)]

    num_of_mines = 10
    count = 0
    # set up mines
    while count < num_of_mines:
        x = random.randint(0, (dimension - 1))
        y = random.randint(0, (dimension - 1))
        # check for if the cell already has a mine
        if board[x][y] != '*':
            board[x][y] = '*'
            count += 1

    set_up_board(board, dimension)
    display_board(board_for_display, dimension)
    play_game(board, board_for_display, dimension)
    
# Update list items adjacent to mines
def set_up_board(board, dim):
    for i in range(dim):
        for j in range(dim):
            if board[i][j] == '*':
                # list of coordinates for adjacent items
                adjacent = [(i-1,j),(i-1,j+1),(i-1,j-1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]
                # iterate through the tuples in the list 'adjacent'
                for x in adjacent:
                    # if the cell falls within the board and does not also contain a mine,
                    # add 1 to its value
                    if (0 <= x[0] < dim) and (0 <= x[1] < dim) and (board[x[0]][x[1]] != '*'):
                        board[x[0]][x[1]] += 1
            

# Display the board with coordinates provided on the top
# and left side of the cells
def display_board(board, dim):
    print("   0 1 2 3 4 5 6 7 8")
    print("--------------------")

    count = 0
    for i in range(dim):
        print(f"{count}|", end=' ') 
        # output cell
        for j in range(dim):
            print(f"{board[i][j]}", end=' ')
        count += 1
        print()

# This function requests the player's choice and continues to ask for their choice of coordinates
# until they select a mine or only 10 cells are left uncovered
def play_game(board, board_for_display, dim):
    over = False
    uncovered_cells = 0
    max_uncovered_cells = dim * dim - 10
    # open file MinesweeperRecord.txt
    file = open("MinesweeperRecord.txt", "w")
    file.write("Record of Minesweeper moves and final board.\n")

    # loops until the user loses or wins
    while (not over) and (uncovered_cells < max_uncovered_cells):
        print("Enter x and y to dig")
        x = int(input("X: "))
        y = int(input("Y: "))
        # check input
        while not(0 <= x < dim) or not(0 <= y < dim):
            print("Invalid point. Please reenter your desired coordinates")
            x = int(input("X: "))
            y = int(input("Y: "))
        # Write move to file
        file.write(f"Dig at ({x}, {y})\n")

        # if the cell is a bomb, the game is over
        if board[y][x] == '*':
            display_board(board, dim)
            print("You lost!")
            over = True
        # if the cell borders a mine, uncover the cell
        elif (board[y][x] > 0) and (board_for_display[y][x] == '+'):
            board_for_display[y][x] = board[y][x]
            display_board(board_for_display, dim)
            uncovered_cells += 1
        # if the cell is blank, call update_board to uncover all adjacent
        # blank cells recursively, stopping at their adjacent cells with numerical values
        # greater than 0
        elif (board_for_display[y][x] == '+'):
            board_for_display[y][x] = ' '
            uncovered_cells += 1
            uncovered_cells = update_board(board, board_for_display, dim, uncovered_cells, y, x)
            display_board(board_for_display, dim)
        else:
            print("The cell at those coordinates is already open")

    # Display congratulations message and uncovered board if the user won
    if uncovered_cells == max_uncovered_cells:
        display_board(board, dim)
        print("Congratulations! You won!")
    
    save_board(board, dim, file)
    file.close()

# Recursive function for if the user selects a blank cell. Each blank cell adjacent to the original
# blank cell will recursively call this function.
def update_board(board, board_for_display, dim, count, y, x):
    # list of coordinates for adjacent items
    adjacent = [(y-1,x),(y-1,x+1),(y-1,x-1),(y,x-1),(y,x+1),(y+1,x-1),(y+1,x),(y+1,x+1)]

    # iterate through the tuples in the list 'adjacent'
    for i in adjacent:
        # check if the cell is in bounds and is not already uncovered
        if (0 <= i[0] < dim) and (0 <= i[1] < dim) and board_for_display[i[0]][i[1]] == '+':
            # if the value of the cell is 0, display the cell as a blank and recusively call this
            # function with the coordinates of this new cell
            if board[i[0]][i[1]] == 0:
                board_for_display[i[0]][i[1]] = ' '
                count += 1
                count = update_board(board, board_for_display, dim, count, i[0], i[1])
            # if the cell has a value between but not including 0 and 9, uncover the cell
            elif 1 <= board[i[0]][i[1]] <= 8:
                board_for_display[i[0]][i[1]] = board[i[0]][i[1]]
                count += 1
            else:
                print("Error")
    return count

# Save the board to a file with coordinates provided on the top
# and left side of the board
def save_board(board, dim, file):
    file.write("   0 1 2 3 4 5 6 7 8\n")
    file.write("--------------------\n")

    count = 0
    for i in range(dim):
        file.write(f"{count}| ") 
        # write cell value to file
        for j in range(dim):
            file.write(f"{board[i][j]} ")
        count += 1
        file.write("\n")

main()