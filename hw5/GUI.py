###Name: Yihan Xu
###ID: 47011405
###project 5
###Ogame Gui


import tkinter
import game_logic
import math



FONT1 = ('Helvetica', 10)
FONT2 = ('Helvetica', 20)

class OGame:
    def __init__(self):
        self._enter_button = False
        self._root_window = tkinter.Tk()
        self._root_window.title('Othello Game')
        
        ###create canvas
        self._canvas = tkinter.Canvas(master = self._root_window,
                                      width = 400,
                                      height = 400,
                                      background = '#87CEEB')
        
        ###create input button, which let users click and enter the legal input
        input_button = tkinter.Button(master = self._root_window,
                                      text = 'Click here to enter your option',
                                      font = FONT1,
                                      command = self._click_input_button)
        
        ###set where my canvas should show in the window
        self._canvas.grid(row = 0, column = 0,
                          padx = 20, pady = 40,
                          sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        
        ###set where my input button should show in the window
        input_button.grid(row = 0, column = 0,
                          padx = 10, pady = 10,
                          sticky = tkinter.S + tkinter.E)
        
        ###make the row and column change as resize the window change
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

        ###everytime user resize the window, the event happen and resize all the things
        self._root_window.bind('<Configure>', self._resize)
        self._root_window.bind('<Button-1>', self._drop)


    def start(self):
        
        ###start the Ogame
        self._root_window.mainloop()

    def _resize(self, event):

        ###only when the input button was clicked, resize the line and discs
        if self._enter_button == True:
            self._canvas.delete(tkinter.ALL)
            self._print_board()
            self.draw_discs()

        ###when input button is not clicked, resize the canvas
        elif self._enter_button == False:
            self._canvas.delete(tkinter.ALL)
            
        
    def _drop(self, event):

        ###when enter button and start button are both clicked,
        ###and the click is inside the canvas, start drop discs.
        if self._enter_button == True:
            if self._input.start_game == True:
                if event.x / self.actual_width >= 0 and event.x / self.actual_width <= 1 and event.y / self.actual_height >= 0 and event.y / self.actual_height <= 1:

                    ###calculate the unit height and width of each rectangle 
                    self.unit_height = self.actual_height / self.total_row_number
                    self.unit_width = self.actual_width / self.total_col_number

                    ###calculate the row and col that in the board list that I need to drop
                    self.drop_row = int(event.y // self.unit_height)
                    self.drop_col = int(event.x // self.unit_width)

                    ###check if it is a valid move, return a valid list
                    self.valid_list = game_logic.check_move(self.drop_row,
                                                            self.drop_col,
                                                            self.board_list,
                                                            self.total_row_number,
                                                            self.total_col_number,
                                                            self.move_option)
                    
                    ###if there is a valid move, check win and check the special case
                    if self.valid_list != []:
                        self.board_list = game_logic.change_color(self.board_list, self.valid_list, self.move_option)
                        self.move_option = game_logic.who_turn(self.move_option)
                        self.black_num = game_logic.how_many_black(self.board_list)
                        self.show_black = tkinter.Label(master = self._root_window,
                                                        text = 'Black: ' + str(self.black_num),
                                                        font = FONT2)
                
                        self.white_num = game_logic.how_many_white(self.board_list)
                        self.show_white = tkinter.Label(master = self._root_window,
                                                        text = 'White: ' + str(self.white_num),
                                                        font = FONT2)
                        
                        self.zero_number = game_logic.how_many_zero(self.board_list)
                        move = game_logic.check_opposite_move(self.move_option, self.board_list, self.total_row_number, self.total_col_number, self.zero_number)
                        if move == 1:
                            self.show_turn = tkinter.Label(master = self._root_window,
                                                           text = 'Turn: ' + self.move_option,
                                                           font = FONT2)
                        else:
                            self.show_turn = tkinter.Label(master = self._root_window,
                                                           text = 'Turn: ' + game_logic.who_turn(self.move_option),
                                                           font = FONT2)
                            
                        self.show_black.grid(row = 3, column = 5,
                                             padx = 5, pady = 5,
                                             sticky = tkinter.S)
                        self.show_white.grid(row = 5, column = 5,
                                             padx = 5, pady = 5,
                                             sticky = tkinter.S)
                        self.show_turn.grid(row = 0, column = 5,
                                            padx = 5, pady = 5,
                                            sticky = tkinter.N)
                        self.draw_discs()
                        
                        self.zero_number = game_logic.how_many_zero(self.board_list)
                        
                        winner = game_logic.win_condition(self.board_list, self.win_option, self.total_row_number, self.total_col_number, self.zero_number, self.move_option)
                        if winner == 'B' and self.zero_number == 0:
                            win_window_b = winner_window(winner)
                            return
                        elif winner == 'W' and self.zero_number == 0:
                            win_window_w = winner_window(winner)
                            return
                        elif winner == 'NONE' and self.zero_number == 0:
                            win_window_n = winner_window(winner)
                            return
                            
                        self.zero_number = game_logic.how_many_zero(self.board_list)
                        move = game_logic.check_opposite_move(self.move_option, self.board_list, self.total_row_number, self.total_col_number, self.zero_number)
                        if move == -1:
                            self.move_option = game_logic.who_turn(self.move_option)
                            move1 = game_logic.check_opposite_move(self.move_option, self.board_list, self.total_row_number, self.total_col_number, self.zero_number)
                            if move1 == -1:
                                winner = game_logic.win_condition(self.board_list, self.win_option, self.total_row_number, self.total_col_number, self.zero_number, self.move_option)
                                if winner == 'B':
                                    win_window_b = winner_window(winner)
                                elif winner == 'W':
                                    win_window_w = winner_window(winner)
                                elif winner == 'NONE':
                                    win_window_n = winner_window(winner)
                                    
                    else:
                        invalid_window_pop = invalid_window()
                    
    def _click_input_button(self):
        
        ###after user click enter button, pop a window in the top and ask infomation
        self._input = Input_window()
        self._input.not_yet()

        ###only when the game is start, get the information from the window
        if self._input.start_game == True:
            self._enter_button = True
            self.total_row_number = self._input.total_row
            self.total_col_number = self._input.total_col
            self.move_option = self._input.first_turn
            self.top_left_disc = self._input.top_left_color
            self.win_option = self._input.how_to_win
            self.board_list = game_logic.original_board_list(self.total_row_number,
                                                             self.total_col_number,
                                                             self.top_left_disc)            


            self.black_num1 = game_logic.how_many_black(self.board_list)
            self.show_black1 = tkinter.Label(master = self._root_window,
                                             text = 'Black: ' + str(self.black_num1),
                                             font = FONT2)
            
            self.white_num1 = game_logic.how_many_white(self.board_list)
            self.show_white1 = tkinter.Label(master = self._root_window,
                                             text = 'White: ' + str(self.white_num1),
                                             font = FONT2)
            self.show_turn1 = tkinter.Label(master = self._root_window,
                                            text = 'Turn: ' + self.move_option,
                                            font = FONT2)
            self.show_black1.grid(row = 3, column = 5,
                                  padx = 5, pady = 5,
                                  sticky = tkinter.S)
            self.show_white1.grid(row = 5, column = 5,
                                  padx = 5, pady = 5,
                                  sticky = tkinter.S)
            self.show_turn1.grid(row = 0, column = 5,
                                 padx = 5, pady = 5,
                                 sticky = tkinter.N)
            self._print_board()
            self.draw_discs()
            
    def _print_board(self):

        ###calculate the actual width and height of the canvas
        self.actual_width = self._canvas.winfo_width()
        self.actual_height = self._canvas.winfo_height()

        ###draw the board by vertical and parallel line
        for rows in range(1, self.total_row_number):
            from_point1 = Point(0, rows / self.total_row_number).in_pixel(self.actual_width, self.actual_height)
            to_point2 = Point(1, rows / self.total_row_number).in_pixel(self.actual_width, self.actual_height)
            parallel_line = self._canvas.create_line(from_point1, to_point2)
            
        for cols in range(1, self.total_col_number):
            from_point2 = Point(cols / self.total_col_number, 0).in_pixel(self.actual_width, self.actual_height)
            to_point3 = Point(cols / self.total_col_number, 1).in_pixel(self.actual_width, self.actual_height)
            vertical_line = self._canvas.create_line(from_point2, to_point3)

    def draw_discs(self):

        ###draw the discs
        self.actual_width = self._canvas.winfo_width()
        self.actual_height = self._canvas.winfo_height()
        for rows in range(self.total_row_number):
            for cols in range(self.total_col_number):
                from_point3 = Point((cols / self.total_col_number),
                                    (rows / self.total_row_number)).in_pixel(self.actual_width,
                                                                             self.actual_height)
                
                to_point4 = Point((cols + 1) / self.total_col_number,
                                  (rows + 1) / self.total_row_number).in_pixel(self.actual_width,
                                                                               self.actual_height)
                if self.board_list[rows][cols] == 'B':
                    self._canvas.create_oval(from_point3, to_point4,
                                             fill = 'black',
                                                 outline = 'black')
                elif self.board_list[rows][cols] == 'W':
                    self._canvas.create_oval(from_point3, to_point4,
                                             fill = 'white',
                                             outline = 'black')


class Input_window:
    def __init__(self):

        ###this window pop when user click enter
        self.start_game = False
        self._input_window = tkinter.Toplevel()
        self._input_window.title('Option Window')
        
        row_number = tkinter.Label(master = self._input_window,
                                   text = 'How many row in the board (even number from 4 - 16): ')
        col_number = tkinter.Label(master = self._input_window,
                                   text = 'How many column in the board (even number from 4 - 16): ')
        first_move = tkinter.Label(master = self._input_window,
                                   text = 'Which color move first (B for Black, W for White): ')
        top_left = tkinter.Label(master = self._input_window,
                                 text = 'Which color is in top left (B for Black, W for White): ')
        win_option = tkinter.Label(master = self._input_window,
                                   text = "How to determine winner ('>' or '<'): ")

        self._row_number = tkinter.Entry(master = self._input_window,
                                         bg = 'gray',
                                         font = FONT1,
                                         width = 10)
        self._col_number = tkinter.Entry(master = self._input_window,
                                         bg = 'gray',
                                         font = FONT1,
                                         width = 10)
        self._first_move = tkinter.Entry(master = self._input_window,
                                         bg = 'gray',
                                         font = FONT1,
                                         width = 10)
        self._top_left = tkinter.Entry(master = self._input_window,
                                         bg = 'gray',
                                         font = FONT1,
                                         width = 10)
        self._win_option = tkinter.Entry(master = self._input_window,
                                         bg = 'gray',
                                         font = FONT1,
                                         width = 10)
        
        start_button = tkinter.Button(master = self._input_window,
                                      text = 'Click to start Othello Game',
                                      font = FONT1,
                                      command = self._click_start)
                                                     
        row_number.grid(row = 0, column = 1,
                        padx = 5, pady = 5,
                        sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        col_number.grid(row = 1, column = 1,
                        padx = 5, pady = 5,
                        sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        first_move.grid(row = 2, column = 1,
                        padx = 5, pady = 5,
                        sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        top_left.grid(row = 3, column = 1,
                        padx = 5, pady = 5,
                        sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        win_option.grid(row = 4, column = 1,
                        padx = 5, pady = 5,
                        sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._row_number.grid(row = 0, column = 2,
                              padx = 5, pady = 5,
                              sticky = tkinter.E + tkinter.W)
        self._col_number.grid(row = 1, column = 2,
                              padx = 5, pady = 5,
                              sticky = tkinter.E + tkinter.W)
        self._first_move.grid(row = 2, column = 2,
                              padx = 5, pady = 5,
                              sticky = tkinter.E + tkinter.W)
        self._top_left.grid(row = 3, column = 2,
                              padx = 5, pady = 5,
                              sticky = tkinter.E + tkinter.W)
        self._win_option.grid(row = 4, column = 2,
                              padx = 5, pady = 5,
                              sticky = tkinter.E + tkinter.W)

        start_button.grid(row = 6, column = 2,
                          padx = 5, pady = 5,
                          sticky = tkinter.S + tkinter.E)
        button_frame = tkinter.Frame(master = self._input_window)
        button_frame.grid(row = 6, column = 2,
                          padx = 5, pady = 5,
                          sticky = tkinter.S + tkinter.E)
        
        self._input_window.rowconfigure(0, weight = 1)
        self._input_window.rowconfigure(1, weight = 1)
        self._input_window.rowconfigure(2, weight = 1)
        self._input_window.rowconfigure(3, weight = 1)
        self._input_window.rowconfigure(4, weight = 1)
        self._input_window.rowconfigure(6, weight = 1)
        self._input_window.columnconfigure(1, weight = 1)
        self._input_window.columnconfigure(2, weight = 1)
        
    def _click_start(self):

        ###after user click start, close the window
        self.start_game = True
        self.total_row = int(self._row_number.get())
        self.total_col = int(self._col_number.get())
        self.first_turn = self._first_move.get()
        self.top_left_color = self._top_left.get()
        self.how_to_win = self._win_option.get()
        self._input_window.destroy()

        
    ###return everything from the input class so I can use in Ogame class
    def start_game(self):
        return self.start_game

    def total_row(self):
        return self.total_row
    
    def total_col(self):
        return self.total_col

    def first_turn(self):
        return self.first_turn

    def top_left_color(self):
        return self.first_turn

    def how_to_win(self):
        return self.how_to_win

    def not_yet(self):
        self._input_window.grab_set()
        self._input_window.wait_window()

        
class invalid_window:

    ###this window pop when there is a invalid move
    def __init__(self):
        self._invalid_window = tkinter.Toplevel()
        self._invalid_window.title('Invalid window')
        text_button = tkinter.Button(master = self._invalid_window,
                              text = 'INVALID move, click me to continue.',
                              font = FONT2,
                              command = self._close_window)
        text_button.grid(row = 0, column = 0,
                         padx = 5, pady = 5,
                         sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

    def _close_window(self):
        self._invalid_window.destroy()

class winner_window:

    ###this window pop when there is a winner
    def __init__(self, SMART):
        self._winner_window = tkinter.Toplevel()
        self._winner_window.title('Congratulation!')
        text = tkinter.Label(master = self._winner_window,
                             text = 'GAME OVER!' + '  ' + SMART + '  ' + '  ' + 'WIN!!!',
                             font = FONT2)
        text.grid(row = 5, column = 5,
                  padx = 20, pady = 20,
                  sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        close_button = tkinter.Button(master = self._winner_window,
                                      text = 'Click me to exit',
                                      font = FONT1,
                                      command = self._close_game)
        close_button.grid(row = 10, column = 5,
                          padx = 20, pady = 20,
                          sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

    def _close_game(self):
        self._winner_window.destroy()
                             
        
class Point:

    ###change the point from fraction to pixel
    def __init__(self, frac_x, frac_y):
        self._frac_x = frac_x
        self._frac_y = frac_y

    def remember_value(self):
        return self._frac_x, self._frac_y

    def in_pixel(self, width, height):
        self.P_pixel = (int(self._frac_x * width), int(self._frac_y * height))
        return self.P_pixel

       
if __name__ == '__main__':
    OGame().start()
            
