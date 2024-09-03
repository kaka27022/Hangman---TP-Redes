import socket
import threading
from tkinter import *

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
        show_guess_letter_screen()
    elif "You won" in message:
        show_player_won_screen()
    elif "Game over" in message:
        show_game_over_screen()
    # Adicione mais condições para diferentes tipos de mensagens

# As funções show_x_screen são chamadas para atualizar a interface gráfica
def show_choose_difficulty_screen():
    janela = Tk()
    janela.title("Escolha a Dificuldade")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    Label(janela, text="Escolha o nível de dificuldade:", font=("Georgia", 20), fg="#EBE8CD", bg="#486441", justify="center").pack(pady=30)
    
    for difficulty in ["Fácil", "Médio", "Difícil"]:
        Button(janela, text=difficulty, font=("Georgia", 20), fg="#EBE8CD", bg="#617C5A", command=lambda d=difficulty: send_difficulty(d, janela)).pack(pady=20)

    janela.mainloop()

def send_difficulty(difficulty, janela):
    client_socket.send(difficulty.encode('utf-8'))
    # Fecha a janela após enviar
    janela.destroy()

def show_guess_letter_screen():
    janela = Tk()
    janela.title("Adivinhe a Letra")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    # Aqui você pode adicionar a lógica para mostrar a palavra parcial, etc.
    Label(janela, text="Sua vez de adivinhar uma letra:", font=("Georgia", 20), fg="#EBE8CD", bg="#486441", justify="center").pack(pady=30)
    entrada = Entry(janela, font=("Georgia", 20), width=20)
    entrada.pack(pady=20)
    
    Button(janela, text="Enviar", font=("Georgia", 20), fg="#EBE8CD", bg="#617C5A", command=lambda: send_guess(entrada.get(), janela)).pack(pady=20)

    janela.mainloop()

def send_guess(guess, janela):
    client_socket.send(guess.encode('utf-8'))
    # Fecha a janela após enviar
    janela.destroy()

# Exemplo de função para mostrar a tela de vitória
def show_player_won_screen():
    janela = Tk()
    janela.title("Você Ganhou!")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    Label(janela, text="Parabéns, você venceu!", font=("Georgia", 35), fg="#EBE8CD", bg="#486441", justify="center").pack(pady=30)
    img = PhotoImage(file="./art/trophy.png")
    Label(janela, image=img, bg="#486441").pack(pady=30)

    janela.mainloop()

# Função para mostrar a tela de derrota
def show_game_over_screen():
    janela = Tk()
    janela.title("Fim de Jogo")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    Label(janela, text="Game Over", font=("Georgia", 35), fg="#EBE8CD", bg="#486441", justify="center").pack(pady=30)
    img = PhotoImage(file="./art/GAMEOVER!.png")
    Label(janela, image=img, bg="#486441").pack(pady=30)

    janela.mainloop()

# Inicializando o cliente
client_socket = client()