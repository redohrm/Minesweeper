# Programmer: Ruth Dohrmann
# Description: This program allows the user to play a Minesweeper game by utilizing the tKinter library.
# The program implements a 9x9 board with 10 randomly placed mines. The program includes the option of
# flagging and a timer to keeps track of how long the user has been playing. After winning or losing, 
# the program displays the entire board uncovered. The user is given the option of restarting.
import tkinter as tk
import random
import threading

done = False
game_over = False
dimension = 9
max_uncovered_cells = dimension * dimension - 10
num_cells_dug = 0

# Set up mines and update list items adjacent to mines
def set_up_board():
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

    # label cells surrounding mines
    for i in range(dimension):
        for j in range(dimension):
            if board[i][j] == '*':
                # list of coordinates for adjacent items
                adjacent = [(i-1,j),(i-1,j+1),(i-1,j-1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]
                # iterate through the tuples in the list 'adjacent'
                for x in adjacent:
                    # if the cell falls within the board and does not also contain a mine,
                    # add 1 to its value
                    if (0 <= x[0] < dimension) and (0 <= x[1] < dimension) and (board[x[0]][x[1]] != '*'):
                        board[x[0]][x[1]] += 1

# Handle the user's choice of cell to dig
def dig(i, j):
    global num_cells_dug
    global game_over

    # Check if the cell is already dug or flagged
    if board_for_display[j][i]["bg"] == "#17C337":
        # Handle bomb (uncover cells and stop the timer)
        if board[i][j] == '*':
            label1.config(text = "You lost.")
            uncover_all_cells()
            game_over = True
        # Uncover numbered cell
        elif board[i][j] > 0:
            board_for_display[j][i].config(text=str(board[i][j]), bg = "#8C6F28", activebackground = "#8C6F28")
            num_cells_dug += 1
        # Uncover blank cell
        else:
            board_for_display[j][i].config(bg = "#8C6F28", activebackground = "#8C6F28")
            num_cells_dug += 1
            update_board(j, i)

    # Check if the user won (uncovered the required number of cells without bombs)
    if(num_cells_dug == max_uncovered_cells):
        label1.config(text = "You Won!!!")
        uncover_all_cells()
        game_over = True

# Recursive function for if the user selects a blank cell. Each blank cell adjacent to the original
# blank cell will recursively call this function.
def update_board(y, x):
    global num_cells_dug
    # list of coordinates for adjacent items
    adjacent = [(y-1,x),(y-1,x+1),(y-1,x-1),(y,x-1),(y,x+1),(y+1,x-1),(y+1,x),(y+1,x+1)]

    # iterate through the tuples in the list 'adjacent'
    for i in adjacent:
        # check if the cell is in bounds and is not already uncovered
        if (0 <= i[0] < dimension) and (0 <= i[1] < dimension) and board_for_display[i[0]][i[1]]["bg"] == "#17C337":
            # if the value of the cell is 0, display the cell as a blank and recusively call this
            # function with the coordinates of this new cell
            if board[i[1]][i[0]] == 0:
                board_for_display[i[0]][i[1]].config(text = ' ', bg = "#8C6F28", activebackground = "#8C6F28")
                num_cells_dug += 1
                update_board(i[0], i[1]) 
            # if the cell has a value between but not including 0 and 9, uncover the cell
            elif 1 <= board[i[1]][i[0]] <= 8:
                board_for_display[i[0]][i[1]].config(text=str(board[i[1]][i[0]]), bg = "#8C6F28", activebackground = "#8C6F28")
                num_cells_dug += 1     
            else:
                print("Error")

# Each button in the grid will display value of the board underneath and will change color
def uncover_all_cells():
    for i in range(dimension):
        for j in range(dimension):
            board_for_display[i][j].config(text=str(board[j][i]), bg = "#8C6F28", activebackground = "#8C6F28")

# Flag a cell (right click)
def flag(i, j):
    # Verify the cell is undug
    if board_for_display[j][i]["bg"] == "#17C337":
        board_for_display[j][i].config(text='F', bg = "#D50704", activebackground = "#D50704")

# Unflag a cell (double right click)
def unflag(i, j):
    # Verify the cell was already flagged
    if board_for_display[j][i]["bg"] == "#D50704":
        board_for_display[j][i].config(text=' ', bg = "#17C337", activebackground = "#19BA37")

# Initialize the buttons that make up the board
def set_up_button(i, j):
    button = tk.Button(frame2, height=5, width=5)
    button["text"] = ' '
    button["bg"] = "#17C337"
    button["activebackground"] = "#19BA37"
    button.grid(row=i, column=j)
    # Bind the button to the appropriate functions
    button.bind("<Button-1>", lambda e: dig(i, j))
    button.bind("<Button-3>", lambda e : flag(i, j))
    button.bind("<Double-Button-3>", lambda e : unflag(i, j))
    return button

# Reset the board
def reset():
    global game_over
    global my_time
    global num_cells_dug

    # Set cells of underlying board to zero
    for i in range(dimension):
        for j in range(dimension):
            board[i][j] = 0
    # Reinitialize
    set_up_board()
    for i in range(dimension):
        for j in range(dimension):
            board_for_display[i][j].config(text=' ', bg="#17C337", activebackground="#19BA37")

    num_cells_dug = 0
    # Reset timer
    my_time = 0
    game_over = False

    label1.config(text = "Let's Play")

# Timer function called every one second (in turn this function calls timer_function_2)
def timer_function_1():
    if done:
        return
    timer_function_2()
    thread1 = threading.Timer(1, timer_function_1)
    thread1.start()

# Called every 1 second, changes label2
def timer_function_2():
    global my_time
    if not game_over:
        minutes, seconds = divmod(my_time, 60)
        hours, minutes = divmod(minutes, 60)
        label2['text'] = f"{hours}:{minutes}:{seconds}"
        my_time += 1

# End the timer if the user closes the window
def on_closing():
    global done
    done = True
    root.destroy()

# Set up root
root = tk.Tk()
root.geometry("569x669")
root.minsize(569,669)
root.maxsize(570,670)
root.configure(background="#6C5309")
root.title("Minesweeper")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Set up frames 1 and 2
frame1 = tk.Frame(root)
frame1.pack()
frame2 = tk.Frame(root)
frame2.pack()

# Set up reset button
reset_button = tk.Button(frame1, text="RESET", background="#FF9313", activebackground="#F58500", height=3, width=15, command=reset)
reset_button.pack(side="left")

# Set up labels 1 and 2
label1 = tk.Label(frame1, text="Let's Play", background="#39D8EB", height=4, width=36)
label1.pack(side="left")
# Label for the timer
label2 = tk.Label(frame1, text="Timer", background="#FB1F69", height=4, width=25)
label2.pack(side="left")
# Starting number of seconds
my_time = 0
# Start timer
thread1 = threading.Timer(1, timer_function_1)
thread1.start()

# Set up blank board (not viewed by the user)
board = [[0]*dimension for x in range(dimension)]
# Set up mines and the surrounding cells
set_up_board()
# Set up grid of buttons
board_for_display = [[set_up_button(i, j) for i in range(dimension)] for j in range(dimension)]

root.mainloop()
