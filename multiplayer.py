import tkinter as tk
from board import Board
from disks import Disks
from moves import Moves

class Multiplayer:
    def __init__(self):
        self.board = Board()
        self.disks = Disks()
        self.moves = Moves()

        self.window, self.frame = self.board.create_board()
        self.board.create_squares(self.frame)

        self.access_disks, self.board_state = self.disks.create_disks(self.frame)

        self.current_player = "red"
        self.selected_disk = None

        for position, disk in self.access_disks.items():
            disk.bind("<Button-1>", lambda event, pos=position: self.select_disk(pos))

        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0 and self.board_state[(row, col)] == "empty":
                    square = self.frame.grid_slaves(row=row, column=col)[0]
                    square.bind("<Button-1>", lambda event, pos=(row, col): self.make_move(pos))

    def select_disk(self, position):
        if self.board_state[position] == self.current_player:
            self.selected_disk = position
            print(f"{self.current_player.capitalize()} selected disk at {position}")

    def make_move(self, end_position):
        if not self.selected_disk:
            print("No disk selected!")
            return

        start_position = self.selected_disk

        if self.moves.is_valid_move(start_position, end_position, self.current_player, self.board_state):
            self.moves.move_disk(start_position, end_position, self.current_player, self.board_state, self.access_disks)
            self.update_bindings(start_position, end_position)

        elif self.moves.is_valid_capture(start_position, end_position, self.current_player, self.board_state):
            self.moves.capture_disk(start_position, end_position, self.current_player, self.board_state, self.access_disks)
            self.update_bindings(start_position, end_position)

        else:
            print("Invalid move!")
            return

        winner = self.moves.check_winner(self.current_player, self.board_state)
        if winner:
            self.show_winner(winner)
            return

        self.switch_turn()

    def update_bindings(self, start_position, end_position):
        self.access_disks[end_position].bind("<Button-1>", lambda event, pos=end_position: self.select_disk(pos))
        square = self.frame.grid_slaves(row=start_position[0], column=start_position[1])[0]
        square.bind("<Button-1>", lambda event, pos=start_position: self.make_move(pos))

    def show_winner(self, player_color):
        winner_window = tk.Toplevel(self.window)
        winner_window.geometry("300x200")
        winner_window.title(f"{player_color.capitalize()} Wins!!!")

        winner_frame = tk.Frame(winner_window, bg="lightgreen", bd=5)
        winner_frame.pack(fill="both", expand=True)

        winner_message = tk.Label(winner_frame, text=f"{player_color.capitalize()} Won!!!",
                                  font=("Arial", 20), bg="lightgreen")
        winner_message.pack(pady=20)

        close_button = tk.Button(winner_frame, text="Close", font=("Arial", 14, "bold"),
                                 bg="red", fg="black", command=self.window.quit)
        close_button.pack(pady=10)

        reset_button = tk.Button(winner_frame, text="Reset Game", font=("Arial", 16, "bold"),
                                 bg="blue", fg="white", padx=20, pady=10, command=self.reset_game)
        reset_button.pack(pady=10)

    def reset_game(self):
        self.window.destroy()
        self.__init__()
        print("Game has been reset!")

    def switch_turn(self):
        self.current_player = "red" if self.current_player == "black" else "black"
        self.selected_disk = None
        print(f"It's {self.current_player.capitalize()}'s turn!")

    def run(self):
        self.window.mainloop()

