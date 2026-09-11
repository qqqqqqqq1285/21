import tkinter as tk
from tkinter import messagebox
import random

C_BG = "#13271F"
C_TABLE = "#1A382A"
C_PANEL = "#224A36"
C_GOLD = "#E6C27A"
C_TEXT = "#F8F9FA"
C_TEXT_DIM = "#A0B0A8"
C_BTN_GREEN = "#2E8B57"
C_BTN_GREEN_H = "#3CB371"
C_BTN_RED = "#B22222"
C_BTN_RED_H = "#CD5C5C"

FONT_TITLE = ("Segoe UI Semibold", 32)
FONT_H1 = ("Segoe UI", 16, "bold")
FONT_P = ("Segoe UI", 12)

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
        self.show_menu()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_menu(self):
        self.clear()

        card = tk.Frame(self, bg=C_PANEL, padx=50, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="ИГРА «21»", font=FONT_TITLE, bg=C_PANEL, fg=C_GOLD).pack(pady=(0, 20))

        f = tk.Frame(card, bg=C_PANEL)
        f.pack(fill="x", pady=10)
        tk.Label(f, text="СТАВКА ($):", font=FONT_P, bg=C_PANEL, fg=C_TEXT_DIM, width=15, anchor="w").pack(side="left")
        e = tk.Entry(f, textvariable=self.current_bet, font=FONT_P, bg=C_BG, fg=C_TEXT, insertbackground=C_TEXT, relief="flat", bd=5)
        e.pack(side="right", fill="x", expand=True)

        tk.Label(card, text=f"ВАШ БАЛАНС: ${self.balance}", font=("Segoe UI", 10), bg=C_PANEL, fg=C_GOLD).pack(pady=(20, 10))

        ModernButton(card, "ИГРАТЬ", self.start_game, width=140).pack(pady=10)
        ModernButton(card, "ВЫХОД", self.destroy, width=140, bg=C_BTN_RED, hover_bg=C_BTN_RED_H).pack(pady=5)

    def start_game(self):
        raw_bet = self.current_bet.get().strip()

        if not raw_bet.isdigit():
            return messagebox.showwarning("Ошибка ввода", "Ставка должна содержать только положительные целые числа!")

        bet_val = int(raw_bet)

        if bet_val <= 0 or bet_val > self.balance:
            return messagebox.showwarning("Ошибка", "Некорректная сумма ставки или недостаточно средств!")

        self.balance -= bet_val
        self.clear()

        top = tk.Frame(self, bg=C_PANEL, height=60)
        top.pack(fill="x", side="top")

        tk.Label(top, text=f"БАЛАНС: ${self.balance}", font=FONT_H1, bg=C_PANEL, fg=C_GOLD).pack(side="left", padx=30, pady=15)
        tk.Label(top, text=f"СТАВКА: ${bet_val}", font=FONT_H1, bg=C_PANEL, fg=C_TEXT).pack(side="left", padx=30, pady=15)
        ModernButton(top, "В МЕНЮ", self.show_menu, width=120, height=35, bg=C_BTN_RED, hover_bg=C_BTN_RED_H).pack(side="right", padx=20, pady=10)

if __name__ == "__main__":
    app = Game21App()
    app.mainloop()