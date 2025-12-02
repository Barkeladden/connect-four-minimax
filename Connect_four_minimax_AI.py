# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 07:55:41 2024

@author: Barkn
"""

import sys
import pygame

# config
pygame.init()

WIDTH, HEIGHT = 588, 504
TILESIZE = WIDTH/7
FPS = 60

# Angir hvor mange trekk fremmover AI-en tenker
DEPTH = 3

# colors
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
LIGHT_GREY = (200, 200, 200)
RED = (220, 0, 0)
YELLOW = (255, 255, 50)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Connect 4')
clock = pygame.time.Clock()
turn = 0

board_state = [[0, 0, 0, 0, 0, 0], # 
               [0, 0, 0, 0, 0, 0], # 0 0 0 0 0 0 0 0 0
               [0, 0, 0, 0, 0, 0], # 0 0 0 0 0 0 0 0 0
               [0, 0, 0, 0, 0, 0], # 0 0 0 0 0 0 0 0 0
               [0, 0, 0, 0, 0, 0], # 0 0 0 0 0 0 0 0 0
               [0, 0, 0, 0, 0, 0], # 0 0 0 0 0 0 0 0 0
               [0, 0, 0, 0, 0, 0]] # 0 0 0 0 0 0 0 0 0

a= -1
board_background = []
for i in board_state:
    a+=1
    for y in range(len(i)):
        rect = pygame.Rect(a*TILESIZE, y*TILESIZE, TILESIZE,TILESIZE)
        board_background.append(rect)

        
def run():
    global board_state, turn
    while True:
        clock.tick(FPS)
        draw()
        if turn % 2 == 0:
            ai_column = ai_move()
            board_state = move(board_state, ai_column, 1)
            draw()
            if win_check(board_state) == 1:
                win(1)
            turn += 1
        events()
        

def events():
    global board_state, turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn % 2 != 0:
            old_board = [col[:] for col in board_state]
            board_state = move(board_state, mouse(), 2)
            turn += 1
            if old_board == board_state:  
                turn -= 1
            draw()
            if win_check(board_state) == 1: win(1)
            elif win_check(board_state) == 2: win(2)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset()
            return 'reset'
def draw():
    screen.fill(GREY)
    
    for i in board_background:
        pygame.draw.ellipse(screen, WHITE, i)
    
    a = -1
    for i in board_state:
        a += 1
        for y in range(6):
            if i[y] == 1:
                rect = pygame.Rect(a*TILESIZE, y*TILESIZE, TILESIZE,TILESIZE)
                pygame.draw.ellipse(screen, RED, rect)
            elif i[y] == 2:
                rect = pygame.Rect(a*TILESIZE, y*TILESIZE, TILESIZE,TILESIZE)
                pygame.draw.ellipse(screen,YELLOW, rect)
    
    show_move()
    
    pygame.display.flip()
    
def win_check(board):
    
    # vertikal
    for colum in board:
        red_in_row = 0
        yellow_in_row = 0
        for i in colum:
            if i == 1: 
                red_in_row += 1
                yellow_in_row = 0
                if red_in_row > 3: return 1
            elif i == 2: 
                yellow_in_row += 1
                red_in_row = 0
                if yellow_in_row > 3: return 2
            else:
                red_in_row = 0
                yellow_in_row = 0
    
    # horisontal
    rows = []
    for i in range(len(board)-1):
        r = []
        for colum in board:
            r.append(colum[i])
        rows.append(r)
    for row in rows:
        red_in_row = 0
        yellow_in_row = 0
        for i in row:
            if i == 1: 
                red_in_row += 1
                yellow_in_row = 0
                if red_in_row > 3: return 1
            elif i == 2: 
                yellow_in_row += 1
                red_in_row = 0
                if yellow_in_row > 3: return 2
            else:
                red_in_row = 0
                yellow_in_row = 0
                
    
    # diagonal
    for n in range(4):
       for i in range(3, 6):
           if board[n][i] == board[n+1][i-1] and board[n+1][i-1] == board[n+2][i-2] and board[n+2][i-2] == board[n+3][i-3]:
               if board[n][i] != 0:
                        return board[n][i]
           i -= 3 
           if board[n][i] == board[n+1][i+1] and board[n+1][i+1] == board[n+2][i+2] and board[n+2][i+2] == board[n+3][i+3]:
               if board[n][i] != 0:
                        return board[n][i]
    # draw
    if board[0].count(0) == 0 and board[1].count(0) == 0 and board[2].count(0) == 0 and board[3].count(0) == 0 and board[4].count(0) == 0 and board[5].count(0) == 0 and board[6].count(0) == 0: return 0
    
    return None
def reset():
    global board_state
    board_state = [[0, 0, 0, 0, 0, 0],  
                   [0, 0, 0, 0, 0, 0], 
                   [0, 0, 0, 0, 0, 0], 
                   [0, 0, 0, 0, 0, 0], 
                   [0, 0, 0, 0, 0, 0], 
                   [0, 0, 0, 0, 0, 0], 
                   [0, 0, 0, 0, 0, 0]] 

def win(state=0):
    font = pygame.font.SysFont(None, 45)
    draw = font.render('Draw!!', True, RED)
    red = font.render('Red won!!', True, RED)
    yellow = font.render('Yellow won!!', True, RED)
    
    if state == 1: text = red
    elif state == 2: text = yellow
    else: text = draw
    go = True
    back = pygame.Rect(WIDTH/3, 20, 200, 45)
    while go:
       # screen.fill(GREY)
       
       pygame.draw.rect(screen, WHITE, back)
       screen.blit(text, (WIDTH/3, 20))
       if events() == 'reset':
           go = False
       
       pygame.display.flip()
def mouse():
    x_pos, y_pos = pygame.mouse.get_pos()
    return int(x_pos//TILESIZE)

def show_move():
    x = mouse()
    y = board_state[x].count(0) - 1
    rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE,TILESIZE)
    pygame.draw.ellipse(screen, LIGHT_GREY, rect)

def move(board, colum, player):
    if board[colum].count(0) > 0:
        if player == 1:
                board[colum].pop(0)
                board[colum].insert(board[colum].count(0), 1)
        elif player == 2:
            board[colum].pop(0)
            board[colum].insert(board[colum].count(0), 2)
    return board

def evaluation(board):
    points = 0
    if win_check(board) == 1: points += 100
    if win_check(board) == 2: points -= 100
    
    for n in range(4):
       for i in range(3, 6):
           if board[n][i] == board[n+1][i-1] and board[n+1][i-1] == board[n+2][i-2] and board[n+3][i-3] == 0:
               if board[n][i] == 1: points += 10
               elif board[n][i] == 2: points -= 10
           i -= 3 
           if board[n][i] == board[n+1][i+1] and board[n+1][i+1] == board[n+2][i+2] and board[n+3][i+3] == 0:
               if board[n][i] == 1: points += 10
               elif board[n][i] == 2: points -= 10
    
    for n in range(4):
       for i in range(3, 6):
           if board[n][i] == board[n+1][i-1] and board[n+2][i-2] == 0 and board[n+3][i-3] == 0:
               if board[n][i] == 1: points += 5
               elif board[n][i] == 2: points -= 5
           i -= 3 
           if board[n][i] == board[n+1][i+1] and board[n+2][i+2] == 0 and board[n+3][i+3] == 0:
               if board[n][i] == 1: points += 5
               elif board[n][i] == 2: points -= 5
    

    for colum in board:
        for i in range(5, 2, -1):
            if colum[i] == colum[i-1] and colum[i-1] == colum[i-2] and colum[i-3] == 0:
                if colum[i] == 1: points += 10
                elif colum[i] == 2: points -= 10 
            elif colum[i] == colum[i-1] and colum[i-2] == 0 and colum[i-3] == 0:
                if colum[i] == 1: points += 5
                elif colum[i] == 2: points -= 5
                

            
    
    for i in board[3]:
        if i == 1: points += 1
        if i == 2: points -= 1
    
    rows = []
    for i in range(len(board)-1):
        r = []
        for colum in board:
            r.append(colum[i])
        rows.append(r)
    for row in rows:
        for i in range(4):
            if row[i] == row[i+1] and row[i+1] == row[i+2] and row[i+3] == 0:
                if row[i] == 1: points += 10
                elif row[i] == 2: points -= 10
            elif row[i] == row[i+1] and row[i+2] == 0 and row[i+3] == 0:
                if row[i] == 1: points += 5
                elif row[i] == 2: points -= 5
            
            if row[6-i] == row[5-i] and row[5-i] == row[4-i] and row[3-i] == 0:
                if row[6-i] == 1: points += 10
                elif row[6-i] == 2: points -= 10
            elif row[6-i] == row[5-i] and row[4-i] == 0 and row[3-i] == 0:
                if row[i] == 1: points += 5
                elif row[i] == 2: points -= 5
    return points

def ai_move():
    best_score = -99999
    best_col = None
    alpha = -99999
    beta = 99999
    for col in range(7):
        if board_state[col].count(0) > 0:
            temp_board = [row[:] for row in board_state]
            temp_board = move(temp_board, col, 1)
            score = minimax(temp_board, DEPTH, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_col = col
            alpha = max(alpha, score)
    print(best_score)
    return best_col

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or win_check(board) != None:
        return evaluation(board)

    valid_moves = [col for col in range(7) if board[col].count(0) > 0]

    if maximizing_player:
        max_eval = -99999
        for col in valid_moves:
            temp_board = [row[:] for row in board]
            temp_board = move(temp_board, col, 1)
            eval_score = minimax(temp_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = 99999
        for col in valid_moves:
            temp_board = [row[:] for row in board]
            temp_board = move(temp_board, col, 2)
            eval_score = minimax(temp_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

run()

