import random
import tkinter as tk
from board import Board
from disks import Disks
from moves import Moves

class CheckersGame:
    def __init__(self):
        self.board = Board()
        self.disks = Disks()
        self.moves = Moves()

        # Create the game board
        self.window, self.frame = self.board.create_board()
        self.board.create_squares(self.frame)

        # Add the disks to the board
        self.access_disks, self.board_state = self.disks.create_disks(self.frame)

        # Current player turn (Player is red, AI is black)
        self.current_player = "red"
        self.selected_disk = None

        # Bind player clicks
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

        # Check for a winner after a move
        winner = self.moves.check_winner(self.current_player, self.board_state)
        if winner:
            self.show_winner(winner)
            return

        self.switch_turn()

    def update_bindings(self, start_position, end_position):
        """Update click bindings after a move."""
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
        """Reset the game by destroying and reinitializing."""
        self.window.destroy()
        self.__init__()
        print("Game has been reset!")

    def switch_turn(self):
        """Switch player turn and trigger AI move if needed."""
        self.current_player = "red" if self.current_player == "black" else "black"
        self.selected_disk = None
        print(f"It's {self.current_player.capitalize()}'s turn!")

        if self.current_player == "black":
            self.window.after(800, self.ai_move)  # AI move after delay

    def ai_move(self):
        """AI chooses the best move using Minimax."""
        print("AI is thinking...")
        _, best_move = self.minmax(depth=3, is_maximizing=True, alpha=float('-inf'), beta=float('inf'))

        if best_move:
            start, end = best_move
            if self.moves.is_valid_capture(start, end, "black", self.board_state):
                self.moves.capture_disk(start, end, "black", self.board_state, self.access_disks)
                self.update_bindings(start,end)
            else:
                self.moves.move_disk(start, end, "black", self.board_state, self.access_disks)
                self.update_bindings(start,end)

        winner = self.moves.check_winner("black", self.board_state)
        if winner:
          self.show_winner(winner)
          return

        self.switch_turn()

    def stimulate_move(self,move,player_color):
        start,end=move
        self.board_state[end]=player_color
        self.board_state[start]="empty"
        if abs(start[0]-end[0])==2:
            mid_row=(start[0]+end[0])//2
            mid_col=(start[1]+end[1])//2
            self.board_state[(mid_row,mid_col)]="empty"
    def undo_move(self,move,captured_peice=None):
        start,end=move
        self.board_state[start]=self.board_state[end]
        self.board_state[end]="empty"
        if captured_peice:
            mid_row=(start[0]+end[0])//2
            mid_col=(start[1]+end[1])//2
            self.board_state[(mid_row,mid_col)]=captured_peice
    def valid_move(self,player_color):
        valid=[]
        valid_capture=[]
        for (row,col),color in self.board_state.items():
            if(player_color=="black"):
                single_moves=[
                    (row+1,col+1),(row+1,col-1)
                ]
                double_moves=[
                    (row+2,col+2),(row+2,col-2)
                ]
            else:
                single_moves=[
                    (row-1,col+1),(row-1,col-1)
                ]
                double_moves=[
                    (row-2,col+2),(row-2,col-2)

                ]

            if color==player_color:
                for move in single_moves:
                    if self.moves.is_valid_move((row,col),move,player_color,self.board_state):
                        valid.append(((row,col),move))
                for move in double_moves:
                    if self.moves.is_valid_capture((row,col),move,player_color,self.board_state):
                        captured_peice=self.get_captured_move(((row,col),move))
                        self.stimulate_move(((row,col),move),player_color)
                        next_capture_move=self.valid_move(player_color)
                        self.undo_move(((row,col),move),captured_peice)
                        valid_capture.append(((row,col),move))


        return valid_capture if valid_capture else valid
    def minmax(self,depth,is_maximizing,alpha,beta):
        if depth==0 or self.moves.check_winner("black",self.board_state) or self.moves.check_winner("red",self.board_state):
            return self.evaluate_board(),None
        best_move=None
        valid_moves = sorted(self.valid_move("black" if is_maximizing else "red"),
                             key=lambda move: self.evaluate_board(),
                             reverse=is_maximizing)

        if is_maximizing:
            max_val=float('-inf')
            for move in valid_moves:
                captured_peice = self.get_captured_move(move)
                self.stimulate_move(move,"black")

                eval,_=self.minmax(depth-1,False,alpha,beta)
                self.undo_move(move,captured_peice)
                if eval>max_val:
                    max_val=eval
                    best_move=move
                elif eval == max_val:  # If two moves have the same score, randomize
                    if random.random() < 0.5:
                        best_move = move
                alpha=max(alpha,eval)
                if beta<=alpha:
                    break
            return max_val,best_move
        else:
            min_val=float('inf')
            for move in valid_moves:
                captured_peice = self.get_captured_move(move)
                self.stimulate_move(move,"red")

                eval,_=self.minmax(depth-1,True,alpha,beta)
                self.undo_move(move,captured_peice)
                if eval<min_val:
                    min_val=eval
                    best_move=move
                elif eval == min_val:  # If two moves have the same score, randomize
                    if random.random() < 0.5:
                        best_move = move
                beta=min(beta,eval)
                if beta<=alpha:
                    break
            return min_val,best_move

    def evaluate_board(self):
        computer_score = 0
        player_score = 0

        for (row, col), color in self.board_state.items():
            if color == "black":
                score = 3  # Base score

                if row == 7:  # Promotion to king
                    score += 10
                elif row >= 4:  # Control center
                    score += 2
                elif col == 0 or col == 7:  # Edge defense
                    score += 1

                computer_score += score

            elif color == "red":
                score = 3

                if row == 0:  # Promotion to king
                    score += 10
                elif row <= 3:  # Control center
                    score += 2
                elif col == 0 or col == 7:  # Edge defense
                    score += 1

                player_score += score

        return computer_score - player_score  # Higher is better for AI

    def get_captured_move(self,move):
        start,end=move
        if abs(start[0]-end[0])==2:
            mid_row=(start[0]+end[0])//2
            mid_col=(start[1]+end[1])//2
            return self.board_state[(mid_row,mid_col)]
        return None

    def run(self):
        self.window.mainloop()

