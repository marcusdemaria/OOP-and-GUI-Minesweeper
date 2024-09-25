import random

class Minesweeper:
    SIZE = 10  # Size of the game board
    BOMBS = 15  # Number of bombs

    def __init__(self):
        self.board = [['-' for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.revealed = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.remaining_cells = self.SIZE * self.SIZE - self.BOMBS
        self.game_over = False
        self.place_bombs()

    def place_bombs(self):
        bombs_placed = 0
        while bombs_placed < self.BOMBS:
            row = random.randint(0, self.SIZE - 1)
            col = random.randint(0, self.SIZE - 1)
            if self.board[row][col] != 'X':
                self.board[row][col] = 'X'
                bombs_placed += 1

    def count_adjacent_bombs(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # Skip the current cell
                new_x, new_y = x + i, y + j
                if 0 <= new_x < self.SIZE and 0 <= new_y < self.SIZE and self.board[new_x][new_y] == 'X':
                    count += 1
        return count

    def reveal_cell(self, x, y):
        if self.revealed[x][y] or self.game_over:
            return

        self.revealed[x][y] = True

        if self.board[x][y] == 'X':
            self.game_over = True
            return

        adjacent_bombs = self.count_adjacent_bombs(x, y)
        self.board[x][y] = str(adjacent_bombs) if adjacent_bombs > 0 else ' '

        if adjacent_bombs == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_x, new_y = x + i, y + j
                    if 0 <= new_x < self.SIZE and 0 <= new_y < self.SIZE:
                        self.reveal_cell(new_x, new_y)

    def print_board(self):
        print("   ", end='')
        for i in range(self.SIZE):
            print(f"{i} ", end='')
        print()

        for i in range(self.SIZE):
            print(f"{i}  ", end='')
            for j in range(self.SIZE):
                if self.revealed[i][j]:
                    print(f"{self.board[i][j]} ", end='')
                else:
                    print("- ", end='')
            print()

    def play(self):
        print("Welcome to Minesweeper!")
        self.print_board()

        while self.remaining_cells > 0 and not self.game_over:
            try:
                x, y = map(int, input("Enter coordinates (x y): ").split())
                if not (0 <= x < self.SIZE and 0 <= y < self.SIZE):
                    print("Invalid input. Coordinates must be within bounds.")
                    continue
                if self.revealed[x][y]:
                    print("Cell already revealed. Try again.")
                    continue

                self.reveal_cell(x, y)
                if self.board[x][y] == 'X':
                    break
                else:
                    self.remaining_cells -= 1
                    if self.remaining_cells == 0:
                        print("Congratulations! You won!")
                        self.print_board()
                    else:
                        self.print_board()
            except ValueError:
                print("Invalid input. Please enter two numbers.")

        if self.game_over:
            print("Game Over! You hit a bomb.")
            for i in range(self.SIZE):
                for j in range(self.SIZE):
                    if self.board[i][j] == 'X':
                        self.revealed[i][j] = True
            self.print_board()

if __name__ == "__main__":
    game = Minesweeper()
    game.play()