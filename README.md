# Kenken-Game
<div align="center">
<img src="https://github.com/Heba-Atef99/Kenken-Game/blob/main/assets/wide_logo.png" width="550">  
        
![GitHub language count](https://img.shields.io/github/languages/count/Heba-Atef99/Kenken-Game?color=%2300&logo=GitHub)
![GitHub contributors](https://img.shields.io/github/contributors/Heba-Atef99/Kenken-Game?color=%2300&logo=GitHub)
![GitHub top language](https://img.shields.io/github/languages/top/Heba-Atef99/Kenken-Game?color=%2300)

Our project is a software that can solve Kenken game with any board size using backtracking, backtracking with forward checking, or backtracking with arc consistency.
</div>  

The goal of this project is to create a software that solves the KENKEN puzzle. This is a constrain satisfaction problem (CSP), and we implement and analyze the performance of the three algorithms of CSP:  
  1. Backtracking 
  2. Backtracking with forward checking 
  3. Backtracking with arc consistency

## Puzzle representation

### Board
The KenKen board is represented by a square n-by-n grid of cells. The grid may contain between 1 and n boxes (cages) represented by a heavily outlined perimeter. Each cage will contain in superscript: the target digit value for the cage followed by a mathematical operator. 
<div align="center">
<img src="https://github.com/Heba-Atef99/Kenken-Game/blob/main/images/5x5_board.png" width="550">  
</div>

### Constraints

Each valid solution must follow the below rules:

- The only numbers you may write are 1 to N for a NxN size puzzle.
- A number cannot be reapeated within the same row.
- A number cannot be reapeated within the same solumn.
- In a one-cell cage, just write the target number in that cell.
- Each "cage" (region bounded by a heavy border) contains a "target number" and an arithmetic operation. You must fill that cage with numbers that produce the target number, using only the specified arithmetic operation. Numbers may be repeated within a cage, if necessary, as long as they do not repeat within a single row or column.

## Comparison Between Algorithms
The below table represents the time performance of each algorithm, to solve different size puzzles each 100 times.

|  Size  |   BT   | BT+FC  |  BT+AC |
| :----: | :----: | :----: | :----: | 
|   3x3  | 0.113s | 0.129s | 0.147s | 
|   5x5  | 5.456s | 2.808s | 4.832s | 

## GUI Manual
1. This is the front window in which the user specifies the board size as a single number and the algorithm used to solve the board.

<div align="center">
<img src="https://github.com/Heba-Atef99/Kenken-Game/blob/main/images/front_window.png" width="550">  
</div>

2. This is an example of 4x4 board generated using backtracking with arc consistency
<div align="center">
<img src="https://github.com/Heba-Atef99/Kenken-Game/blob/main/images/back_mac_4x4.png" width="550">  
</div>

3. Warnings to guide the user if they haven't filled all input fields or enterd wrong value
<div align="center">
<img src="https://github.com/Heba-Atef99/Kenken-Game/blob/main/images/warning_1.png" width="550">  
<img src="https://github.com/Heba-Atef99/Kenken-Game/blob/main/images/warning_2.png" width="550">  
</div>


