# Tic Tac Toe Game v1.1
# designed by:
#   ██████  ██       ██  ██    ██ ███████ ██████  
#  ██    ██ ██       ██  ██    ██ ██      ██   ██ 
#  ██    ██ ██       ██  ██    ██ █████   ██████  
#  ██    ██ ██       ██   ██  ██  ██      ██   ██ 
#   ██████  ███████  ██    ████   ███████ ██   ██ 

import random
import time
from pyfiglet import Figlet

# You can control the size by adjusting the width parameter
# Smaller width (e.g., 80) for smaller text, larger width (e.g., 200) for larger text
f = Figlet(font='block', width=120)  # Increased size
print(f.renderText('TIC TAC TOE'))
# For even bigger text, you can use a font that's naturally larger
# big_f = Figlet(font='starwars', width=150)  # Alternative larger font
# print(big_f.renderText('TICTACTOE'))

# create board
def create_board():
    board = []
    for i in range(3):
        row = [' ', ' ', ' ']
        board.append(row)
    return board

# display board
def print_board(board):
    for i in board:
        print('|'.join(i))
        print('-' * 5)
# for testing ---> print_board(create_board()) - result = so far so good :-)

# make move
def make_move(board, row, col, player):
    if board[row][col] == ' ':
        board[row][col] = player
        return True
    else:
        print("Invalid move! Cell already taken.")
        return False
# check
def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    return None  # No winner yet

# radom entry by the computer
def random_move(board, player):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = player
        return True
    return False

def play_tic_tac_toe():
    board = create_board()
    current_player = 'X'
    moves_count = 0
    
    # Ask if the player wants to play against the computer
    play_against_computer = input("Do you want to play against the computer? (y/n): ").lower() == 'y'

    while True:
        print_board(board)
        
        if current_player == 'X' or not play_against_computer:
            # Human player's turn
            while True:  # Loop until a valid move is made
                try:
                    row = int(input(f'Player {current_player}, please input the row (0-2): '))
                    col = int(input(f'Player {current_player}, please input the column (0-2): '))

                    if 0 <= row <= 2 and 0 <= col <= 2:
                        if make_move(board, row, col, current_player):
                            moves_count += 1
                            break 
                    else:
                        print('Input is not correct! Please provide number from 0 to 2.')
                except ValueError:
                    print('Input is not correct! Please provide a valid number.')
        else:
            # Computer's turn
            print("Computer's turn (Player O)...")
            # Add a slight delay to make it feel more natural
            time.sleep(1)
            
            if random_move(board, current_player):
                print(f"Computer placed an 'O'")
                moves_count += 1
        
        # Check if game is over
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == 'O' and play_against_computer:
                print('Computer wins! Better luck next time!')
            else:
                print(f'Player {winner} has won! Congratulations!')
            break
        
        # Check for draw
        if moves_count == 9:
            print_board(board)
            print('Draw! Game over!')
            break

        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'
        
play_tic_tac_toe()