import tkinter as tk
import random

C_BG = "#13271F"
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

class Deck:
    def __init__(self):
        self.cards = [{'rank': r, 'suit': s, 'value': 10 if r in 'JQK' else (11 if r == 'A' else int(r)),
                       'color': "#E74C3C" if s in '♥♦' else "#2C3E50"}
                      for s in '♠♥♦♣' for r in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

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

        bg_canvas = tk.Canvas(self, bg=C_BG, highlightthickness=0)
        bg_canvas.pack(fill="both", expand=True)
        bg_canvas.create_oval(-100, -100, 400, 400, fill="#183626", outline="")
        bg_canvas.create_oval(800, 500, 1300, 1000, fill="#183626", outline="")

        card = tk.Frame(self, bg=C_PANEL, padx=50, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="ИГРА «21»", font=FONT_TITLE, bg=C_PANEL, fg=C_GOLD).pack(pady=(0, 30))

        def create_input(parent, label, var, is_option=False, options=None):
            f = tk.Frame(parent, bg=C_PANEL)
            f.pack(fill="x", pady=10)
            tk.Label(f, text=label, font=FONT_P, bg=C_PANEL, fg=C_TEXT_DIM, width=15, anchor="w").pack(side="left")
            if is_option:
                opt = tk.OptionMenu(f, var, *options)
                opt.config(bg=C_BG, fg=C_TEXT, font=FONT_P, highlightthickness=0, relief="flat")
                opt["menu"].config(bg=C_BG, fg=C_TEXT, font=FONT_P)
                opt.pack(side="right", fill="x", expand=True)
            else:
                e = tk.Entry(f, textvariable=var, font=FONT_P, bg=C_BG, fg=C_TEXT, insertbackground=C_TEXT, relief="flat", bd=5)
                e.pack(side="right", fill="x", expand=True)

        create_input(card, "СТАВКА ($):", self.current_bet)
        create_input(card, "КОЛ-ВО БОТОВ:", self.bot_count, True, [0, 1, 2])

        tk.Label(card, text=f"ВАШ БАЛАНС: ${self.balance}", font=("Segoe UI", 10), bg=C_PANEL, fg=C_GOLD).pack(pady=(20, 10))

        btn_frame = tk.Frame(card, bg=C_PANEL)
        btn_frame.pack(pady=10)

        ModernButton(btn_frame, "ПРАВИЛА", self.show_rules, width=140, bg="#2980B9", hover_bg="#3498DB").pack(side="left", padx=5)
        ModernButton(btn_frame, "ИГРАТЬ", None, width=140).pack(side="left", padx=5)
        ModernButton(btn_frame, "ВЫХОД", self.destroy, width=140, bg=C_BTN_RED, hover_bg=C_BTN_RED_H).pack(side="left", padx=5)

    def show_rules(self):
        rules_win = tk.Toplevel(self)
        rules_win.title("Правила игры")
        rules_win.geometry("500x450")
        rules_win.configure(bg=C_BG)
        rules_win.resizable(False, False)
        rules_win.transient(self)
        rules_win.grab_set()

        tk.Label(rules_win, text="ПРАВИЛА ИГРЫ «21»", font=FONT_H1, bg=C_BG, fg=C_GOLD).pack(pady=10)

        text_frame = tk.Frame(rules_win, bg=C_BG)
        text_frame.pack(padx=20, pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        rules_text = tk.Text(text_frame, font=FONT_P, bg=C_BG, fg=C_TEXT, wrap="word", yscrollcommand=scrollbar.set, bd=0)
        rules_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=rules_text.yview)

        content = (
            "1. Цель игры — набрать сумму очков, максимально близкую к 21, но не превышающую её.\n\n"
            "2. Карты от 2 до 10 дают соответствующие очки по номиналу.\n\n"
            "3. Валет (J), Дама (Q) и Король (K) дают по 10 очков.\n\n"
            "4. Туз (A) дает 11 очков (или 1 очко при переборе).\n\n"
            "5. Дилер обязан брать карты до 17 очков.\n\n"
            "6. БОТЫ: Управляются алгоритмом и остановятся при наборе 17 очков."
        )
        rules_text.insert("1.0", content)
        rules_text.config(state="disabled")

        ModernButton(rules_win, "ЗАКРЫТЬ", rules_win.destroy, width=150, bg=C_BTN_RED, hover_bg=C_BTN_RED_H).pack(pady=15)

if __name__ == "__main__":
    app = Game21App()
    app.mainloop()