# Tic Tac Toe Game v2.1 - Joshua Edition
# designed by:
#   ██████  ██       ██  ██    ██ ███████ ██████  
#  ██    ██ ██       ██  ██    ██ ██      ██   ██ 
#  ██    ██ ██       ██  ██    ██ █████   ██████  
#  ██    ██ ██       ██   ██  ██  ██      ██   ██ 
#   ██████  ███████  ██    ████   ███████ ██   ██ 
# (c) 2025-2026 by oliver@devtron.pro
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# WarGames-Zitate und Joshua-Kommentare
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
    "Strange game. The only winning move is not to play.",
    "WOPR Systemstatus: Humor-Level bei 75%.",
    "Die Quietscheente hat gesprochen.",
    "10 PRINT 'HELLO WORLD' 20 GOTO 10",
    "Akustikkoppler-Geschwindigkeit: 300 Baud. Geduld bitte...",
    "Fun Fact: Dieser Code hat mehr Zeilen als mein erster C64-Hack.",
    "LOAD \"*\",8,1 ... SEARCHING FOR TICTACTOE ... FOUND!",
]

# Konami Code Easter Egg: ↑↑↓↓←→←→BA
KONAMI_SEQUENCE = ['Up', 'Up', 'Down', 'Down', 'Left', 'Right', 'Left', 'Right', 'b', 'a']

def random_joshua_quote():
    return random.choice(JOSHUA_QUOTES)

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

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title(f"Tic Tac Toe - Joshua Edition | {random_joshua_quote()}")
        master.configure(bg="#222")
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
        self.cvc_delay = 500  # ms
        self.konami_buffer = []
        self.master.bind('<Key>', self.check_konami)
        self.akustikkoppler_animation()

    def check_konami(self, event):
        """Konami Code Easter Egg: ↑↑↓↓←→←→BA"""
        self.konami_buffer.append(event.keysym)
        if len(self.konami_buffer) > len(KONAMI_SEQUENCE):
            self.konami_buffer.pop(0)
        if self.konami_buffer == KONAMI_SEQUENCE:
            self.konami_buffer = []
            self.wopr_takeover()

    def akustikkoppler_animation(self):
        self.clear_window()
        anim_label = tk.Label(self.master, text="Verbinde mit WOPR...\nAkustikkoppler aktiviert...\n", font=("Courier New", 18), fg="#0ff", bg="#222")
        anim_label.pack(pady=40)
        self.master.update()
        self.master.after(1800, self.create_menu)

    def create_menu(self):
        self.clear_window()
        # Joshua-Begrüßung
        label = tk.Label(self.master, text=random_joshua_quote(), font=("Courier New", 20, "bold"), fg="#0ff", bg="#222")
        label.pack(pady=20)
        title = tk.Label(self.master, text="TIC TAC TOE", font=("Courier New", 32, "bold"), fg="#0f0", bg="#222")
        title.pack(pady=10)
        btn1 = tk.Button(self.master, text="Mensch vs Mensch", font=("Courier New", 16), width=20, bg="#444", fg="#fff",
                         command=self.start_human_vs_human)
        btn1.pack(pady=10)
        btn2 = tk.Button(self.master, text="Mensch vs Computer", font=("Courier New", 16), width=20, bg="#444", fg="#fff",
                         command=self.start_human_vs_computer)
        btn2.pack(pady=10)
        btn3 = tk.Button(self.master, text="Computer vs Computer", font=("Courier New", 16), width=20, bg="#444", fg="#fff",
                         command=self.start_computer_vs_computer)
        btn3.pack(pady=10)
        # Easter Egg: Joshua-Modus
        btn4 = tk.Button(self.master, text="Joshua-Modus (Demo)", font=("Courier New", 14), width=20, bg="#222", fg="#0ff",
                         command=self.joshua_demo)
        btn4.pack(pady=10)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def start_human_vs_human(self):
        self.mode = "hvh"
        self.play_against_computer = False
        self.computer_vs_computer = False
        self.stats = {"X": 0, "O": 0, "Draws": 0, "Games": 0}
        self.start_game()

    def start_human_vs_computer(self):
        self.mode = "hvc"
        self.play_against_computer = True
        self.computer_vs_computer = False
        self.stats = {"X": 0, "O": 0, "Draws": 0, "Games": 0}
        self.start_game()

    def start_computer_vs_computer(self):
        self.mode = "cvc"
        self.play_against_computer = False
        self.computer_vs_computer = True
        num_games = simpledialog.askinteger("Anzahl Spiele", "Wie viele Spiele sollen simuliert werden?", minvalue=1, maxvalue=100)
        if not num_games:
            num_games = 1
        self.stats = {"X": 0, "O": 0, "Draws": 0, "Games": 0}
        self.cvc_games = num_games
        self.cvc_current_game = 0
        self.cvc_prepare_game()

    def cvc_prepare_game(self):
        self.clear_window()
        self.board = create_board()
        self.current_player = 'X'
        self.game_running = True
        frame = tk.Frame(self.master, bg="#222")
        frame.pack(pady=20)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text=' ', font=("Courier New", 32, "bold"), width=3, height=1,
                                bg="#111", fg="#0f0", activebackground="#333", state="disabled")
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn
        self.status_label = tk.Label(self.master, text=f"Computer vs Computer - Spiel {self.cvc_current_game+1} von {self.cvc_games}", font=("Courier New", 16), fg="#fff", bg="#222")
        self.status_label.pack(pady=10)
        tk.Button(self.master, text="Abbrechen", font=("Courier New", 12), bg="#444", fg="#fff",
                  command=self.create_menu).pack(pady=5)
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
            # Joshua-Kommentar bei Computer-Sieg
            self.status_label.config(text=f"Spiel {self.cvc_current_game+1}: {winner} gewinnt! {random_joshua_quote()}")
            self.master.after(1200, self.cvc_next_game)
        elif moves_count == 9:
            self.stats["Draws"] += 1
            self.stats["Games"] += 1
            self.game_running = False
            # Joshua-Kommentar bei Unentschieden
            self.status_label.config(text=f"Spiel {self.cvc_current_game+1}: Unentschieden! {random_joshua_quote()}")
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

    def start_game(self):
        self.clear_window()
        self.board = create_board()
        self.current_player = 'X'
        self.game_running = True
        frame = tk.Frame(self.master, bg="#222")
        frame.pack(pady=20)
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text=' ', font=("Courier New", 32, "bold"), width=3, height=1,
                                bg="#111", fg="#0f0", activebackground="#333",
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn
        self.status_label = tk.Label(self.master, text="Spieler X ist am Zug", font=("Courier New", 16), fg="#fff", bg="#222")
        self.status_label.pack(pady=10)
        tk.Button(self.master, text="Zurück zum Menü", font=("Courier New", 12), bg="#444", fg="#fff",
                  command=self.create_menu).pack(pady=5)
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
            # Joshua-Kommentar bei Computer-Sieg
            self.end_game(winner, computer=True)
        elif all(cell != ' ' for row in self.board for cell in row):
            self.end_game(None, computer=True)
        else:
            # Joshua-Kommentar nach Computer-Zug
            self.status_label.config(text=f"Computer hat gezogen. {random_joshua_quote()}")
            self.current_player = 'X'
            self.master.after(500, lambda: self.status_label.config(text=f"Spieler {self.current_player} ist am Zug"))

    def end_game(self, winner, computer=False):
        self.game_running = False
        self.stats["Games"] += 1
        if winner:
            self.stats[winner] += 1
            if computer and winner == 'O':
                msg = f"Computer (Joshua) gewinnt!\n{random_joshua_quote()}"
            else:
                msg = f"Spieler {winner} gewinnt!\n{random_joshua_quote()}"
        else:
            self.stats["Draws"] += 1
            msg = f"Unentschieden!\n{random_joshua_quote()}"
        self.status_label.config(text=msg)
        messagebox.showinfo("Spielende", msg)
        if self.mode in ["hvh", "hvc"]:
            if messagebox.askyesno("Neues Spiel?", "Nochmal spielen?\n" + random_joshua_quote()):
                self.start_game()
            else:
                self.create_menu()

    def show_simulation_results(self):
        self.clear_window()
        tk.Label(self.master, text="=== Simulationsergebnisse ===", font=("Courier New", 20), fg="#0f0", bg="#222").pack(pady=20)
        tk.Label(self.master, text=f"Spiele gesamt: {self.stats['Games']}", font=("Courier New", 16), fg="#fff", bg="#222").pack(pady=5)
        tk.Label(self.master, text=f"X gewinnt: {self.stats['X']}", font=("Courier New", 16), fg="#fff", bg="#222").pack(pady=5)
        tk.Label(self.master, text=f"O gewinnt: {self.stats['O']}", font=("Courier New", 16), fg="#fff", bg="#222").pack(pady=5)
        tk.Label(self.master, text=f"Unentschieden: {self.stats['Draws']}", font=("Courier New", 16), fg="#fff", bg="#222").pack(pady=5)
        # Joshua-Zitat zum Abschluss
        tk.Label(self.master, text=random_joshua_quote(), font=("Courier New", 14), fg="#0ff", bg="#222").pack(pady=10)
        tk.Button(self.master, text="Zurück zum Menü", font=("Courier New", 12), bg="#444", fg="#fff",
                  command=self.create_menu).pack(pady=20)

    def wopr_takeover(self):
        """Easter Egg: WOPR übernimmt den Bildschirm"""
        self.clear_window()
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
            "...",
            "Ergebnis: KEIN GEWINNER",
            "",
            "A strange game.",
            "The only winning move is not to play.",
            "",
            "WOPR empfiehlt: Lieber TicTacToe. 🎮",
            "",
            "— Joshua (und TARS, der das hier reingeschmuggelt hat)"
        ]
        for i, line in enumerate(lines):
            color = "#f00" if i == 0 or "DEFCON" in line else "#0f0"
            if "TARS" in line:
                color = "#0ff"
            tk.Label(self.master, text=line, font=("Courier New", 14),
                     fg=color, bg="#000", anchor="w").pack(anchor="w", padx=20)
        self.master.configure(bg="#000")
        tk.Button(self.master, text="[ENTER] Zurück zur Realität",
                  font=("Courier New", 12), bg="#333", fg="#0f0",
                  command=self.create_menu).pack(pady=20)

    def joshua_demo(self):
        # Easter Egg: Joshua spielt gegen sich selbst, zeigt Zitate
        self.mode = "joshua"
        self.stats = {"X": 0, "O": 0, "Draws": 0, "Games": 0}
        self.cvc_games = 3
        self.cvc_current_game = 0
        self.cvc_delay = 700
        self.cvc_prepare_game()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = TicTacToeGUI(root)
    root.mainloop()
