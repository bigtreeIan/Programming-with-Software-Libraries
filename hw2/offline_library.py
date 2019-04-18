import connectfour

def print_board(gamestate):
    print("1  2  3  4  5  6  7")
    for i in range(6):
        for j in range(7):
            if gamestate[0][j][i] == 0:
                print(".", " ", end="")
            elif gamestate[0][j][i] == 1:
                print("R", " ", end="")
            elif gamestate[0][j][i] == 2:
                print("Y", " ", end="")
        print("\n")

def DROP1(pop_or_drop, new):
    #new = connectfour.new_game_state()
    while True:
        if pop_or_drop[0:5] == "DROP ":
            try:
                n = int(pop_or_drop[5])
                column_number = n - 1
                drop = connectfour.drop_piece(new, column_number)
            except connectfour.InvalidMoveError:
                print("a move cannot be made in the given column because the column is filled already")
                break
            except connectfour.GameOverError:
                print("Game is over! Please enter E to exit the game or enter N to start a new game")
                continue
            except ValueError:
                print("Invalid input, try again")
                continue
            new = drop
            print_board(drop)
            return new

        elif pop_or_drop[0:4] == "POP ":
            try:
                p = int(pop_or_drop[4])
                pop_number = p - 1
                drop = connectfour.pop_piece(new, pop_number)
            except connectfour.InvalidMoveError:
                print("a piece cannot be popped from the bottom of the given column because the column is empty or because the piece at the bottom of the column belongs to the other player")
                break
            except connectfour.GameOverError:
                print("Game is over! Please enter E to exit the game or enter N to start a new game")
                continue
            except ValueError:
                print("Invalid input, try again")
                continue
            new = drop
            print_board(drop)
            return new
        break
