###Name: Yihan Xu
###ID: 47011405
###hw4
###user interface

import game_logic

###ask the row number of the board
def ask_row():
    while True:
        try:
            row_num = int(input())
            if row_num >= 4 and row_num <= 16 and row_num % 2 == 0:
                return row_num
                break
            else:
                continue
        except:
            continue

###ask the column number of the board
def ask_col():
    while True:
        try:
            col_num = int(input())
            if col_num >= 4 and col_num <= 16 and col_num % 2 == 0:
                return col_num
                break
            else:
                continue
        except:
            continue
        
###ask which one move first
def first_move():
    while True:
        try:
            first_move = input()
            if first_move == 'B' or first_move == 'W':
                return first_move
                break
            else:
                continue
        except:
            continue

###ask which one is in the top left position
def original_position():
    while True:
        try:
            top_left = input()
            if top_left == 'B':
                return 'B'
                break
            elif top_left == 'W':
                return 'W'
                break
            else:
                continue
        except:
            continue

###ask how the game win
def how_game_win():
    while True:
        try:
            win_option = input()
            if win_option == '>' or win_option == '<':
                return win_option
                break
            else:
                continue
        except:
            continue

###print the board
def print_board(original_board_list, row_num, col_num, turn):
    black = game_logic.how_many_black(original_board_list)
    white = game_logic.how_many_white(original_board_list)
    print('B: ', black, ' ', 'W: ', white)
    for i in range(row_num):
        for j in range(col_num):
            if original_board_list[i][j] == 'NONE':
                print('.', ' ', end='')
            elif original_board_list[i][j] == 'B':
                print('B', ' ', end='')
            elif original_board_list[i][j] == 'W':
                print('W', ' ', end='')
        print('\n')

###ask which row and col users want to put       
def which_row_col(row_num, col_num):
    while True:
        row_col = input().split()
        if len(row_col) == 2:
            row = int(row_col[0])
            col = int(row_col[1])
            if row > 0 and row <= row_num and col > 0 and col <= col_num:
                return row, col
                break
            else:
                continue
        else:
            continue

def main():
    ###get all the varible that needed
    row_num = ask_row()
    col_num = ask_col()
    turn = first_move()
    top_left = original_position()
    win_option = how_game_win()
    board = game_logic.original_board_list(row_num, col_num, top_left)
    print_board(board, row_num, col_num, turn)
    print('TURN:', turn)
    while True:
        row, col = which_row_col(row_num, col_num)
        row_new = row - 1
        col_new = col - 1
        valid_list = game_logic.check_move(row_new, col_new, board, row_num, col_num, turn)
        if valid_list != []:
            board = game_logic.change_color(board, valid_list, turn)
            turn = game_logic.who_turn(turn)
            print('VALID')
            print_board(board, row_num, col_num, turn)
            zero_num = game_logic.how_many_zero(board)
            winner = game_logic.win_condition(board, win_option)
            if winner == 'NONE' and zero_num != 0:
                pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
            elif winner == 'NONE' and zero_num == 0:
                print('WINNER: ', 'NONE')
                break
            elif winner == 'B':
                print('WINNER: ', 'B')
                break
            elif winner == 'W':
                print('WINNER: ', 'W')
                break
            ###make whatever changes
            ###flip the turn
            ###if there is no move for the current player:
            ###flip the turn
            ###if there is no move for the current player:
            ###game is over
            move = game_logic.check_opposite_move(turn, board, row_num, col_num, zero_num)
            if move == 1:
                print('TURN:', turn)
                continue
            elif move == -1:
                turn = game_logic.who_turn(turn)
                move1 = game_logic.check_opposite_move(turn, board, row_num, col_num, zero_num)
                if move1 == 1:
                    print('TURN:', turn)
                    continue
                elif move1 == -1:
                    winner = game_logic.win_condition(board, win_option)
                    if winner == 'NONE':
                        print('WINNER: ', 'NONE')
                        break
                    elif winner == 'B':
                        print('WINNER: ', 'B')
                        break
                    elif winner == 'W':
                        print('WINNER: ', 'W')
                        break
        elif valid_list == []:
            print('INVALID')
            continue
        
if __name__ == '__main__':
    main()
