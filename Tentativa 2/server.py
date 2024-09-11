import socket
import random
import threading

#import hangman_art
import hangman_words
from game_info import game_state

def handle_client(client_socket, client_address, player_num, game_state):
    print(f"Player {player_num} connected from {client_address}")
    client_socket.send(f"Welcome Player {player_num}!\n".encode('utf-8'))

    if player_num == 1:
        # Player 1 sets up the game
        client_socket.send("Choose difficulty".encode('utf-8'))
        difficulty = client_socket.recv(16).decode('utf-8').strip().lower()
        
        # Initialize the game state based on chosen difficulty
        game_state['difficulty'] = difficulty
        game_state['chosen_word'] = random.choice(hangman_words.word_list[difficulty])
        game_state['display'] = ['-' for _ in range(len(game_state['chosen_word']))]
        game_state['ready'] = True  # Set the game state to ready after initialization

        #notify_all_clients(f"Player 1 has chosen difficulty: {difficulty}.\n", game_state)

    else:
        # Wait until Player 1 initializes the game state
        while not game_state['ready']:
            continue
        #client_socket.send(f"Player 1 has set the difficulty to {game_state['difficulty']}.\n".encode('utf-8'))

    while game_state['lives'] > 0 and '-' in game_state['display']:
        if game_state['turn'] != player_num:
            continue

        # Send current game state and prompt for a guess
        #client_socket.send(f"Word: {' '.join(game_state['display'])}\n".encode('utf-8'))
        #client_socket.send(f"Lives left: {game_state['lives']}\n".encode('utf-8'))
        client_socket.send(f"Your turn".encode('utf-8'))
        guess = client_socket.recv(16).decode('utf-8').lower().strip()

        if guess in game_state['used_letters']:
            client_socket.send(f"Your turn".encode('utf-8'))
            guess = client_socket.recv(16).decode('utf-8').lower().strip()
        else:
            game_state['used_letters'].append(guess)
            if guess in game_state['chosen_word']:
                game_state['aux'] = 1
                #client_socket.send(f"Correct! Letter {guess} is in the word!\n".encode('utf-8'))
                for i, letter in enumerate(game_state['chosen_word']):
                    if letter == guess:
                        game_state['display'][i] = guess
            else:
                game_state['lives'] -= 1
                game_state['aux'] = 0
                #client_socket.send(f"Wrong! Letter {guess} is not in the word.\n".encode('utf-8'))
                game_state['wrong_letters'].append(guess)

            # Switch turn
            game_state['turn'] = 1 if game_state['turn'] == 2 else 2

        notify_all_clients(None, game_state)  # Notify all clients of updated state

    # Check for end of game and notify clients
    if '-' not in game_state['display']:
        notify_all_clients("you won", game_state)
    elif game_state['lives'] == 0:
        notify_all_clients("Game over", game_state)
    else: 
        notify_all_clients("You lost", game_state)  # Notify all clients of updated state

    client_socket.close()

def notify_all_clients(message, game_state):
    for client in game_state['clients']:
        try:
            if message:
                client.send(message.encode('utf-8'))
            #client.send(f"Word: {' '.join(game_state['display'])}\n".encode('utf-8'))
            #client.send(f"Wrong letters: {', '.join(game_state['wrong_letters'])}\n".encode('utf-8'))
            client.send(f"Lives: {game_state['lives']}\n".encode('utf-8'))
        except:
            continue

def server(host='localhost', port=8082):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print(f"Server started on {host}:{port}")

    while len(game_state['clients']) < 2:
        client_socket, client_address = server_socket.accept()
        game_state['clients'].append(client_socket)
        player_num = len(game_state['clients'])
        threading.Thread(target=handle_client, args=(client_socket, client_address, player_num, game_state)).start()

server()




    

