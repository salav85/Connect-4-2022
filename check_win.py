import pygame

def check_win(piece, board):
#check vertical
    for c in range(7):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece  and board[r+3][c] == piece:
                return (True, (r,c), (r+1,c), (r+2,c), (r+3,c))
#check horrisontal
    for c in range(4):
        for r in range(6):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return (True, (r,c), (r,c+1), (r,c+2), (r,c+3))
#check diago. vers haut
    for c in range(4):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return (True, (r,c), (r+1,c+1), (r+2,c+2), (r+3,c+3))
# Check diago vers bas
    for c in range(4):
        for r in range(3, 6):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return (True, (r,c), (r-1,c+1), (r-2,c+2), (r-3,c+3))
    return (False, None)