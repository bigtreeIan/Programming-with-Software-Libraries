###Name: Yihan Xu
###ID: 47011405
###project 5
###game logic


###create a list to represent the col in every row
###then append the original discs to the list

def original_board_list(row_num, col_num, top_left):
    board_list = []
    for row in range(row_num):
        board_list.append([])
        for col in range(col_num):
            board_list[-1].append('NONE')
    line_left_right = int((col_num - 2) // 2) 
    line_up_down = int((row_num - 2) // 2)
    if top_left == 'B':
        board_list[line_up_down][line_left_right] = 'B'
        board_list[line_up_down][line_left_right + 1] = 'W'
        board_list[line_up_down + 1][line_left_right] = 'W'
        board_list[line_up_down + 1][line_left_right + 1] = 'B'
    elif top_left == 'W':
        board_list[line_up_down][line_left_right] = 'W'
        board_list[line_up_down][line_left_right + 1] = 'B'
        board_list[line_up_down + 1][line_left_right] = 'B'
        board_list[line_up_down + 1][line_left_right + 1] = 'W'
    return board_list

###switch turn
def who_turn(turn):
    if turn == 'B':
        return 'W'
    elif turn == 'W':
        return 'B'
    
###count black
def how_many_black(board):
    sum_black = 0
    for i in board:
        for j in i:
            if j == 'B':
                sum_black += 1
    return sum_black

###count white
def how_many_white(board):
    sum_white = 0
    for i in board:
        for j in i:
            if j == 'W':
                sum_white += 1
    return sum_white

###count black
def how_many_zero(board):
    sum_zero = 0
    for i in board:
        for j in i:
            if j == 'NONE':
                sum_zero += 1
    return sum_zero

###determine whether there is a winner
def win_condition(current_board, win_option, row_num, col_num, zero, turn):
    black_num = how_many_black(current_board)
    white_num = how_many_white(current_board)
    move = check_opposite_move(turn, current_board, row_num, col_num, zero)
    if zero != 0:
        if move == -1:
            if black_num > white_num:
                winner = 'B'
                return winner
            elif white_num > black_num:
                winner = 'W'
                return winner
        else:
            winner = 'NONE'
            return winner
            
        
    elif zero == 0:
        if win_option == '>':
            if black_num > white_num:
                winner = 'B'
                return winner
            elif white_num > black_num:
                winner = 'W'
                return winner
            elif white_num == black_num:
                winner = 'NONE'
                return winner
        elif win_option == '<':
            if black_num < white_num:
                winner = 'B'
                return winner
            elif white_num < black_num:
                winner = 'W'
                return winner
            elif white_num == black_num:
                winner = 'NONE'
                return winner

###check if there is a valid move and if there is one, append all the position
###that need to be switch color to list
def check_move(row_new, col_new, board_list, row_num, col_num, turn):
    if row_new <= row_num - 1 and col_new <= col_num - 1:
        if board_list[row_new][col_new] != 'NONE':
            valid_list = []
            return valid_list
        elif board_list[row_new][col_new] == 'NONE':
            valid_list = []
            another_color = 0
            #LEFT
            try:
                if row_new >= 0 and col_new - 1 >= 0 and board_list[row_new][col_new - 1] == who_turn(turn):
                    col_l = col_new - 1
                    for col in range(col_l):                      
                        another_color = another_color + 1
                        col_l = col_l - 1
                        if col_l >= 0 and board_list[row_new][col_l] == turn:
                            for i in range(another_color + 1):
                                valid_list.append([row_new, col_new - i])
                            break
            except:
                pass
            another_color = 0
            #RIGHT
            try:
                if row_new >= 0 and col_new + 1 >= 0 and board_list[row_new][col_new + 1] == who_turn(turn):
                    col_r = col_new + 1
                    for col in range(col_num - col_r):
                        another_color = another_color + 1
                        col_r = col_r + 1
                        if col_r >= 0 and board_list[row_new][col_r] == turn:
                            for i in range(another_color + 1):
                                valid_list.append([row_new, col_new + i])
                            break
            except:
                pass
            another_color = 0
            #UP
            try:
                if row_new - 1 >= 0 and col_new >= 0 and board_list[row_new - 1][col_new] == who_turn(turn):
                    row_u = row_new - 1
                    for row in range(row_new - 1):
                        another_color = another_color + 1
                        row_u = row_u - 1
                        if row_u >= 0 and board_list[row_u][col_new] == turn:
                            for i in range(another_color + 1):
                                valid_list.append([row_new - i, col_new])
                            break
            except:
                pass
            another_color = 0
            #DOWN
            try:
                if board_list[row_new + 1][col_new] == who_turn(turn):
                    row_d = row_new + 1
                    for row in range(row_num - row_new - 1):
                        another_color = another_color + 1
                        row_d = row_d + 1
                        if row_d >= 0 and board_list[row_d][col_new] == turn:
                            for i in range(another_color + 1):
                                valid_list.append([row_new + i, col_new])
                            break
            except:
                pass
            another_color = 0
            
            try:               
                if row_new - 1>= 0 and col_new + 1 >= 0 and board_list[row_new - 1][col_new + 1] == who_turn(turn):
                    row_ur = row_new - 1
                    col_ur = col_new + 1
                    for j in range(row_new - 1):
                        another_color = another_color + 1
                        row_ur = row_ur - 1
                        col_ur = col_ur + 1
                        if row_ur >= 0 and col_ur >= 0 and board_list[row_ur][col_ur] == turn:
                            for i in range(another_color + 1):
                                valid_list.append([row_new - i, col_new + i])
                            break
            except:
                pass
            another_color = 0
            
            try:
                if row_new - 1>= 0 and col_new - 1 >= 0 and board_list[row_new - 1][col_new - 1] == who_turn(turn):
                    row_ul = row_new - 1
                    col_ul = col_new - 1
                    for j in range(row_new - 1):
                        another_color = another_color + 1
                        row_ul = row_ul - 1
                        col_ul = col_ul - 1
                        if row_ul >= 0 and col_ul >= 0 and board_list[row_ul][col_ul] == turn:
                            for i in range(another_color + 1):
                                valid_list.append([row_new - i, col_new - i])
                            break
            except:
                pass
            another_color = 0
            
            try:
                if row_new + 1 >= 0 and col_new - 1 >= 0 and board_list[row_new + 1][col_new - 1] == who_turn(turn):
                    row_dl = row_new + 1
                    col_dl = col_new - 1
                    for j in range(row_num - row_new - 1):
                        another_color = another_color + 1
                        row_dl = row_dl + 1
                        col_dl = col_dl - 1
                        if row_dl >= 0 and col_dl >= 0 and board_list[row_dl][col_dl] == turn:
                            for i in range(another_color + 1):
                                valid_list.append([row_new + i, col_new - i])
                            break
            except:
                pass
            another_color = 0
            
            try:                
                if row_new + 1>= 0 and col_new + 1 >= 0 and board_list[row_new + 1][col_new + 1] == who_turn(turn):
                    row_dr = row_new + 1
                    col_dr = col_new + 1
                    for j in range(row_num - row_new - 1):
                        another_color = another_color + 1
                        row_dr = row_dr + 1
                        col_dr = col_dr + 1
                        if row_dr >= 0 and col_dr >= 0 and board_list[row_dr][col_dr] == turn:
                            for i in range(another_color + 1):
                                valid_list.append([row_new + i, col_new + i])
                            break
            except:
                pass
            return valid_list

###change the color of the discs that in the list that need to be changed
def change_color(board, valid_list, turn):
    for rc_pair in valid_list:
        row, col = rc_pair
        board[int(row)][int(col)] = turn
    return board

###check for the gotcha condition, if the opposite cannot move, return -1
def check_opposite_move(turn, board, row_num, col_num, zero):
    empty_position_list = _empty_position(board)
    valid = []
    for position in range(zero):
        empty_row, empty_col = empty_position_list[position]
        valid = valid + check_move(empty_row, empty_col, board, row_num, col_num, turn)
    if valid != []:
        move = 1
        return move
    elif valid == []:
        move = -1
        return move

###get the row/col of all the empty position    
def _empty_position(board):
    empty_position_list = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'NONE':
                empty_position_list.append([i,j])
    return empty_position_list

class Game_Over_Error(Exception):
    def transfer(self):
        print('WINNER', winner)
        
class Invalid_Move_Error(Exception):
    def transfer(self):
        print('INVALID')
        
class Input_error(Exception):
    def transfer(self):
        print('INVALID INPUT')
