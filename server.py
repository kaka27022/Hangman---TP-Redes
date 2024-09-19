import socket
import random
import threading
import json

import hangman_words
from game_info import game_state

game_state_lock = threading.Lock()

def handle_client(client_socket, client_address, player_num, game_state):
    print(f"Player {player_num} connected from {client_address}")
    client_socket.send(f"Welcome Player {player_num}!\n".encode('utf-8'))

    if player_num == 1:
        # Player 1 sets up the game
        client_socket.send("Choose difficulty".encode('utf-8'))
        difficulty = client_socket.recv(16).decode('utf-8').strip().lower()
        
        # Initialize the game state based on chosen difficulty
        with game_state_lock:
            game_state['difficulty'] = difficulty
            game_state['chosen_word'] = random.choice(hangman_words.word_list[difficulty])
            game_state['display'] = ['-' for _ in range(len(game_state['chosen_word']))]
            game_state['ready'] = True  # Set the game state to ready after initialization

        print(game_state['difficulty'])
        print(game_state['chosen_word'])

    else:
        # Wait until Player 1 initializes the game state
        while not game_state['ready']:
            continue

    while game_state['lives'] > 0 and '-' in game_state['display']:
        with game_state_lock:
            if game_state['turn'] != player_num:
                continue

            # Send current game state and prompt for a guess
            client_socket.send("Your turn".encode('utf-8'))
            guess = client_socket.recv(16).decode('utf-8').strip().lower()

            if guess in game_state['used_letters']:
                client_socket.send(f"Your turn".encode('utf-8'))
                guess = client_socket.recv(16).decode('utf-8').strip().lower()

            else:
                game_state['used_letters'].append(guess)
                if guess in game_state['chosen_word']:
                    game_state['aux'] = 1
                    for i, letter in enumerate(game_state['chosen_word']):
                        if letter == guess:
                            game_state['display'][i] = guess
                else:
                    game_state['lives'] -= 1
                    game_state['Mistakes'] += 1
                    game_state['aux'] = 0
                    game_state['wrong_letters'].append(guess)

                # Switch turn
                game_state['turn'] = 1 if game_state['turn'] == 2 else 2
                print(game_state)

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
    game_info_json = json.dumps({
        "display": ''.join(game_state['display']),
        "wrong_letters": game_state['wrong_letters'],
        "turn": game_state['turn'],
        "Mistakes": game_state['Mistakes'],
        "aux": game_state['aux'],  # Adiciona o novo campo auxiliar ao estado do jogo
    })

    for client in game_state['clients']:
        try:
            if message:
                client.send((message + "\n").encode('utf-8'))  # Certifique-se de enviar uma nova linha
            # Envia o estado do jogo atualizado em formato JSON
            client.send(f"Game State: {game_info_json}\n".encode('utf-8'))  # Adiciona a nova linha
        except Exception as e:
            print(f"Failed to send message to client: {e}")


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




    

