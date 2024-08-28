import socket
import random
import threading

import hangman_art
import hangman_words

def handle_client(client_socket, client_address, player_num, game_state):
    print(f"Player {player_num} connected from {client_address}")
    client_socket.send(f"Welcome Player {player_num}!\n".encode('utf-8'))

    if player_num == 1:
        client_socket.send("Choose difficulty (easy, medium, hard) ".encode('utf-8'))
        difficulty = client_socket.recv(16).decode('utf-8').strip().lower()
        
        # Loop until a valid difficulty is chosen
        while difficulty not in hangman_words.word_list:
            client_socket.send("Invalid difficulty. Choose again (easy, medium, hard): ".encode('utf-8'))
            difficulty = client_socket.recv(16).decode('utf-8').strip().lower()
        
        # Initialize the game state based on chosen difficulty
        game_state['difficulty'] = difficulty
        game_state['chosen_word'] = random.choice(hangman_words.word_list[difficulty])
        game_state['display'] = ['-' for _ in range(len(game_state['chosen_word']))]
        game_state['ready'] = True  # Set the game state to ready after initialization

    else:
        # Wait until Player 1 initializes the game state
        while not game_state['ready']:
            continue

    while '-' in game_state['display']:
        if game_state['turn'] != player_num:
            continue

        client_socket.send(f"Word: {' '.join(game_state['display'])}\n".encode('utf-8'))
        client_socket.send(f"Your turn, Player {player_num}!\n".encode('utf-8'))
        client_socket.send(f"Used letters: {', '.join(game_state['used_letters'])}\n".encode('utf-8'))

        guess = client_socket.recv(16).decode('utf-8').lower().strip()
        if guess in game_state['used_letters']:
            client_socket.send(f"You've already guessed {guess}.\n".encode('utf-8'))
        else:
            game_state['used_letters'].append(guess)
            if guess in game_state['chosen_word']:
                for i, letter in enumerate(game_state['chosen_word']):
                    if letter == guess:
                        game_state['display'][i] = guess
            else:
                client_socket.send(f"Letter {guess} is not in the word.\n".encode('utf-8'))

            game_state['turn'] = 1 if game_state['turn'] == 2 else 2

        notify_all_clients(game_state)

    if '-' not in game_state['display'] and player_num != game_state['turn']:   # Tem que ser diferente por que a turn muda, descoberta por tentativa
        client_socket.send(f"Congratulations Player {player_num}, you won!\n".encode('utf-8'))
    else:
        client_socket.send(f"Game over! The word was {game_state['chosen_word']}!\n".encode('utf-8'))

    client_socket.close()

def notify_all_clients(game_state):
    for client in game_state['clients']:
        try:
            client.send(f"Word: {' '.join(game_state['display'])}\n".encode('utf-8'))
            client.send(f"Used letters: {', '.join(game_state['used_letters'])}\n".encode('utf-8'))
        except:
            continue

def server(host='localhost', port=8082):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print(f"Server started on {host}:{port}")

    game_state = {
        'difficulty': None,
        'chosen_word': None,
        'display': None,
        'used_letters': [],
        'turn': 1,
        'clients': [],
        'ready': False,  # Game state is not ready until Player 1 sets it up
    }

    while len(game_state['clients']) < 2:
        client_socket, client_address = server_socket.accept()
        game_state['clients'].append(client_socket)
        player_num = len(game_state['clients'])
        threading.Thread(target=handle_client, args=(client_socket, client_address, player_num, game_state)).start()

server()



    

