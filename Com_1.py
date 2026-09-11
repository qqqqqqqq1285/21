import tkinter as tk

C_BG = "#13271F"
C_GOLD = "#E6C27A"
FONT_TITLE = ("Segoe UI Semibold", 32)

class Game21App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Разработка игры 21")
        self.geometry("1100x800")
        self.configure(bg=C_BG)

        self.balance = 1000
        self.current_bet = tk.StringVar(value="50")
        self.bot_count = tk.IntVar(value=1)

        self.bind("<F11>", lambda e: self.attributes("-fullscreen", not self.attributes("-fullscreen")))

        tk.Label(self, text="Разработка игры 21", font=FONT_TITLE, bg=C_BG, fg=C_GOLD).pack(expand=True)

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

if __name__ == "__main__":
    app = Game21App()
    app.mainloop()