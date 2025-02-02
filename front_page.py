import tkinter as tk
from checkers import CheckersGame
from multiplayer import Multiplayer
class Front:
    def __init__(self):
        self.front_window = tk.Tk()
        self.front_window.title("Front Page")
        self.front_window.geometry("300x200")
        self.front_window.configure(bg="white")

        self.front_frame = tk.Frame(self.front_window, bg="lightblue", bd=5, relief="ridge")
        self.front_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.single_button = tk.Button(self.front_frame, text="Single Player", font=("Arial", 12, "bold"),
                                       bg="green", fg="white", command=self.single_player)
        self.single_button.pack(pady=10)

        self.multi_button = tk.Button(self.front_frame, text="Multiplayer", font=("Arial", 12, "bold"),
                                      bg="blue", fg="white", command=self.multiplayer)
        self.multi_button.pack(pady=10)

        self.front_window.mainloop()

    def single_player(self):
        print("Single Player mode selected!")
        self.front_window.destroy()  # Close the front page
        game = CheckersGame()  # Start the single player game
        game.run()

    def multiplayer(self):
        print("Multiplayer mode selected!")
        self.front_window.destroy()  # Close the front page
        multiplayer_game = Multiplayer()  # Start the multiplayer game
        multiplayer_game.run()

    def run(self):
        self.front_window.mainloop()