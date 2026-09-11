import tkinter as tk
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

class CardWidget(tk.Canvas):
    def __init__(self, parent, card=None, hidden=False):
        super().__init__(parent, width=84, height=124, bg=C_TABLE, highlightthickness=0)
        self.card = card
        self.hidden = hidden
        self.w_current = 80
        self.render()

    def render(self):
        self.delete("all")
        if self.w_current <= 0: return

        offset = (80 - self.w_current) / 2
        bg = "#FFFFFF" if not self.hidden else C_PANEL
        create_rounded_rect(self, 2 + offset, 2, 82 - offset, 122, 8, fill=bg,
                            outline="#7F8C8D" if not self.hidden else C_GOLD)

        if self.w_current > 50:
            if not self.hidden and self.card:
                font_sz_r = int(20 * (self.w_current / 80))
                font_sz_s = int(24 * (self.w_current / 80))
                self.create_text(42, 45, text=self.card['rank'], font=("Arial", font_sz_r, "bold"), fill=self.card['color'])
                self.create_text(42, 80, text=self.card['suit'], font=("Arial", font_sz_s), fill=self.card['color'])
            elif self.hidden:
                self.create_oval(32, 52, 52, 72, outline=C_GOLD, width=2)

    def flip(self, callback=None):
        self._shrink(callback)

    def _shrink(self, callback):
        self.w_current -= 10
        if self.w_current <= 0:
            self.hidden = not self.hidden
            self._grow(callback)
        else:
            self.render()
            self.after(15, lambda: self._shrink(callback))

    def _grow(self, callback):
        self.w_current += 10
        if self.w_current >= 80:
            self.w_current = 80
            self.render()
            if callback: callback()
        else:
            self.render()
            self.after(15, lambda: self._grow(callback))

class Deck:
    def __init__(self):
        self.cards = [{'rank': r, 'suit': s, 'value': 10 if r in 'JQK' else (11 if r == 'A' else int(r)),
                       'color': "#E74C3C" if s in '♥♦' else "#2C3E50"}
                      for s in '♠♥♦♣' for r in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

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

    def _calc(self, hand):
        v = sum(c['value'] for c in hand)
        a = sum(1 for c in hand if c['rank'] == 'A')
        while v > 21 and a:
            v -= 10
            a -= 1
        return v

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_menu(self):
        self.clear()

        card = tk.Frame(self, bg=C_PANEL, padx=50, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="ИГРА «21»", font=FONT_TITLE, bg=C_PANEL, fg=C_GOLD).pack(pady=(0, 20))

        ModernButton(card, "ИГРАТЬ", self.start_game, width=140).pack(pady=10)
        ModernButton(card, "ВЫХОД", self.destroy, width=140, bg=C_BTN_RED, hover_bg=C_BTN_RED_H).pack(pady=5)

    def start_game(self):
        self.clear()

        top = tk.Frame(self, bg=C_PANEL, height=60)
        top.pack(fill="x", side="top")

        tk.Label(top, text=f"БАЛАНС: ${self.balance}", font=FONT_H1, bg=C_PANEL, fg=C_GOLD).pack(side="left", padx=30, pady=15)
        ModernButton(top, "В МЕНЮ", self.show_menu, width=120, height=35, bg=C_BTN_RED, hover_bg=C_BTN_RED_H).pack(side="right", padx=20, pady=10)

        self.table = tk.Frame(self, bg=C_TABLE)
        self.table.pack(expand=True, fill="both")

        self.zones = {}
        self.zones['dealer'] = self._create_zone("ДИЛЕР", 0.5, 0.15)
        self.zones['player'] = self._create_zone("ВЫ", 0.5, 0.8)

        if self.bot_count.get() >= 1: self.zones['bot_0'] = self._create_zone("БОТ 1", 0.15, 0.5)
        if self.bot_count.get() == 2: self.zones['bot_1'] = self._create_zone("БОТ 2", 0.85, 0.5)

    def _create_zone(self, name, rx, ry):
        f = tk.Frame(self.table, bg=C_TABLE)
        f.place(relx=rx, rely=ry, anchor="center")
        lbl = tk.Label(f, text=name, font=("Segoe UI", 11, "bold"), bg=C_TABLE, fg=C_TEXT_DIM)
        lbl.pack()
        cards = tk.Frame(f, bg=C_TABLE, height=130)
        cards.pack()
        score = tk.Label(f, text="", font=FONT_H1, bg=C_TABLE, fg=C_GOLD)
        score.pack()
        return {'cards': cards, 'score': score, 'name': lbl, 'hand': []}

if __name__ == "__main__":
    app = Game21App()
    app.mainloop()