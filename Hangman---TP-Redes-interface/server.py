import socket
import threading
import interface

def handle_client(client_socket, client_address, player_num, game_state):
    print(f"Player {player_num} connected from {client_address}")

    if player_num == 1:
        client_socket.send(interface.game_init_player1(game_state).encode('utf-8'))

    else:
        while not game_state['ready']:
            client_socket.send(interface.game_init_player2().encode('utf-8'))
            continue

    while game_state['lives'] > 0 and '-' in game_state['display']:
        if game_state['turn'] != player_num:
            continue
        
        client_socket.send(interface.choose_letter(game_state).encode('utf-8'))

        notify_all_clients(game_state)

    if '-' not in game_state['display'] and player_num != game_state['turn']:   # Tem que ser diferente por que a turn muda, descoberta por tentativa
        client_socket.send(interface.player_won(game_state).encode('utf-8'))
    elif game_state['lives'] == 0:
        client_socket.send(interface.game_over(game_state).encode('utf-8'))
    else:
        client_socket.send(interface.player_lost(game_state).encode('utf-8'))

    client_socket.close()

def notify_all_clients(game_state):
    for client in game_state['clients']:
        try:
            client.send(interface.show_informations(game_state).encode('utf-8'))
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
        'wrong_letters':[],
        'lives': 6,
        'Mistakes': 0,
        'turn': 1,
        'aux': 0,
        'clients': [],
        'ready': False,  # Game state is not ready until Player 1 sets it up
    }

    while len(game_state['clients']) < 2:
        client_socket, client_address = server_socket.accept()
        game_state['clients'].append(client_socket)
        player_num = len(game_state['clients'])
        threading.Thread(target=handle_client, args=(client_socket, client_address, player_num, game_state)).start()

server()


    

