import tkinter as tk
from PIL import Image,ImageTk
from tkinter import messagebox
from board_gui import solve

font_style = "Times New Roman"
# Setting the start window with title, icon & fixed size
window = tk.Tk(className=" KENKEN")
window.iconphoto(False, tk.PhotoImage(file='assets/logo.png'))
window.geometry("600x360")
window.resizable(False, False)

# Creating a canvas to put all the widgets inside
canvas = tk.Canvas(window, width = 600, height = 360)
canvas.pack(fill='both', expand = True)

# Creating background image
bg = tk.PhotoImage(file = 'assets/bg2.png')
canvas.create_image(0, 0, image=bg, anchor = "nw")

# Adding heading
canvas.create_text(300, 50, text = 'Welcome to', font=(font_style, 24), fill="white")

# Load logo image in the script
img= (Image.open("assets/wide_logo.png"))
#Resize the Image using resize method
resized_logo= img.resize((200,33), Image.ANTIALIAS)
logo= ImageTk.PhotoImage(resized_logo)
canvas.create_image(300, 90, image=logo, anchor = "center")

# Add board size Label
canvas.create_text(210, 170, text = 'Board Size:', font=(font_style, 15), fill="white")
#Create an Entry widget to accept User Input for board size
board_size_entry= tk.Entry(window, width= 10)
board_size_entry.place(x=270, y=162)

# Add algorithm Label
canvas.create_text(210, 210, text = 'Algorithm:', font=(font_style, 15), fill="white")
# Set the Menu initially
menu= tk.StringVar()
menu.set("Select Algorithm")

#Create a dropdown Menu
drop= tk.OptionMenu(window, menu, "Backtracking", "Backtracking With Forward Checking","Backtracking With Arc Consistency")
drop["highlightthickness"] = 0
drop.place(x=270, y=198)


def get_input():
    global board_size_entry, menu
    board_size= int(board_size_entry.get())
    algorithm = menu.get()
    
    # # Check that all fields are filled
    # if not board_size or algorithm == "Select Algorithm":
    #     messagebox.showwarning("Warning", "Please, fill all the input fields")

    # # Check that min no for board size is 3
    # elif int(board_size) < 2:
    #     messagebox.showwarning("Warning", "The minimum number for board size is 2")

    # else:
    #     solution = 0
    #     create_board(window, board_size, solution)
    groups = [(((1, 1),), '.', 3), (((2, 1), (3, 1), (3, 2), (2, 2)), '+', 8), (((1, 2), (1, 3)), '-', -1), (((2, 3), (3, 3)), '-', -2)]
    solutions = {((1, 1),): (3,), ((3, 1), (3, 2), (2, 1), (2, 2)): (1, 2, 2, 3), ((1, 2), (1, 3)): (1, 2), ((2, 3), (3, 3)): (1, 3)}
    solve(window, board_size, groups, solutions)

# Creating the start button
start_btn = tk.Button(window, text="Start Kenken", font=(font_style, 10), command = get_input)
start_btn.place(x=262, y=280)

# As of the window is in event listner mode
window.mainloop()