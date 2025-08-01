import pytest

# Passe den Importpfad ggf. an, falls das Hauptmodul anders heißt!
from tic_tac_toe_v1.3 import check_winner, create_board, computer_move

def test_check_winner_row():
    board = [
        ['X', 'X', 'X'],
        [' ', 'O', 'O'],
        [' ', ' ', ' ']
    ]
    assert check_winner(board) == 'X'

def test_check_winner_column():
    board = [
        ['O', 'X', ' '],
        ['O', 'X', ' '],
        ['O', ' ', 'X']
    ]
    assert check_winner(board) == 'O'

def test_check_winner_diagonal():
    board = [
        ['X', 'O', 'O'],
        [' ', 'X', ' '],
        ['O', ' ', 'X']
    ]
    assert check_winner(board) == 'X'

def test_check_winner_none():
    board = [
        ['X', 'O', 'X'],
        ['O', 'X', 'O'],
        ['O', 'X', 'O']
    ]
    assert check_winner(board) is None

def test_computer_move_places_marker():
    board = create_board()
    result = computer_move(board, player='O')
    assert result is True
    assert sum(cell == 'O' for row in board for cell in row) == 1
