import random
import tkinter as tk
from tkinter import messagebox

class MinesweeperGUI:
    SIZE = 10  # Size of the game board (10x10)
    BOMBS = 15  # Total number of bombs on the board

    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.board = [['-' for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.revealed = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.remaining_cells = self.SIZE * self.SIZE - self.BOMBS
        self.game_over = False
        self.buttons = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.create_widgets()
        self.place_bombs()

    def create_widgets(self):
        # Create buttons for the game board
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                btn = tk.Button(self.root, width=3, height=1, command=lambda x=i, y=j: self.on_click(x, y))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        # Add restart and exit buttons
        restart_btn = tk.Button(self.root, text="Restart", command=self.restart_game)
        restart_btn.grid(row=self.SIZE, column=0, columnspan=self.SIZE//2)

        exit_btn = tk.Button(self.root, text="Exit", command=self.root.quit)
        exit_btn.grid(row=self.SIZE, column=self.SIZE//2, columnspan=self.SIZE//2)

    def place_bombs(self):
        # Randomly place bombs on the board
        bombs_placed = 0
        while bombs_placed < self.BOMBS:
            row = random.randint(0, self.SIZE - 1)
            col = random.randint(0, self.SIZE - 1)
            if self.board[row][col] != 'X':
                self.board[row][col] = 'X'
                bombs_placed += 1

    def count_adjacent_bombs(self, x, y):
        # Count the number of bombs surrounding the given cell (x, y)
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_x, new_y = x + i, y + j
                if 0 <= new_x < self.SIZE and 0 <= new_y < self.SIZE and self.board[new_x][new_y] == 'X':
                    count += 1
        return count

    def reveal_cell(self, x, y):
        # Reveal the cell at (x, y) and update the UI
        if self.revealed[x][y] or self.game_over:
            return

        self.revealed[x][y] = True

        if self.board[x][y] == 'X':
            self.game_over = True
            self.buttons[x][y].config(text='X', bg='red')
            self.show_all_bombs()
            messagebox.showinfo("Game Over", "You hit a bomb!")
            return

        adjacent_bombs = self.count_adjacent_bombs(x, y)
        self.board[x][y] = str(adjacent_bombs) if adjacent_bombs > 0 else ' '
        self.buttons[x][y].config(text=self.board[x][y], state='disabled')

        if adjacent_bombs == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_x, new_y = x + i, y + j
                    if 0 <= new_x < self.SIZE and 0 <= new_y < self.SIZE:
                        self.reveal_cell(new_x, new_y)

        self.remaining_cells -= 1
        if self.remaining_cells == 0:
            messagebox.showinfo("Congratulations", "You won!")
            self.game_over = True

    def on_click(self, x, y):
        # Handle button click
        if not self.game_over:
            self.reveal_cell(x, y)

    def show_all_bombs(self):
        # Reveal all bombs on the board when the game is over
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.board[i][j] == 'X':
                    self.buttons[i][j].config(text='X', bg='red')

    def restart_game(self):
        # Restart the game
        self.board = [['-' for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.revealed = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.remaining_cells = self.SIZE * self.SIZE - self.BOMBS
        self.game_over = False
        self.place_bombs()
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                self.buttons[i][j].config(text='', bg='SystemButtonFace', state='normal')

# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = MinesweeperGUI(root)
    root.mainloop()
