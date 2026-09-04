import numpy as np 
import pygame
import random
import math

board = np.zeros((6,7))
turn = 0
BACK_GREY = (169, 169, 169)
DIMGREY = (105, 105, 105)
BLUE = (63,71,150)
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
YELLOW = (252, 186, 3)
RED = (255, 0, 0)
WIN = pygame.display.set_mode((770, 660))

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

def create_board():
    WIN.fill(BACK_GREY)
    for i in range(42):
        x = i%7
        y = i//7
        pos = (110*x+55, 110*y+55)
        if board[y][x] == 1:
            pygame.draw.circle(WIN, YELLOW, pos, int(85/2))
        elif board[y][x] == 2:
            pygame.draw.circle(WIN, RED, pos, int(85/2))
        else:
            pygame.draw.circle(WIN, DIMGREY, pos, int(85/2))
        pygame.draw.rect(WIN, DIMGREY, (110*x,110*y,110,110), 5)
    pygame.display.update()

def possible_moves(board):
    possible_moves = []
    for col in range(7):
        if board[0][col] == 0:
            possible_moves.append(col)
    return possible_moves

def play():
    pos_x = 0
    if side == 1: 
        played = False 
        old_col = -1
        while not played:
            pos_x, pos_y = pygame.mouse.get_pos()
            col = pos_x//110
            if col != old_col:
                create_board()
                #hoverrow
                try_move = pygame.Surface((105,105))
                try_move.fill(BACK_GREY)
                try_move.set_alpha(150)
                y = 6
                for i in range(6):
                    if board[i][col] == 0:
                        y = i
                pygame.draw.circle(try_move, YELLOW, (53,53), int(85/2))
                WIN.blit(try_move, (110*col+5/2, 110*(y)+5/2))
                #hovercol
                john = pygame.Surface((110, 770))
                john.fill(YELLOW)
                john.set_alpha(40)
                WIN.blit(john, (110*col, 0))
                old_col = col
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    played = True
        if col in possible_moves(board):
            set_piece(board, 1, col)
        else:
            play()
    else:
        col, score = minimax(board, 4, True)
        print(score)
        set_piece(board, 2, col)
    create_board()

def set_piece(board, value, x):
    y = 0
    for i in range(6):
        if board[i][x] == 0:
            y = i
    board[y][x] = value

#ai
def evaluate_window(window, score):
    if window.count(2) == 4:
        score += 10000000000000
    elif window.count(2) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(2) == 2 and window.count(0) == 2:
        score += 2
    if window.count(1) == 3 and window.count(0) == 1:
        score -= 600000000000000000
    return score

def board_value(board):
    score = 0

    for c in range(7):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(3):
            window = col_array[r:r+4]
            score = evaluate_window(window, score)
    
    for r in range(6):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(4):
            window = row_array[c:c+4]
            score = evaluate_window(window, score)
    
    for r in range(3):
        for c in range(4):
            window = [board[r+i][c+i] for i in range(4)]
            score = evaluate_window(window, score)
    for r in range(3):
        for c in range(4):
            window = [board[r+3-i][c+i] for i in range(4)]
            score = evaluate_window(window, score)
    return score

def minimax(board, depth, maximizing_player):
    win_1 = check_win(1,board)[0]
    win_2 = check_win(2, board)[0]
    best_score = -math.inf
    best_move = random.choice(possible_moves(board))
    if depth == 0 or win_1 or win_2 or len(possible_moves(board)) == 0:
        if win_2:
            return (None, 1000000000000000000000)
        elif win_1:
            return (None, -1000000000000000000000)
        elif depth == 0:
            return (None, board_value(board))
        else:
            return (None, 0)
    else:
        if maximizing_player:            
            for col in possible_moves(board):
                test_board = board.copy()
                set_piece(test_board, 2, col)
                score = minimax(test_board, depth-1, False)[1]
                if score > best_score:
                    best_move = col
                    best_score = score
            return best_move, best_score
        else: #minimazing player
            best_score = math.inf
            for col in possible_moves(board):
                test_board = board.copy()
                set_piece(test_board, 1, col)
                score = minimax(test_board, depth-1, True)[1]
                if score < best_score:
                    best_move = col
                    best_score = score
            return (best_move, best_score) 

#main loop
for i in range(42):
    turn += 1
    side = turn%2+1
    print(board)
    play()
    pygame.display.update()
    if check_win(side, board)[0]:
        create_board()
        for i in range(1, 5):
            r,c = check_win(side, board)[i]
            pygame.draw.circle(WIN, WHITE, (110*c+55, 110*r+55), 35, int(5/2))
        pygame.display.update()
        print("player " + str(side) + " wins")
        pygame.time.wait(2500)
        break
if not possible_moves(board):
    print("the board is full")
print(board)
pygame.quit()