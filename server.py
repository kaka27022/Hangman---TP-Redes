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
        # Player 1 inicia o jogo
        client_socket.send("Choose difficulty".encode('utf-8'))
        difficulty = client_socket.recv(16).decode('utf-8').strip().lower()
        
        # Inicializa o jogo baseado na dificuldade
        with game_state_lock:
            game_state['difficulty'] = difficulty
            game_state['chosen_word'] = random.choice(hangman_words.word_list[difficulty])
            game_state['display'] = ['-' for _ in range(len(game_state['chosen_word']))]
            game_state['ready'] = True  # Set the game state to ready after initialization

        print(game_state['difficulty'])
        print(game_state['chosen_word'])

    else:
        # Espera player 1 inicializar o jogo
        while not game_state['ready']:
            continue

    while game_state['lives'] > 0 and '-' in game_state['display']:
        with game_state_lock:
            if game_state['turn'] != player_num:
                continue

            chatting = True

            while chatting:
            # Recebe a letra jogada
                client_socket.send("Your turn".encode('utf-8'))
                guess_or_chat = client_socket.recv(16).decode('utf-8').strip().lower()
                print("Teste 1")

                if len(guess_or_chat) == 1:
                    print("Teste 2")
                    guess = guess_or_chat
                    chatting = False
                else: 
                    print("Teste 3")
                    broadcast_chat(player_num, guess_or_chat, game_state)
            
            if guess in game_state['used_letters']:
                client_socket.send("Your turn".encode('utf-8'))
                guess_or_chat = client_socket.recv(16).decode('utf-8').strip().lower()
                print("Teste 4")

                if len(guess_or_chat) == 1:
                    print("Teste 5")
                    guess = guess_or_chat
                    chatting = False
                else: 
                    print("Teste 6")
                    broadcast_chat(player_num, guess_or_chat, game_state)

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

                # Troca a vez
                game_state['turn'] = 1 if game_state['turn'] == 2 else 2
                notify_all_clients(None, game_state)  # Atualiza as informacoes
                #print(game_state)

    # Verifica se o jogo terminou
    if '-' not in game_state['display']:
        # Jogador atual venceu
        winner = player_num
        loser = 1 if player_num == 2 else 2
        
        # Notificar o vencedor e o perdedor
        notify_client(game_state['clients'][winner - 1], "you won", game_state)
        notify_client(game_state['clients'][loser - 1], "You lost", game_state)

    elif game_state['lives'] == 0:
        # Se o número de vidas acabar, ambos perdem
        notify_all_clients("Game over!", game_state)

    client_socket.close()

# Funcao para notificar apenas um cliente
def notify_client(client, message, game_state):
    game_info_json = json.dumps({
        "display": ''.join(game_state['display']),
        "wrong_letters": game_state['wrong_letters'],
        "turn": game_state['turn'],
        "Mistakes": game_state['Mistakes'],
        "aux": game_state['aux'],
        "chosen_word": game_state['chosen_word'],
    })

    try:
        if message:
            client.send((message + "\n").encode('utf-8'))  # Envia a mensagem personalizada
        client.send(f"Game State: {game_info_json}\n".encode('utf-8'))  # Envia o estado do jogo
    except Exception as e:
        print(f"Failed to send message to client: {e}")

# Funcao para notificar todos os clientes
def notify_all_clients(message, game_state):
    game_info_json = json.dumps({
        "display": ''.join(game_state['display']),
        "wrong_letters": game_state['wrong_letters'],
        "turn": game_state['turn'],
        "Mistakes": game_state['Mistakes'],
        "aux": game_state['aux'],  # Adiciona o novo campo auxiliar ao estado do jogo
        "chosen_word": game_state['chosen_word'],
    })

    for client in game_state['clients']:
        try:
            if message:
                client.send((message + "\n").encode('utf-8'))  # Certifique-se de enviar uma nova linha
            # Envia o estado do jogo atualizado em formato JSON
            client.send(f"Game State: {game_info_json}\n".encode('utf-8'))  # Adiciona a nova linha
        except Exception as e:
            print(f"Failed to send message to client: {e}")

# Funcao para transmitir mensagens de chat entre os jogadores
def broadcast_chat(player_num, message, game_state):
    for client in game_state['clients']:
        try:
            client.send(f"Player {player_num} says: {message}\n".encode('utf-8'))
        except Exception as e:
            print(f"Failed to send chat message to client: {e}")

# Inicializa o jogo/servidor
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




    

