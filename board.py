import tkinter as tk

class Board:
    def __init__(self):
        pass

    def create_board(self):
        window = tk.Tk()
        window.title("CHECKERS GAME")
        window.minsize(width=500, height=500)
        window.maxsize(width=700, height=800)
        window.configure(bg="black")

        frame = tk.Frame(window, bg="brown", bd=5, relief="ridge")
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        return window, frame

    def create_squares(self, frame):
        rows = 8
        cols = 8
        for row in range(rows):
            for col in range(cols):
                color = "brown" if (row + col) % 2 == 0 else "beige"
                square = tk.Canvas(frame, bg=color, highlightthickness=0)
                square.grid(row=row, column=col, sticky="nsew")

        for i in range(rows):
            frame.grid_rowconfigure(i, weight=1)
            frame.grid_columnconfigure(i, weight=1)
