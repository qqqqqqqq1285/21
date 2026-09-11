import tkinter as tk

C_BG = "#13271F"
C_GOLD = "#E6C27A"
C_BTN_GREEN = "#2E8B57"
C_BTN_GREEN_H = "#3CB371"
FONT_TITLE = ("Segoe UI Semibold", 32)

def create_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
        x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, width=160, height=45, bg=C_BTN_GREEN, hover_bg=C_BTN_GREEN_H):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)
        self.command = command
        self.bg_color = bg
        self.hover_color = hover_bg

        self.rect_id = create_rounded_rect(self, 2, 2, width - 2, height - 2, 10, fill=self.bg_color)
        self.text_id = self.create_text(width / 2, height / 2, text=text, font=("Segoe UI", 11, "bold"), fill="white")

        self.bind("<Enter>", lambda e: self.itemconfig(self.rect_id, fill=self.hover_color))
        self.bind("<Leave>", lambda e: self.itemconfig(self.rect_id, fill=self.bg_color))
        self.bind("<Button-1>", lambda e: self.move(self.text_id, 0, 1))
        self.bind("<ButtonRelease-1>", self._on_release)
        self.config(cursor="hand2")

    def _on_release(self, event):
        self.move(self.text_id, 0, -1)
        if self.command: self.command()

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

        tk.Label(self, text="Разработка игры 21", font=FONT_TITLE, bg=C_BG, fg=C_GOLD).pack(pady=50)
        ModernButton(self, "ТЕСТ КНОПКИ", lambda: print("Кнопка работает!"), width=200).pack(pady=20)

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

if __name__ == "__main__":
    app = Game21App()
    app.mainloop()