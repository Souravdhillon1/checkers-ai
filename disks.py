import tkinter as tk
class Disks:
    def create_disks(self, frame):
        rows = 8
        cols = 8
        self.disks = {}
        self.board_state = {(row, col): "empty" for row in range(8) for col in range(8)}

        for row in range(rows):
            for col in range(cols):
                if row < 3 and (row + col) % 2 == 0:
                    color = "black"
                    self.board_state[(row, col)] = "black"
                elif row >= 5 and (row + col) % 2 == 0:
                    color = "red"
                    self.board_state[(row, col)] = "red"
                else:
                    continue

                # Create a disk on dark squares
                canvas = tk.Canvas(frame, bg="brown", highlightthickness=0)
                canvas.grid(row=row, column=col, sticky="nsew")
                canvas.create_oval(10, 10, 75, 80, fill=color, outline="black")
                self.disks[(row, col)] = canvas

        return self.disks, self.board_state
