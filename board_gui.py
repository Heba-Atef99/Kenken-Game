import tkinter as tk
from PIL import Image,ImageTk
from tkinter import Toplevel, messagebox

length = 80
side_margin = 50
top_margin = 80

def create_grid(canvas, board_size):
    top_margin = 90
    left_margin = side_margin
    for row in range(board_size):
        r_start = top_margin + row * length
        r_end = top_margin + (row+1) * length
        for i in range(board_size):
            start = left_margin + i * length
            end = left_margin + (i+1) * length
            canvas.create_rectangle(start, r_start, end, r_end, outline="black", fill="white")
            offset = length/2
            canvas.create_text(offset + start, offset + r_start, text = '59', font=("Times New Roman", 20), fill="black")
            offset = 7
            canvas.create_text(3 + offset + start, offset + r_start, text = '11+', font=("Times New Roman", 10), fill="red")

def create_board(window, board_size, solution):
    size = board_size * length
    width = 2 * side_margin + size
    height = 2 * top_margin + size
    geometry = str(width) + "x" + str(height)
    board = Toplevel(window)
    board.title("Solution Board")
    board.iconphoto(False, tk.PhotoImage(file='assets/logo.png'))
    board.geometry(geometry)
    board.resizable(False, False)

    # Creating a canvas to put all the widgets inside
    canvas = tk.Canvas(board, width = 600, height = 360)
    canvas.pack(fill='both', expand = True)

    # Creating background image
    # bg = tk.PhotoImage(file = 'assets/bg2.png')
    # canvas.create_image(0, 0, image=bg, anchor = "nw")

    # Load logo image in the script
    img= (Image.open("assets/wide_logo.png"))
    #Resize the Image using resize method
    resized_logo= img.resize((200,33), Image.ANTIALIAS)
    logo= ImageTk.PhotoImage(resized_logo)
    canvas.create_image(width/2, 40, image=logo, anchor = "center")

    
    create_grid(canvas, board_size)

    board.mainloop()

