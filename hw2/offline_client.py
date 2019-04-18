import connectfour
import offline_library


###Draw the board
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


def main():
    loaded = connectfour.new_game_state()
    while True:
        message = input("message(enter 'DROP number(1-7)'or 'POP number(1-7)': ")
        test = loaded
        if len(message) == 6 and message[0:5] == "DROP ":
            if message[5] == "1" or message[5] == "2" or message[5] == "3" or message[5] == "4" or message[5] == "5" or message[5] == "6" or message[5] == "7":
                loaded = offline_library.DROP1(message, loaded)
                if loaded == None:
                    loaded = test
                    continue
        ###ask user to input POP or DROP,
        ###check if the operation is valid,
        ###if the action is invalid, ask user to input again

                
                if connectfour.winning_player(loaded) == True:
                    winner = connectfour.winning_player(loaded)
                    if winner == 1:
                        print("Game over, Red wins!")
                        break
                    elif winner == 2:
                        print("Game over, Yellow wins!")
                        break
        ###call win function to check if there is a winner after user move


        elif len(message) == 5 and message[0:4] == "POP ":
            if message[4] == "1" or message[4] == "2" or message[4] == "3" or message[4] == "4" or message[4] == "5" or message[4] == "6" or message[4] == "7":
                loaded = offline_library.DROP1(message, loaded)
                if loaded == None:
                    loaded = test
                    continue
                if connectfour.winning_player(loaded) == True:
                    winner = connectfour.winning_player(loaded)
                    if winner == 1:
                        print("Game over, Red wins!")
                        break
                    elif winner == 2:
                        print("Game over, Yellow wins!")
                        break

        else:
            print("Please enter valid operation.")
            continue


if __name__ == '__main__':
    main()
