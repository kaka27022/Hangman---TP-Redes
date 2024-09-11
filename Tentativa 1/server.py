import socket
import threading
import random
import hangman_words

def handle_client(client_socket, client_address, player_num, game_state):
    print(f"Player {player_num} connected from {client_address}")

    if player_num == 1:
        client_socket.send("Choose difficulty: Fácil, Médio, Difícil".encode('utf-8'))

        # Espera o jogador 1 escolher a dificuldade
        difficulty = client_socket.recv(1024).decode('utf-8')
        game_state['difficulty'] = difficulty.lower()
        print(f"Player {player_num} chose difficulty: {difficulty.lower()}")

        # Escolha a palavra e prepare o estado do jogo
        game_state['chosen_word'] = random.choice(hangman_words.word_list[difficulty.lower()])
        game_state['display'] = ['-' for _ in range(len(game_state['chosen_word']))]
        game_state['ready'] = True

    else:
        while not game_state['ready']:
            client_socket.send("Aguarde jogador 1 escolher a dificuldade!!!".encode('utf-8'))
            continue

    while game_state['lives'] > 0 and '-' in game_state['display']:
        if game_state['turn'] != player_num:
            continue

        client_socket.send(f"Your turn, Player {player_num}. Guess a letter: {''.join(game_state['display'])}".encode('utf-8'))
        guess = client_socket.recv(1024).decode('utf-8')

        if guess in game_state['used_letters']:
            client_socket.send(f"Letter {guess} has already been guessed. Try again.".encode('utf-8'))
        else:
            game_state['used_letters'].append(guess)
            if guess in game_state['chosen_word']:
                game_state['aux'] = 1
                for i, letter in enumerate(game_state['chosen_word']):
                    if letter == guess:
                        game_state['display'][i] = guess
            else:
                game_state['aux'] = 0
                game_state['lives'] -= 1
                game_state['Mistakes'] += 1
                game_state['wrong_letters'].append(guess)

            game_state['turn'] = 1 if game_state['turn'] == 2 else 2

            notify_all_clients(game_state)

    if '-' not in game_state['display'] and player_num != game_state['turn']:
        client_socket.send("You won!".encode('utf-8'))
    elif game_state['lives'] == 0:
        client_socket.send("Game over!".encode('utf-8'))
    else:
        client_socket.send("You lost!".encode('utf-8'))

    client_socket.close()

def notify_all_clients(game_state):
    for client in game_state['clients']:
        try:
            client.send(f"Word: {''.join(game_state['display'])} | Wrong letters: {', '.join(game_state['wrong_letters'])} | Lives left: {game_state['lives']}".encode('utf-8'))
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
        'wrong_letters': [],
        'lives': 6,
        'Mistakes': 0,
        'turn': 1,
        'aux': 0,
        'clients': [],
        'ready': False,
    }

    while len(game_state['clients']) < 2:
        client_socket, client_address = server_socket.accept()
        game_state['clients'].append(client_socket)
        player_num = len(game_state['clients'])
        threading.Thread(target=handle_client, args=(client_socket, client_address, player_num, game_state)).start()

server()