import tkinter as tk
from tkinter import messagebox
import random
import copy

class SudokuSolver:
    def _init_(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        
        # Initialize a 9x9 grid of Entry widgets
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        
        # Add buttons for solving and generating puzzles
        solve_button = tk.Button(master, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=10, column=0, columnspan=4, pady=10)
        
        generate_button = tk.Button(master, text="Generate Puzzle", command=self.generate_puzzle)
        generate_button.grid(row=10, column=5, columnspan=4, pady=10)
        
    def create_grid(self):
        """Creates the 9x9 grid of Entry widgets for the Sudoku puzzle."""
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.master, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry
                
    def get_board(self):
        """Retrieves the current state of the Sudoku board from the GUI."""
        board = []
        for row in range(9):
            board_row = []
            for col in range(9):
                text = self.entries[row][col].get()
                # If the cell is empty, consider it as 0
                if text == '':
                    board_row.append(0)
                else:
                    board_row.append(int(text))
            board.append(board_row)
        return board
    
    def set_board(self, board):
        """Sets the given Sudoku board state in the GUI."""
        for row in range(9):
            for col in range(9):
                value = board[row][col]
                self.entries[row][col].delete(0, tk.END)
                if value != 0:
                    self.entries[row][col].insert(0, str(value))
    
    def is_valid(self, board, num, pos):
        """Checks if placing the number num at position pos on the board is valid."""
        # Check the row
        for i in range(9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False
        
        # Check the column
        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False
        
        # Check the 3x3 square
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False
        
        return True
    
    def solve(self, board):
        """Uses backtracking to solve the given Sudoku board."""
        empty = self.find_empty(board)
        if not empty:
            return True
        else:
            row, col = empty
            
        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                
                if self.solve(board):
                    return True
                
                board[row][col] = 0
        
        return False
    
    def find_empty(self, board):
        """Finds the first empty cell on the board."""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return (row, col)
        return None
    
    def solve_sudoku(self):
        """Solves the current Sudoku board and displays the solution."""
        board = self.get_board()
        if self.solve(board):
            self.set_board(board)
        else:
            
            messagebox.showerror("No Solution", "No solution exists for the current Sudoku board.")
    
    def generate_puzzle(self):
        """Generates a new Sudoku puzzle and displays it on the board."""
     
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
        
      
        full_board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board(full_board)
        
        
        solution = copy.deepcopy(full_board)
        

        num_cells_to_remove = random.randint(30, 50)
        
      
        removed_positions = set()
        while len(removed_positions) < num_cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if (row, col) not in removed_positions:
                full_board[row][col] = 0
                removed_positions.add((row, col))
                
                
                temp_board = copy.deepcopy(full_board)
                self.solve(temp_board)
                if temp_board != solution:
                   
                    full_board[row][col] = solution[row][col]
                    removed_positions.remove((row, col))
        
       
        self.set_board(full_board)
    
    def fill_board(self, board):
        """Fills the given board using a backtracking algorithm."""
        if not self.find_empty(board):
            return True
        
        row, col = self.find_empty(board)
        numbers = list(range(1, 10))
        random.shuffle(numbers)  
        
        for num in numbers:
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                if self.fill_board(board):
                    return True
                board[row][col] = 0
        
        return False

if _name_ == "_main_":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
