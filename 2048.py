from tkinter import *  # Import tkinter for GUI creation
from tkinter import messagebox  # Provides pop-up dialog boxes
import random  

class GameBoard:
    # Color configuration for different tile values
    TILE_BG_COLOR = {
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#f2b179',
        '16': '#f59563',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#edc850',
        '1024': '#edc22e',
        '2048': '#edc22e',
    }

    TILE_COLOR = {
        '2': '#776e65',
        '4': '#776e65',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#f9f6f2',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }

    def __init__(self):
        # Initializing game window and layout
        self.window = Tk()
        self.window.title("2048 Game")
        self.window.configure(bg="#faf8ef")

        # Creating game grid
        self.game_area = Frame(self.window, bg="#bbada0", bd=4, relief=RIDGE)
        self.board = []
        self.grid_values = [[0] * 4 for _ in range(4)]
        self.is_compressed = False
        self.is_merged = False
        self.is_moved = False
        self.score = 0
        self.best_score = 0  # Initializing best score

        # Top Frame for score display
        self.top_frame = Frame(self.window, bg="#faf8ef", padx=10, pady=10)
        self.top_frame.grid(row=0, column=0, pady=10)

        # Score and best score labels
        self.score_label = Label(
            self.top_frame, text="Score: 0", font=("Verdana", 18, "bold"), bg="#faf8ef", fg="#776e65"
        )
        self.score_label.grid(row=0, column=0, sticky="e", padx=(20, 10))

        self.best_score_label = Label(
            self.top_frame, text="Best: 0", font=("Verdana", 18, "bold"), bg="#faf8ef", fg="#776e65"
        )
        self.best_score_label.grid(row=0, column=1, sticky="e", padx=(20, 10))

        # Grid layout creation
        self.game_area.grid(row=1)
        for i in range(4):
            row_cells = []
            for j in range(4):
                label = Label(
                    self.game_area,
                    text="",
                    bg="#cdc1b4",
                    font=("Helvetica", 30, "bold"),
                    width=4,
                    height=2,
                )
                label.grid(row=i, column=j, padx=7, pady=7)
                row_cells.append(label)
            self.board.append(row_cells)
        self.game_area.grid()

    def reverse_rows(self):
        """Reverses the tiles in each row."""
        for row_index in range(4):
            self.grid_values[row_index].reverse()

    def transpose_grid(self):
        """Transposes the grid (rows become columns and vice versa)."""
        self.grid_values = [
            [self.grid_values[j][i] for j in range(len(self.grid_values))] 
            for i in range(len(self.grid_values[0]))
        ]

    def compress_grid(self):
        """Compresses the grid by shifting all non-zero values to the left."""
        temp_grid = [[0] * 4 for _ in range(4)]
        for i in range(4):
            count = 0
            for j in range(4):
                if self.grid_values[i][j] != 0:
                    temp_grid[i][count] = self.grid_values[i][j]
                    if count != j:
                        self.is_compressed = True
                    count += 1
        self.grid_values = temp_grid

    def merge_grid(self):
        """Merges adjacent cells with the same value and updates the score."""
        self.is_merged = False
        for i in range(4):
            for j in range(3):
                if (
                    self.grid_values[i][j] == self.grid_values[i][j + 1]
                    and self.grid_values[i][j] != 0
                ):
                    self.grid_values[i][j] *= 2
                    self.grid_values[i][j + 1] = 0
                    self.score += self.grid_values[i][j]
                    self.is_merged = True

    def add_random_tile(self):
        """Adds a random tile (2 or 4) to an empty cell on the grid."""
        empty_cells = [
            (i, j) for i in range(4) for j in range(4) if self.grid_values[i][j] == 0
        ]
        selected_cell = random.choice(empty_cells)
        self.grid_values[selected_cell[0]][selected_cell[1]] = random.choices([2, 4], weights=[90, 10])[0]

    def can_merge(self):
        """Checks if any adjacent cells can be merged."""
        for i in range(4):
            for j in range(3):
                if self.grid_values[i][j] == self.grid_values[i][j + 1]:
                    return True
        for i in range(3):
            for j in range(4):
                if self.grid_values[i][j] == self.grid_values[i + 1][j]:
                    return True
        return False

    def update_grid_display(self):
        """Updates the grid with the current tile values and colors."""
        for i in range(4):
            for j in range(4):
                if self.grid_values[i][j] == 0:
                    self.board[i][j].config(text="", bg="#cdc1b4")
                else:
                    self.board[i][j].config(
                        text=str(self.grid_values[i][j]),
                        bg=self.TILE_BG_COLOR.get(str(self.grid_values[i][j])),
                        fg=self.TILE_COLOR.get(str(self.grid_values[i][j])),
                    )
        self.score_label.config(text=f"Score: {self.score}")
        self.best_score_label.config(text=f"Best: {self.best_score}")


class Game2048:
    def __init__(self, game_board):
        self.game_board = game_board
        self.game_over = False
        self.game_won = False
        self.restart_button = Button(
            self.game_board.top_frame,
            text="Restart",
            command=self.restart_game,
            font=("Verdana", 14, "bold"),
            bg="#8f7a66",
            fg="#ffffff",
            activebackground="#9c8574",
            relief=RAISED,
            padx=10,
        )
        self.restart_button.grid(row=0, column=2, sticky="w", padx=(0, 20))

    def start_game(self):
        """Starts the game by adding two random tiles and binding keyboard keys."""
        self.game_board.add_random_tile()
        self.game_board.add_random_tile()
        self.game_board.update_grid_display()
        self.game_board.window.bind("<Key>", self.handle_keypress)
        self.game_board.window.mainloop()

    def restart_game(self):
        """Restarts the game with a fresh grid."""
        self.game_board.grid_values = [[0] * 4 for _ in range(4)]
        self.game_board.score = 0
        self.game_board.score_label.config(text="Score: 0")  # Reset score label
        self.game_board.add_random_tile()  # Add two new random tiles
        self.game_board.add_random_tile()
        self.game_board.update_grid_display()  # Refresh the grid display

    def handle_keypress(self, event):
        """Handles key presses for moving and merging tiles."""
        if self.game_over or self.game_won:
            return
        self.game_board.is_compressed = False
        self.game_board.is_merged = False
        self.game_board.is_moved = False
        key_pressed = event.keysym

        if key_pressed == "Up":
            # Transpose to treat columns as rows, then compress and merge to move tiles up, and transpose back to restore original orientation.
            self.game_board.transpose_grid()
            self.game_board.compress_grid()
            self.game_board.merge_grid()
            self.game_board.is_moved = self.game_board.is_compressed or self.game_board.is_merged
            self.game_board.transpose_grid()
        elif key_pressed == "Down":
            # Transpose to treat columns as rows, reverse the rows to move tiles down, then compress and merge, and reverse back to restore original orientation.
            self.game_board.transpose_grid()
            self.game_board.reverse_rows()
            self.game_board.compress_grid()
            self.game_board.merge_grid()
            self.game_board.is_moved = self.game_board.is_compressed or self.game_board.is_merged
            self.game_board.compress_grid()
            self.game_board.reverse_rows()
            self.game_board.transpose_grid()
        elif key_pressed == "Left":
            # Compress and merge tiles to move them left, then compress again to fill any gaps.
            self.game_board.compress_grid()
            self.game_board.merge_grid()
            self.game_board.is_moved = self.game_board.is_compressed or self.game_board.is_merged
            self.game_board.compress_grid()
        elif key_pressed == "Right":
            # Reverse rows to move tiles to the right, compress and merge, and reverse back to restore original orientation.
            self.game_board.reverse_rows()
            self.game_board.compress_grid()
            self.game_board.merge_grid()
            self.game_board.is_moved = self.game_board.is_compressed or self.game_board.is_merged
            self.game_board.compress_grid()
            self.game_board.reverse_rows()
        else:
            pass
        self.game_board.update_grid_display()

        # Check for game win
        if any(self.game_board.grid_values[i][j] == 2048 for i in range(4) for j in range(4)):
            self.game_won = True
            messagebox.showinfo("2048", message="You Won!")
            return

        # Check for game over
        if not any(self.game_board.grid_values[i][j] == 0 for i in range(4) for j in range(4)) and not self.game_board.can_merge():
            self.game_over = True
            if messagebox.askyesno("2048", "Game Over! Do you want to play again?"):
                self.restart_game()
            else:
                self.game_board.window.quit()

        if self.game_board.is_moved:
            # If a move was made, add a random tile to the grid to simulate the game's next step.
            self.game_board.add_random_tile()

        # Update best score
        if self.game_board.score > self.game_board.best_score:
            self.game_board.best_score = self.game_board.score

        self.game_board.update_grid_display()


game_board = GameBoard()
game_2048 = Game2048(game_board)
game_2048.start_game()
