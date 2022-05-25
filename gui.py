import tkinter as tk
from PIL import Image,ImageTk

# Setting the start window
window = tk.Tk(className=" KENKEN")
window.iconphoto(False, tk.PhotoImage(file='assets/logo.png'))
window.geometry("600x360")
window.resizable(False, False)

# Creating the title of the window and displaying it on the window
# title1 = tk.Label(window, text="Welcome To", justify=tk.CENTER, font=("Times New Roman", 24), fg="white")
# title2 = tk.Label(window, text="Kenken Game")
# title1.grid(row=2, column=2)
# title2.grid(row=3, column=2)

# # Creating the start button
# start_btn = tk.Button(window, text="Start Kenken", state=tk.DISABLED)
# start_btn.grid(row=5, column=2)
# Create style Object

canvas = tk.Canvas(window, width = 600, height = 360)
canvas.pack(fill='both', expand = True)

# Creating background image
bg = tk.PhotoImage(file = 'assets/bg2.png')
canvas.create_image(0, 0, image=bg, anchor = "nw")

# Adding title 
canvas.create_text(300, 50, text = 'Welcome to', font=("Times New Roman", 24), fill="white")

# Load logo in the script
img= (Image.open("assets/wide_logo.png"))
#Resize the Image using resize method
resized_logo= img.resize((200,33), Image.ANTIALIAS)
logo= ImageTk.PhotoImage(resized_logo)
canvas.create_image(300, 90, image=logo, anchor = "center")

# Add board size Label
canvas.create_text(210, 170, text = 'Board Size:', font=("Times New Roman", 15), fill="white")
#Create an Entry widget to accept User Input
board_size_entry= tk.Entry(window, width= 10)
board_size_entry.place(x=270, y=162)

# Add algorithm Label
canvas.create_text(210, 210, text = 'Algorithm:', font=("Times New Roman", 15), fill="white")
#Set the Menu initially
menu= tk.StringVar()
menu.set("Select Algorithm")

#Create a dropdown Menu
drop= tk.OptionMenu(window, menu, "Backtracking", "Backtracking With Forward Checking","Backtracking With Arc Consistency")
drop["highlightthickness"] = 0
drop.place(x=270, y=198)


def get_input():
    global board_size_entry, menu
    board_size= board_size_entry.get()
    algorithm = menu.get()
    

    # Check that all fields are filled
    if not board_size or algorithm == "Select Algorithm":
        tk.messagebox.showwarning("Warning", "Please, fill all the input fields")

    if int(board_size) < 3:
        tk.messagebox.showwarning("Warning", "The minumem number for board size is 3")

    print(board_size)
    print(algorithm)

# Creating the start button
start_btn = tk.Button(window, text="Start Kenken", font=("Times New Roman", 10), command = get_input)
start_btn.place(x=262, y=280)

# As of the window is in event listner mode
window.mainloop()
