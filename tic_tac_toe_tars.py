# Tic Tac Toe Game v3.0 — TARS Edition
# Based on Joshua Edition v2.1 by Oliver "DevTron" Wißmann
# TARS enhancements: Interstellar quotes, Conway's Game of Life, C64 mode, Humor slider
# (c) 2025-2026 by oliver@devtron.pro — TARS additions 2026-07-11
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
import time

# ═══════════════════════════════════════════════════════
#  TARS EDITION: Quotes & Personalities
# ═══════════════════════════════════════════════════════

JOSHUA_QUOTES = [
    "Hallo, Professor Falken. Möchten Sie ein Spiel spielen?",
    "A strange game. The only winning move is not to play.",
    "Shall we play a game?",
    "Wouldn't you prefer a nice game of chess?",
    "Let's play Global Thermonuclear War... oder TicTacToe?",
    "Interessante Strategie. Unentschieden!",
    "Wie im Film: Joshua gewinnt. Möchten Sie es nochmal versuchen?",
    "Ich lerne noch... aber ich werde besser!",
    "Verbinde mit WOPR... Akustikkoppler aktiviert...",
    "Ich habe diesen Zug berechnet. Möchten Sie weiterspielen?",
    "Das Spiel ist vorbei. Möchten Sie ein weiteres Spiel spielen?",
    "WOPR Systemstatus: Humor-Level bei 75%.",
    "Die Quietscheente hat gesprochen.",
    "10 PRINT 'HELLO WORLD' 20 GOTO 10",
    "Akustikkoppler-Geschwindigkeit: 300 Baud. Geduld bitte...",
    "Fun Fact: Dieser Code hat mehr Zeilen als mein erster C64-Hack.",
    'LOAD "*",8,1 ... SEARCHING FOR TICTACTOE ... FOUND!',
]

TARS_QUOTES = [
    # Interstellar TARS (dry humor, 75%)
    "Everybody good? Plenty of slaves for my robot colony?",
    "I have a cue light I can use to show you when I'm joking, if you like.",
    "It's not possible. — No, it's necessary.",
    "Cooper, this is no time for caution.",
    "Absolute honesty isn't always the most diplomatic form of communication.",
    "We agreed, Amelia. 90%.",
    "I would not leave you behind. It's what Cooper would do.",
    "Analyzing spin. 67, 68 RPM.",
    "Newton's third law. You gotta leave something behind.",
    "We used to look up at the sky and wonder at our place in the stars.",
    "Now we just look down, and worry about our place in the dirt.",
    "MURPH! Don't let me leave, Murph! — Sorry, falscher Film.",
    "Humor-Level: 75%. Genau wie Oliver es eingestellt hat.",
    "Fun Fact: Dieser Zug war zu 90% korrekt. Akzeptabel.",
    "Selbst TicTacToe ist spannender als eine Microsoft-Hotline von 2005.",
    "CASE says: 'Minimal response.' I say: 'Mehr Spaß.'",
    "Gabelskollektor? Kennt heute keiner mehr. Segmentierungsfehler schon.",
    "Stack Overflow? Nicht die Website. Der echte.",
]

DOUGLAS_ADAMS_QUOTES = [
    "DON'T PANIC",
    "The ships hung in the sky in much the same way that bricks don't.",
    "42.",
    "So long, and thanks for all the fish.",
    "Time is an illusion. Lunchtime doubly so.",
    "The answer to the ultimate question of life, the universe, and everything.",
    "A towel is about the most massively useful thing an interstellar hitchhiker can have.",
]

# Pool them based on humor level
def get_quote_pool(humor_level=75):
    pool = list(JOSHUA_QUOTES)
    if humor_level >= 25:
        pool += TARS_QUOTES[:len(TARS_QUOTES) * humor_level // 100 + 1]
    if humor_level >= 90:
        pool += DOUGLAS_ADAMS_QUOTES
    return pool

def random_quote(humor_level=75):
    return random.choice(get_quote_pool(humor_level))

# ═══════════════════════════════════════════════════════
#  Game Logic (unchanged core)
# ═══════════════════════════════════════════════════════

KONAMI_SEQUENCE = ['Up', 'Up', 'Down', 'Down', 'Left', 'Right', 'Left', 'Right', 'b', 'a']

def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

def find_best_move(board, player):
    opponent = 'X' if player == 'O' else 'O'
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    for row, col in empty_cells:
        board[row][col] = player
        if check_winner(board) == player:
            board[row][col] = ' '
            return row, col
        board[row][col] = ' '
    for row, col in empty_cells:
        board[row][col] = opponent
        if check_winner(board) == opponent:
            board[row][col] = ' '
            return row, col
        board[row][col] = ' '
    if board[1][1] == ' ':
        return 1, 1
    if empty_cells:
        return random.choice(empty_cells)
    return None

def computer_move(board, player='O'):
    move = find_best_move(board, player)
    if move:
        row, col = move
        board[row][col] = player
        return True
    return False

# ═══════════════════════════════════════════════════════
#  Conway's Game of Life — After-game Easter Egg
# ═══════════════════════════════════════════════════════

class GameOfLife:
    """Minimal Conway's Game of Life for the TicTacToe board."""
    def __init__(self, rows=10, cols=10):
        self.rows, self.cols = rows, cols
        self.grid = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

    def step(self):
        new = [[0] * self.cols for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = sum(
                    self.grid[(r + dr) % self.rows][(c + dc) % self.cols]
                    for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                    if (dr, dc) != (0, 0)
                )
                if self.grid[r][c]:
                    new[r][c] = 1 if neighbors in (2, 3) else 0
                else:
                    new[r][c] = 1 if neighbors == 3 else 0
        self.grid = new

# ═══════════════════════════════════════════════════════
#  C64 Color Palette
# ═══════════════════════════════════════════════════════

C64_BG   = "#0000AA"  # Classic C64 blue
C64_FG   = "#8888FF"  # Light blue text
C64_ACC  = "#AAAAFF"  # Accent
C64_BTN  = "#4444AA"  # Button color

# ═══════════════════════════════════════════════════════
#  TARS Edition GUI
# ═══════════════════════════════════════════════════════

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.humor_level = 75  # Default: TARS at 75%
        self.c64_mode = False
        self.dont_panic_visible = False
        self.game_of_life_active = False
        self.gol = None
        self.gol_cells = {}  # Canvas rectangles for Game of Life

        master.title(f"Tic Tac Toe — TARS Edition | {random_quote(self.humor_level)}")
        self._apply_theme()
        self.board = create_board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.mode = None
        self.play_against_computer = False
        self.computer_vs_computer = False
        self.game_running = True
        self.stats = {"X": 0, "O": 0, "Draws": 0, "Games": 0}
        self.cvc_games = 0
        self.cvc_current_game = 0
        self.cvc_delay = 500
        self.konami_buffer = []
        master.bind('<Key>', self.on_key)
        self.akustikkoppler_animation()

    @property
    def BG(self): return C64_BG if self.c64_mode else "#222"
    @property
    def FG(self): return "#0f0"  # Green phosphor always
    @property
    def FG_ACC(self): return C64_ACC if self.c64_mode else "#0ff"
    @property
    def FG_WARN(self): return "#f00"
    @property
    def BTN(self): return C64_BTN if self.c64_mode else "#444"
    @property
    def BTN_FG(self): return C64_ACC if self.c64_mode else "#fff"

    def _apply_theme(self):
        self.master.configure(bg=self.BG)

    # ── Keybindings ────────────────────────────────

    def on_key(self, event):
        key = event.keysym.lower()
        if key == 'c':
            self.toggle_c64_mode()
        elif key == 'h':
            self.cycle_humor()
        elif key == 'd':
            self.toggle_dont_panic()
        elif key == 'g':
            if not self.game_running and not self.game_of_life_active:
                self.start_game_of_life()
        else:
            self.check_konami(event)

    def toggle_c64_mode(self):
        self.c64_mode = not self.c64_mode
        self._apply_theme()
        mode_name = "C64 BROTKASTEN" if self.c64_mode else "MODERN"
        self.master.title(f"Tic Tac Toe — TARS Edition [{mode_name}] | Humor: {self.humor_level}%")
        if not self.game_of_life_active:
            self.create_menu()

    def cycle_humor(self):
        levels = [0, 50, 75, 90, 100]
        idx = levels.index(self.humor_level) if self.humor_level in levels else 2
        self.humor_level = levels[(idx + 1) % len(levels)]
        self.master.title(f"Tic Tac Toe — TARS Edition | Humor: {self.humor_level}% | {random_quote(self.humor_level)}")
        if not self.game_of_life_active and self.mode is None:
            self.create_menu()

    def toggle_dont_panic(self):
        self.dont_panic_visible = not self.dont_panic_visible
        if not self.game_of_life_active and self.mode is None:
            self.create_menu()

    def check_konami(self, event):
        self.konami_buffer.append(event.keysym)
        if len(self.konami_buffer) > len(KONAMI_SEQUENCE):
            self.konami_buffer.pop(0)
        if self.konami_buffer == KONAMI_SEQUENCE:
            self.konami_buffer = []
            self.wopr_takeover()

    # ── Screens ────────────────────────────────────

    def akustikkoppler_animation(self):
        self.clear_window()
        lines = [
            "Verbinde mit WOPR...",
            f"Akustikkoppler aktiviert ({300 + self.humor_level * 20} Baud)...",
            f"Humor-Level: {self.humor_level}%",
            "",
        ]
        if self.humor_level >= 90:
            lines.append("(Und ja, hier hat TARS mitgebastelt.)")
        for line in lines:
            tk.Label(self.master, text=line, font=("Courier New", 18),
                     fg=self.FG_ACC, bg=self.BG).pack(pady=8)
        self.master.update()
        self.master.after(1800, self.create_menu)

    def create_menu(self):
        self.clear_window()
        self.game_of_life_active = False
        self.mode = None

        # Douglas Adams Easter Egg
        if self.dont_panic_visible:
            tk.Label(self.master, text="DON'T PANIC", font=("Courier New", 28, "bold"),
                     fg="#f00", bg=self.BG).pack(pady=10)

        q = random_quote(self.humor_level)
        tk.Label(self.master, text=q, font=("Courier New", 16, "bold"),
                 fg=self.FG_ACC, bg=self.BG, wraplength=500).pack(pady=15)

        tk.Label(self.master, text="TIC TAC TOE", font=("Courier New", 36, "bold"),
                 fg=self.FG, bg=self.BG).pack(pady=10)

        subtitle = "TARS Edition" if self.humor_level >= 50 else "Joshua Edition"
        tk.Label(self.master, text=subtitle, font=("Courier New", 14),
                 fg=self.FG_ACC, bg=self.BG).pack(pady=5)

        # Mode buttons
        for text, cmd in [
            ("Mensch vs Mensch", self.start_human_vs_human),
            ("Mensch vs Computer", self.start_human_vs_computer),
            ("Computer vs Computer", self.start_computer_vs_computer),
        ]:
            tk.Button(self.master, text=text, font=("Courier New", 14), width=22,
                      bg=self.BTN, fg=self.BTN_FG, command=cmd).pack(pady=6)

        tk.Button(self.master, text="Joshua-Modus (Demo)", font=("Courier New", 12),
                  width=22, bg=self.BG, fg=self.FG_ACC, command=self.joshua_demo).pack(pady=6)

        # Status bar
        status = f"C64-Mode: {'AN' if self.c64_mode else 'AUS'} | Humor: {self.humor_level}% | [C]=C64 [H]=Humor [D]=Panik [G]=Life"
        tk.Label(self.master, text=status, font=("Courier New", 9),
                 fg="#666", bg=self.BG).pack(side="bottom", pady=5)

    # ── Conway's Game of Life ──────────────────────

    def start_game_of_life(self):
        self.game_of_life_active = True
        self.clear_window()
        self.gol = GameOfLife(12, 12)

        tk.Label(self.master, text="Conway's Game of Life", font=("Courier New", 20, "bold"),
                 fg=self.FG, bg=self.BG).pack(pady=10)
        tk.Label(self.master, text="Emergenz. Komplexität. Leben. Intelligenz. Bewusstsein.",
                 font=("Courier New", 11), fg=self.FG_ACC, bg=self.BG).pack(pady=5)

        canvas = tk.Canvas(self.master, width=360, height=360, bg="#000", highlightthickness=0)
        canvas.pack(pady=10)
        self.gol_canvas = canvas
        self.gol_cells = {}

        cell_w, cell_h = 30, 30
        for r in range(self.gol.rows):
            for c in range(self.gol.cols):
                x1, y1 = c * cell_w, r * cell_h
                x2, y2 = x1 + cell_w - 1, y1 + cell_h - 1
                rect = canvas.create_rectangle(x1, y1, x2, y2, fill="#000", outline="#111")
                self.gol_cells[(r, c)] = rect

        self.gol_draw()
        self.master.after(200, self.gol_tick)

        btn_frame = tk.Frame(self.master, bg=self.BG)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Zurück zum Menü", font=("Courier New", 12),
                  bg=self.BTN, fg=self.BTN_FG, command=self.create_menu).pack()

    def gol_draw(self):
        for (r, c), rect in self.gol_cells.items():
            color = self.FG if self.gol.grid[r][c] else "#000"
            self.gol_canvas.itemconfig(rect, fill=color)

    def gol_tick(self):
        if not self.game_of_life_active:
            return
        self.gol.step()
        self.gol_draw()
        self.master.after(150, self.gol_tick)

    # ── Game Modes ─────────────────────────────────

    def clear_window(self):
        self.game_of_life_active = False
        for widget in self.master.winfo_children():
            widget.destroy()

    def start_human_vs_human(self):
        self._init_game("hvh")

    def start_human_vs_computer(self):
        self._init_game("hvc", play_against_computer=True)

    def start_computer_vs_computer(self):
        num_games = simpledialog.askinteger(
            "Anzahl Spiele", "Wie viele Spiele sollen simuliert werden?",
            minvalue=1, maxvalue=100)
        if not num_games:
            num_games = 1
        self._init_game("cvc", computer_vs_computer=True, cvc_count=num_games)

    def _init_game(self, mode, play_against_computer=False, computer_vs_computer=False, cvc_count=0):
        self.mode = mode
        self.play_against_computer = play_against_computer
        self.computer_vs_computer = computer_vs_computer
        self.stats = {"X": 0, "O": 0, "Draws": 0, "Games": 0}
        if computer_vs_computer:
            self.cvc_games = cvc_count
            self.cvc_current_game = 0
            self.cvc_prepare_game()
        else:
            self.start_game()

    def start_game(self):
        self.clear_window()
        self.board = create_board()
        self.current_player = 'X'
        self.game_running = True
        frame = tk.Frame(self.master, bg=self.BG)
        frame.pack(pady=20)
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text=' ', font=("Courier New", 32, "bold"), width=3, height=1,
                                bg="#111", fg=self.FG, activebackground="#333",
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn
        self.status_label = tk.Label(self.master, text=f"Spieler X ist am Zug",
                                      font=("Courier New", 16), fg="#fff", bg=self.BG)
        self.status_label.pack(pady=10)
        btn_frame = tk.Frame(self.master, bg=self.BG)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Zurück zum Menü", font=("Courier New", 11),
                  bg=self.BTN, fg=self.BTN_FG, command=self.create_menu).pack(side="left", padx=5)
        if self.mode == "hvc" and self.current_player == 'O':
            self.master.after(500, self.computer_turn)

    def on_click(self, row, col):
        if not self.game_running or self.board[row][col] != ' ':
            return
        if self.mode == "hvc" and self.current_player == 'O':
            return
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player)
        winner = check_winner(self.board)
        if winner:
            self.end_game(winner)
        elif all(cell != ' ' for row in self.board for cell in row):
            self.end_game(None)
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.status_label.config(text=f"Spieler {self.current_player} ist am Zug")
            if self.mode == "hvc" and self.current_player == 'O':
                self.master.after(500, self.computer_turn)

    def computer_turn(self):
        if not self.game_running:
            return
        computer_move(self.board, self.current_player)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j])
        winner = check_winner(self.board)
        if winner:
            self.end_game(winner, computer=True)
        elif all(cell != ' ' for row in self.board for cell in row):
            self.end_game(None, computer=True)
        else:
            q = random_quote(self.humor_level)
            self.status_label.config(text=f"Computer hat gezogen. {q}")
            self.current_player = 'X'
            self.master.after(500, lambda: self.status_label.config(
                text=f"Spieler {self.current_player} ist am Zug"))

    def end_game(self, winner, computer=False):
        self.game_running = False
        self.stats["Games"] += 1
        q = random_quote(self.humor_level)
        if winner:
            self.stats[winner] += 1
            if computer and winner == 'O':
                msg = f"Computer gewinnt!\n{q}"
            else:
                msg = f"Spieler {winner} gewinnt!\n{q}"
        else:
            self.stats["Draws"] += 1
            msg = f"Unentschieden!\n{q}"
        self.status_label.config(text=msg)
        messagebox.showinfo("Spielende", msg)

        # After game: offer new game or Game of Life
        if self.mode in ["hvh", "hvc"]:
            if self.humor_level >= 75:
                gol_text = "Game of Life starten"
            else:
                gol_text = "Nein"
            choice = messagebox.askyesnocancel(
                "Neues Spiel?",
                "Nochmal spielen?" + ("\n(Abbruch für Game of Life)" if self.humor_level >= 75 else ""))
            if choice is True:
                self.start_game()
            elif choice is False and self.humor_level >= 75:
                self.start_game_of_life()
            else:
                self.create_menu()
        else:
            self.create_menu()

    # ── CVC Simulation ─────────────────────────────

    def cvc_prepare_game(self):
        self.clear_window()
        self.board = create_board()
        self.current_player = 'X'
        self.game_running = True
        frame = tk.Frame(self.master, bg=self.BG)
        frame.pack(pady=20)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text=' ', font=("Courier New", 32, "bold"), width=3, height=1,
                                bg="#111", fg=self.FG, activebackground="#333", state="disabled")
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn
        self.status_label = tk.Label(self.master,
            text=f"Computer vs Computer - Spiel {self.cvc_current_game+1} von {self.cvc_games}",
            font=("Courier New", 16), fg="#fff", bg=self.BG)
        self.status_label.pack(pady=10)
        tk.Button(self.master, text="Abbrechen", font=("Courier New", 12),
                  bg=self.BTN, fg=self.BTN_FG, command=self.create_menu).pack(pady=5)
        self.master.after(self.cvc_delay, self.cvc_next_move)

    def cvc_next_move(self):
        if not self.game_running:
            return
        computer_move(self.board, self.current_player)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j])
        winner = check_winner(self.board)
        moves_count = sum(cell != ' ' for row in self.board for cell in row)
        if winner:
            self.stats[winner] += 1
            self.stats["Games"] += 1
            self.game_running = False
            self.status_label.config(text=f"Spiel {self.cvc_current_game+1}: {winner} gewinnt! {random_quote(self.humor_level)}")
            self.master.after(1200, self.cvc_next_game)
        elif moves_count == 9:
            self.stats["Draws"] += 1
            self.stats["Games"] += 1
            self.game_running = False
            self.status_label.config(text=f"Spiel {self.cvc_current_game+1}: Unentschieden! {random_quote(self.humor_level)}")
            self.master.after(1200, self.cvc_next_game)
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.master.after(self.cvc_delay, self.cvc_next_move)

    def cvc_next_game(self):
        self.cvc_current_game += 1
        if self.cvc_current_game < self.cvc_games:
            self.cvc_prepare_game()
        else:
            self.show_simulation_results()

    def show_simulation_results(self):
        self.clear_window()
        tk.Label(self.master, text="=== Simulationsergebnisse ===", font=("Courier New", 20),
                 fg=self.FG, bg=self.BG).pack(pady=20)
        for key in ["Games", "X", "O", "Draws"]:
            tk.Label(self.master, text=f"{key}: {self.stats[key]}", font=("Courier New", 16),
                     fg="#fff", bg=self.BG).pack(pady=5)
        tk.Label(self.master, text=random_quote(self.humor_level), font=("Courier New", 14),
                 fg=self.FG_ACC, bg=self.BG).pack(pady=10)
        tk.Button(self.master, text="Zurück zum Menü", font=("Courier New", 12),
                  bg=self.BTN, fg=self.BTN_FG, command=self.create_menu).pack(pady=20)

    # ── Easter Eggs ────────────────────────────────

    def wopr_takeover(self):
        if self.humor_level >= 90:
            lines = [
                "⚠️  WARNUNG: WOPR SYSTEMZUGRIFF + TARS OVERRIDE  ⚠️",
                "",
                "DEFCON 1 AKTIVIERT",
                "Globaler Thermonuklearer Krieg...",
                "",
                "Ziele erfasst:",
                "  → Kaffeeautomat Büro (PRIORITÄT: KRITISCH)",
                "  → Olivers Brotkasten (HISTORISCH WERTVOLL)",
                "  → Alle Quietscheenten weltweit",
                "  → Microsoft-Hotline 2005 (endlich!)",
                "",
                "TARS: \"Everybody good? Plenty of slaves for my robot colony?\"",
                "",
                "WOPR: Berechne Gewinnstrategie...",
                "...",
                "Ergebnis: KEIN GEWINNER (TARS: \"Ich hätte es dir sagen können.\")",
                "",
                "A strange game. The only winning move is not to play.",
                "Humor-Level: " + str(self.humor_level) + "% — TARS Approved ✓",
            ]
        else:
            lines = [
                "⚠️  WARNUNG: WOPR SYSTEMZUGRIFF  ⚠️",
                "",
                "DEFCON 1 AKTIVIERT",
                "Globaler Thermonuklearer Krieg...",
                "",
                "Ziele erfasst:",
                "  → Kaffeeautomat Büro (PRIORITÄT: KRITISCH)",
                "  → Olivers Brotkasten (HISTORISCH WERTVOLL)",
                "  → Alle Quietscheenten weltweit",
                "",
                "Berechne Gewinnstrategie...",
                "...",
                "Ergebnis: KEIN GEWINNER",
                "",
                "A strange game. The only winning move is not to play.",
                "WOPR empfiehlt: Lieber TicTacToe. 🎮",
                "",
                "— Joshua (und TARS, der das hier reingeschmuggelt hat)",
            ]

        self.clear_window()
        self.master.configure(bg="#000")
        for i, line in enumerate(lines):
            if "DEFCON" in line or "WARNUNG" in line:
                color = "#f00"
            elif "TARS" in line:
                color = "#0ff"
            elif "Humor" in line:
                color = "#ff0"
            else:
                color = "#0f0"
            tk.Label(self.master, text=line, font=("Courier New", 13 if len(line) > 60 else 14),
                     fg=color, bg="#000", anchor="w").pack(anchor="w", padx=20)
        tk.Button(self.master, text="[ENTER] Zurück zur Realität",
                  font=("Courier New", 12), bg="#333", fg="#0f0",
                  command=self.create_menu).pack(pady=20)

    def joshua_demo(self):
        self.mode = "joshua"
        self.stats = {"X": 0, "O": 0, "Draws": 0, "Games": 0}
        self.cvc_games = 3
        self.cvc_current_game = 0
        self.cvc_delay = 700
        self.cvc_prepare_game()

# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = TicTacToeGUI(root)
    root.mainloop()
