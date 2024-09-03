from tkinter import *
from styles import *

def game_init_player1(game_state):

    janela = inicializa_janela()

    logo(janela)

    welcome_player(janela)

    label_inicio = Label(janela, 
                text="Escolha o nível de dificuldade: ", 
                font= ("Georgia", 20),
                fg="#EBE8CD",
                bg="#486441",
                justify="center")
    label_inicio.pack(pady=30)

    
    button("Fácil", janela, game_state)
    button("Médio", janela, game_state)
    button("Difícil", janela, game_state)

    janela.mainloop()

def game_init_player2():

    janela = inicializa_janela()

    logo(janela)

    welcome_player(janela)

    label_inicio = Label(janela, 
                text="Aguarde jogador 1 escolher a dificuldade!!!", 
                font= ("Georgia", 20),
                fg="#EBE8CD",
                bg="#486441",
                justify="center")
    label_inicio.pack(pady=30)

    janela.mainloop()


def choose_letter(game_state):

    janela = inicializa_janela()

    show_word(janela, game_state)
    time_player(janela)
    write_letter(janela)
    #guess_button(janela)
    show_hang(janela, game_state)
    show_wrong_letters(janela)

    janela.mainloop()

def show_informations(game_state):

    janela = inicializa_janela()

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

def player_won(game_state):

    janela = inicializa_janela()

    you_won(janela)
    show_word(janela, game_state)

    img = PhotoImage(file="./art/trophy.png")
    label_imagem = Label(janela, 
                         image=img,
                         bg="#486441")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)

    janela.mainloop()

def player_lost(game_state):

    janela = inicializa_janela()

    you_lost(janela)
    show_word(janela, game_state)

    img = PhotoImage(file="./art/emoji.png")
    label_imagem = Label(janela, 
                         image=img,
                         bg="#486441")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)


    janela.mainloop()

def game_over(game_state):
    janela = inicializa_janela()

    loser(janela)
    show_word(janela, game_state)
    show_hang(janela, game_state)

    janela.mainloop()
