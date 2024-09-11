from tkinter import *

def logo(janela):
    img = PhotoImage(file=f"./art/JOGODAFORCA.png")
    label_imagem = Label(janela, image=img, bg="#486441", fg="#EBE8CD")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)

def welcome_player(janela):
    label_inicio = Label(janela, 
                text="Bem vindo, Jogador!", 
                font= ("Georgia", 20),
                fg="#EBE8CD",
                bg="#486441",
                justify="center")
    label_inicio.pack(pady=30)

def show_word(janela, game_state):
    label_word = Label(janela, 
                       text=f"Palavra: {' '.join(game_state['display'])}",
                       font= ("Georgia", 35),
                       fg="#EBE8CD",
                       bg="#486441",
                       justify="center")
    label_word.pack(pady=20)

def time_player(janela, game_state):
    label = Label(janela,
                          text=f"Sua vez, Jogador {game_state['turn']}:",
                          font= ("Georgia", 35),
                          fg="#EBE8CD",
                          bg="#486441",
                          justify="center")
    label.pack(pady=30)

def show_hang(janela,game_state):
    #inicio = 0
    img = PhotoImage(file=f"./art/Forca{game_state['Mistakes']}.png")
    label_imagem = Label(janela, image=img, bg="#486441", fg="#EBE8CD")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)

def show_wrong_letters(janela, game_state):
    label_wrong_letters = Label(janela, 
                               text=f"Letras erradas: {', '.join(game_state['wrong_letters'])}",
                               font= ("Georgia", 35),
                               fg="#EBE8CD",
                               bg="#486441",
                               justify="center")
    label_wrong_letters.pack(pady=20)

def you_won(janela):
    img = PhotoImage(file=f"./art/VOCEGANHOU!!.png")
    label_imagem = Label(janela, image=img, bg="#486441", fg="#EBE8CD")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)

def you_lost(janela):
    img = PhotoImage(file=f"./art/VOCEPERDEU!.png")
    label_imagem = Label(janela, image=img, bg="#486441", fg="#EBE8CD")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)

def loser(janela):
    img = PhotoImage(file=f"./art/GAMEOVER!.png")
    label_imagem = Label(janela, image=img, bg="#486441", fg="#EBE8CD")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)

def letter_in_word(janela):
    # Se ultima letra jogada existir na palavra 
    label = Label(janela,
                          text="Letra existe na palavra!",
                          font= ("Georgia", 35),
                          fg="#EBE8CD",
                          bg="#486441",
                          justify="center")
    label.pack(pady=30)

def letter_not_in_word(janela):
    label = Label(janela,
                          text="Letra nao existe na palavra!",
                          font= ("Georgia", 35),
                          fg="#EBE8CD",
                          bg="#486441",
                          justify="center")
    label.pack(pady=30)