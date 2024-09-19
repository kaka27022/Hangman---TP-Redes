import socket
import threading
import json

from tkinter import *
from styles import *
from game_info import game_state

# Função para inicializar o cliente
def client(host='localhost', port=8082):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    handle_server_message(message)
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    # Thread para receber mensagens do servidor
    threading.Thread(target=receive_messages).start()

    return client_socket

# Função para lidar com mensagens do servidor
def handle_server_message(message):
    if "Choose difficulty" in message:
        show_choose_difficulty_screen()
    elif "Your turn" in message:
        show_guess_letter_screen()  # Atualiza a interface com base na vez do jogador
    elif "Game State" in message:
        update_game_info(message)
    elif "you won" in message:
        show_player_won_screen()
    elif "You lost" in message:
        show_player_lost_screen()
    elif "Game over" in message:
        show_game_over_screen()


def update_game_info(message):
    if "Game State" in message:
        try:
            game_state_str = message.split("Game State: ")[1].strip()
            game_info = json.loads(game_state_str)  # Deserializar JSON
            # Atualizar estado local
            game_state['display'] = list(game_info['display'])
            game_state['wrong_letters'] = game_info['wrong_letters']
            game_state['turn'] = game_info['turn']
            game_state['Mistakes'] = game_info['Mistakes']
            game_state['aux'] = game_info['aux']

            # Atualize a interface ou imprima o estado atualizado
            print("Atualizando estado do jogo:", game_state)
            show_informations()  # Atualiza a interface do jogo
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Erro ao atualizar game state: {e}")


# As funções show_x_screen são chamadas para atualizar a interface gráfica
def show_choose_difficulty_screen():
    janela = Tk()
    janela.title("Jogo da Forca")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    logo(janela)

    welcome_player(janela)

    Label(janela, 
          text="Escolha o nível de dificuldade:", 
          font=("Georgia", 20), 
          fg="#EBE8CD", 
          bg="#486441", 
          justify="center").pack(pady=30)
    
    for difficulty in ["Fácil", "Médio", "Difícil"]:
        Button(janela, 
               text=difficulty, 
               font=("Georgia", 20), 
               fg="#EBE8CD", 
               bg="#617C5A", 
               command=lambda d=difficulty: send_difficulty(d, janela, client_socket)).pack(pady=20)

    janela.mainloop()

def send_difficulty(difficulty, janela, client_socket):
    client_socket.send(difficulty.encode('utf-8'))
    # Fecha a janela após enviar
    janela.destroy()

def show_guess_letter_screen():
    janela = Tk()
    janela.title("Jogo da Forca")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    # Exibir a palavra atual e o jogador da vez
    show_word(janela, game_state)
    time_player(janela, game_state)

    if game_state['turn'] == 1 or game_state['turn'] == 2:
        Label(janela, text="Sua vez de adivinhar uma letra:", font=("Georgia", 20), fg="#EBE8CD", bg="#486441", justify="center").pack(pady=30)
        entrada = Entry(janela, font=("Georgia", 20), width=20)
        entrada.pack(pady=20)

        Button(janela, text="Enviar", font=("Georgia", 20), fg="#EBE8CD", bg="#617C5A", command=lambda: send_guess(entrada.get(), janela, client_socket)).pack(pady=20)
    else:
        # Se não for a vez do jogador, exibir uma mensagem informativa
        Label(janela, text="Aguarde sua vez...", font=("Georgia", 20), fg="#EBE8CD", bg="#486441", justify="center").pack(pady=30)

    show_hang(janela, game_state)
    show_wrong_letters(janela, game_state)

    janela.mainloop()


def send_guess(guess, janela, client_socket):
    client_socket.send(guess.encode('utf-8'))
    # Fecha a janela após enviar a jogada
    janela.destroy()


# Exemplo de função para mostrar a tela de vitória
def show_player_won_screen():
    janela = Tk()
    janela.title("Jogo da Forca")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    you_won(janela)
    show_word(janela, game_state)

    img = PhotoImage(file="./art/trophy.png")
    label_imagem = Label(janela, 
                         image=img,
                         bg="#486441")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)

    janela.mainloop()

def show_player_lost_screen():
    janela = Tk()
    janela.title("Jogo da Forca")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    you_lost(janela)
    show_word(janela, game_state)

    img = PhotoImage(file="./art/emoji.png")
    label_imagem = Label(janela, 
                         image=img,
                         bg="#486441")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)

    janela.mainloop()

def show_informations():
    janela = Tk()
    janela.title("Jogo da Forca")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    # Se ultima letra jogada existir na palavra
    if game_state['aux'] == 1: 
        letter_in_word(janela)
    else:
    # Se ultima letra jogada não existir na palavra
        letter_not_in_word(janela)

    show_hang(janela, game_state)
    show_word(janela, game_state)
    show_wrong_letters(janela, game_state)

    janela.mainloop()

# Função para mostrar a tela de derrota
def show_game_over_screen():
    janela = Tk()
    janela.title("Jogo da Forca")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    loser(janela)
    
    show_word(janela, game_state)
    show_hang(janela, game_state)

    janela.mainloop()

# Inicializando o cliente
client_socket = client()