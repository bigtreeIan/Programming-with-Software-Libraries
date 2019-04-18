###Using of class

class info:
    def row_input(self):
        while True:
            self.row_num = input('Please input total row number: ')
            if self.row_num >= 4 and type(self.row_num) == int:
                break
            else:
                continue
            
    def col_input(self):
        while True:
            self.col_num = input('Please input total column number: ')
            if self.col_num >= 4 and type(self.col_num) == int:
                break
            else:
                continue
            
    def move_option(self):
        while True:
            self.who_move_first = input('Please input the first move: ')
            if self.who_move_first == 'B' or self.who_move_first == 'W':
                break
            else:
                continue
            
    def top_left_position(self):
        while True:
            self.top_left = input('Please input the top left position: ')
            if self.top_left == 'B' or self.top_left == 'W':
                break
            else:
                continue
            
    def win_option(self):
        while True:
            self.win_condition = input('Please input the win condition: ')
            if self.win_condition == '>' or self.win_condition == '<':
                break
            else:
                continue
            

class game_board:
    def __init__(self):
        self.board_list = []
        for row in range(self.row_num):
            self.board_list.append([])
            for col in range(self.col_num):
                self.board_list[-1].append('NONE')
        self.line_left_right = int((self.col_num - 2) // 2) 
        self.line_up_down = int((self.row_num - 2) // 2)
        if self.top_left == 'B':
            self.board_list[self.line_up_down][self.line_left_right] = 'B'
            self.board_list[self.line_up_down][self.line_left_right + 1] = 'W'
            self.board_list[self.line_up_down + 1][self.line_left_right] = 'W'
            self.board_list[self.line_up_down + 1][self.line_left_right + 1] = 'B'
        elif self.top_left == 'W':
            self.board_list[self.line_up_down][self.line_left_right] = 'W'
            self.board_list[self.line_up_down][self.line_left_right + 1] = 'B'
            self.board_list[self.line_up_down + 1][self.line_left_right] = 'B'
            self.board_list[self.line_up_down + 1][self.line_left_right + 1] = 'W'
            
