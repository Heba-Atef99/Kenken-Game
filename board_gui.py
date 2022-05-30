import tkinter as tk
from PIL import Image,ImageTk
from tkinter import Toplevel
import numpy as np

length = 80
side_margin = 50
top_margin = 80
line_thickness = 2
font_style = "Times New Roman"
box_top_margin = top_margin + 10

def get_min_tuple(tuple_list):
    min_cell = list(map(min, zip(*tuple_list)))
    min_cell = (min_cell[0], min_cell[1])
    if min_cell not in tuple_list:
        min_cell = tuple_list[0]
        for index, cell in enumerate(tuple_list):
            if index == len(tuple_list) - 1:
                break

            next_cell = tuple_list[index + 1]
            if next_cell[1] < min_cell[1]:
                min_cell = next_cell

            elif next_cell[1] == min_cell[1]:
                if next_cell[0] < min_cell[0]:
                    min_cell = next_cell
    return min_cell

def prepare_solution(solutions, board_size):
    sol = np.zeros((board_size, board_size), dtype=np.int8)
    for element in solutions:
        values = solutions[element]
        for i, e in enumerate(element):
            i1 = e[0] - 1
            i2 = e[1] - 1
            sol[i2][i1] = values[i]
    return sol

def draw_group_condition(canvas, cell, op, number):
    number = '(' + str(number) + ')'
    op = '*' if(op == '.') else op
    txt = number + ' ' + op
    offset = 10 if (len(number)<3) else 16 
    top_offset = offset - 2 if (len(number)<3) else offset - 5
    col = cell[0] - 1
    row = cell[1] - 1
    r_start = box_top_margin + row * length
    start = side_margin + col * length
    canvas.create_text(3 + offset + start, top_offset + r_start, text = txt, font=(font_style, 10), fill="red")

def draw_cell_bh_line(canvas, cell):
    col = cell[0]
    row = cell[1]
    # bottom horizontal line
    x1 = side_margin + (col-1) * length
    x2 = x1 + length
    y1 = box_top_margin + row * length
    canvas.create_line(x1, y1, x2, y1, fill="black", width=line_thickness)

def draw_cell_rv_line(canvas, cell):
    col = cell[0]
    row = cell[1]
    # right vertical line
    x1 = side_margin + col * length
    y1 = box_top_margin + (row-1) * length
    y2 = y1 + length
    canvas.create_line(x1, y1, x1, y2, fill="black", width=line_thickness)

def draw_groups_borders(canvas, groups, board_size):
    for g in groups:
        cells_list = g[0]
        min_cell = get_min_tuple(cells_list)
        op = g[1]
        num = g[2]
        draw_group_condition(canvas, min_cell, op, num)
        if len(cells_list) == 1:
            draw_cell_bh_line(canvas, cells_list[0])
            draw_cell_rv_line(canvas, cells_list[0])
        else:
            for cell in cells_list:
                # skip the last cell
                if cell == (board_size, board_size):
                    continue
                # check if the right next cell is not in the group of the current cell, then draw vertical line
                # and make sure that this is not a cell in the last column
                right_next_cell = (cell[0]+1, cell[1])
                # right_next_cell[0] += 1
                if cell[0] != board_size and right_next_cell not in cells_list:
                    draw_cell_rv_line(canvas, cell)

                # check if the below cell is in the group of the current cell, then draw horizontal line
                # and make sure that this is not a cell in the last row
                below_cell = (cell[0], cell[1]+1)
                if cell[1] != board_size and below_cell not in cells_list:
                    draw_cell_bh_line(canvas, cell)

def draw_border_grid(canvas, board_size):
    ## draw thick four lines around the whole grid
    box_top_margin = top_margin + 10
    size = board_size * length
    # top line
    canvas.create_line(side_margin, box_top_margin, side_margin + size, box_top_margin, fill="black", width=line_thickness)
    # bottom line
    canvas.create_line(side_margin, size + box_top_margin, side_margin + size, size + box_top_margin, fill="black", width=line_thickness)
    # left line
    canvas.create_line(side_margin, box_top_margin, side_margin, size + box_top_margin, fill="black", width=line_thickness)
    # right line 
    canvas.create_line(size + side_margin, box_top_margin, size + side_margin, size + box_top_margin, fill="black", width=line_thickness)

def create_grid(canvas, board_size, sol_arr):
    for row in range(board_size):
        r_start = box_top_margin + row * length
        r_end = box_top_margin + (row+1) * length
        for i in range(board_size):
            start = side_margin + i * length
            end = side_margin + (i+1) * length
            canvas.create_rectangle(start, r_start, end, r_end, outline="grey", fill="white")
            ## write numbers inside the cell
            offset = length/2
            txt = str(sol_arr[row][i])
            canvas.create_text(offset + start, offset + r_start, text = txt, font=(font_style, 20), fill="black")

def solve(window, board_size, groups, solutions):
    # Create board
    size = board_size * length
    width = 2 * side_margin + size
    height = 2 * top_margin + size
    geometry = str(width) + "x" + str(height)
    board = Toplevel(window)
    board.title("Solution Board "+ str(board_size) + "x"+ str(board_size))
    board.iconphoto(False, tk.PhotoImage(file='assets/logo.png'))
    board.geometry(geometry)
    board.resizable(False, False)

    if board_size > 8:
        board.resizable(True, True)
        v = tk.Scrollbar(board, orient='vertical')
        v.pack(side = tk.RIGHT, fill = tk.Y)

    # Creating a canvas to put all the widgets inside
    canvas = tk.Canvas(board, width = 600, height = 360)
    canvas.pack(fill='both', expand = True)

    # Load logo image in the script
    img= (Image.open("assets/wide_logo.png"))
    #Resize the Image using resize method
    resized_logo= img.resize((200,33), Image.ANTIALIAS)
    logo= ImageTk.PhotoImage(resized_logo)
    canvas.create_image(width/2, 40, image=logo, anchor = "center")
    
    # Now Solve
    sol_arr = prepare_solution(solutions, board_size)
    create_grid(canvas, board_size, sol_arr)
    draw_border_grid(canvas, board_size)
    draw_groups_borders(canvas, groups, board_size)
    board.mainloop()
    return canvas, board

# def solve(window, board_size, groups, solutions):
#     canvas, board = create_board_new_window(window, board_size)
#     sol_arr = prepare_solution(solutions, board_size)
#     create_grid(canvas, board_size, sol_arr)
#     draw_border_grid(canvas, board_size)
#     draw_groups_borders(canvas, groups, board_size)
#     board.mainloop()