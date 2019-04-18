import I32CFSP
import offline_library
import connectfour


###ask user to input user name, and send username to server,
###then print the message return by serve.
def _username_(connection):
    print('Welcome to connectfour network-version!\n')
    print('Please enter username to start the game.\n')
    username = input("Name:")
    I32CFSP.send(connection, "I32CFSP_HELLO "+username)
    response = I32CFSP.receive(connection)
    print('Response: ' + str(response))


###ask user to input AI_GAME to start the game,
###if user input AI_GAME,
###send what user input to serve and if it is AI_GAME,
###if user did not input AI_GAME, ask him to input again.
###print the message get from serve,
def _gamestart_(connection):
    while True:
        A = input("Please enter 'AI_GAME' to ready the server: ")
        if A == "AI_GAME":
            I32CFSP.send(connection, A)
            print(str(I32CFSP.receive(connection)))
            break
        else:
            continue


###receive the message from another module
def _reveice_(connection, messages):    
    for i in range(3):
        response = I32CFSP.receive(connection)
        messages.append(response)
    return messages


###ask user to input host,
###if it is invalid, tell user to input again,
###if it is valid return it.
def read_host():
    while True:
        I32CFSP_HOST = input('Please input host: ').strip()
        if I32CFSP_HOST == '':
            print('Please enter a valid host.')
            continue
        else:
            return I32CFSP_HOST



###ask user to input port,
###if it is invalid, tell user to input again,
###if it is valid return it
def read_port():
    while True:
        try:
            I32CFSP_PORT = int(input('Please input port: ').strip())
            if I32CFSP_PORT == '':
                print('Please enter a valid port.')
                continue
            else:
                return I32CFSP_PORT
        except:
            print('Please enter an integer')

        
        
                    
def main():
    while True:
        try:
            I32CFSP_HOST = read_host()
            I32CFSP_PORT = read_port()
            connection = I32CFSP.connect(I32CFSP_HOST, I32CFSP_PORT)
            break
        except:
            continue
    ###call host(), and port() function, check computer can make a connection
    ###ask user to input valid host and port until it connected

    loaded = connectfour.new_game_state()
    _username_(connection)
    _gamestart_(connection)

    
    while True:
        messages = []
        message = input("message(enter 'DROP number(1-7)'or 'POP number(1-7)':")
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

                elif connectfour.winning_player(loaded) == True:
                    winner = connectfour.winning_player(loaded)
                    if winner == 1:
                        print('Game over, Red wins!')
                        break
                    elif winner == 2:
                        print('Game over, Yellow wins!')
                        break                   
        ###call win function to check if there is a winner after user move

               
                I32CFSP.send(connection, message)
                messages = _reveice_(connection, messages)
                return_meaasges2 = messages[1]
                print(return_meaasges2)
                loaded = offline_library.DROP1(messages[1], loaded)
        ###send message to sever and print the message which action serve make

                if messages[2] == "WINNER_YELLOW" or messages[2] == "WINNER_RED":
                    print('Response: ' + messages[2])
                    print("Response: GAME OVER!")
                    break
        
        elif len(message) == 5 and message[0:4] == "POP ":
            if message[4] == "1" or message[4] == "2" or message[4] == "3" or message[4] == "4" or message[4] == "5" or message[4] == "6" or message[4] == "7":
                loaded = offline_library.DROP1(message, loaded)
                if loaded == None:
                    loaded = test
                    continue

                elif connectfour.winning_player(loaded) == True:
                    winner = connectfour.winning_player(loaded)
                    if winner == 1:
                        print('Game over, Red wins!')
                        break
                    elif winner == 2:
                        print('Game over, Yellow wins!')
                        break
                
                I32CFSP.send(connection, message)
                messages = _reveice_(connection, messages)
                loaded = offline_library.DROP1(messages[1], loaded)

                if messages[2] == "WINNER_YELLOW" or messages[2] == "WINNER_RED":
                    print('Response: ' + messages[2])
                    print("Response: GAME OVER!")
                    break
        else:
            print("Please enter correctly to continue the game.")

if __name__ == '__main__':
    main()
