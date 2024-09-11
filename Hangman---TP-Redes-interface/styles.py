from tkinter import *
import random
import hangman_words
import socket

def inicializa_janela():
    janela = Tk()
    janela.title("Hangman")
    janela.configure(background="#486441")
    janela.geometry("802x708")

    return janela

def logo(janela):
    img = PhotoImage(file=f"./art/JOGODAFORCA.png")
    label_imagem = Label(janela, image=img, bg="#486441", fg="#EBE8CD")
    label_imagem.image = img  # Mantenha uma referência à imagem
    label_imagem.pack(pady=30)

def click(difficulty, game_state):
    game_state['difficulty'] = difficulty.lower()
    game_state['chosen_word'] = random.choice(hangman_words.word_list[difficulty])
    game_state['display'] = ['-' for _ in range(len(game_state['chosen_word']))]
    game_state['ready'] = True  # Set the game state to ready after initialization

def already_choose_letter(game_state, guess):

    janela = inicializa_janela()

    label = Label(janela,
                text=f"Letra {guess} ja jogada, tente novamente:",
                font= ("Georgia", 35),
                fg="#EBE8CD",
                bg="#486441",
                justify="center")
    label.pack(pady=30)


    show_word(janela, game_state)
    time_player(janela)
    write_letter(janela)
    #guess_button(janela)
    show_hang(janela, game_state)
    show_wrong_letters(janela)

    janela.mainloop()

def click_guess(game_state, entrada, client_socket):
    guess = entrada.get()
    if guess in game_state['used_letters']:
        client_socket.send(already_choose_letter(game_state, guess).encode('utf-8'))
    else:
        game_state['used_letters'].append(guess)
        if guess in game_state['chosen_word']:
            game_state['aux'] = 1
            #client_socket.send(f"\nLetter {guess} is in the word!\n".encode('utf-8'))
            for i, letter in enumerate(game_state['chosen_word']):
                if letter == guess:
                    game_state['display'][i] = guess

            #client_socket.send(show_informations(aux, game_state).encode('utf-8'))
            
        else:
            game_state['aux'] = 2
            game_state['lives'] -= 1
            game_state['Mistakes'] += 1
            #client_socket.send(f"\nLetter {guess} is not in the word.\n".encode('utf-8'))
            game_state['wrong_letters'].append(guess)
            #client_socket.send(show_informations(aux, game_state).encode('utf-8'))

        game_state['turn'] = 1 if game_state['turn'] == 2 else 2
    

def button(difficulty, janela, game_state):
    b = Button(janela,
               text=difficulty,
               command=click(difficulty, game_state),
               font= ("Georgia", 20),
               fg="#EBE8CD",
               bg="#617C5A",
               borderwidth=0,
               highlightthickness=0,
               width=20,
               height=2
               )

    b.pack(pady=20)

def write_letter(janela):
    entrada = Entry(janela,
                    font=("Georgia", 20),
                    width=20)
    entrada.pack(pady=20)

    guess_button(janela, entrada)

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

def show_word(janela, game_state):
    label_word = Label(janela, 
                       text=f"Palavra: {' '.join(game_state['display'])}",
                       font= ("Georgia", 35),
                       fg="#EBE8CD",
                       bg="#486441",
                       justify="center")
    label_word.pack(pady=20)

def welcome_player(janela):
    label_inicio = Label(janela, 
                text="Bem vindo, Jogador!", 
                font= ("Georgia", 20),
                fg="#EBE8CD",
                bg="#486441",
                justify="center")
    label_inicio.pack(pady=30)

def time_player(janela, game_state):
    label = Label(janela,
                          text=f"Sua vez, Jogador {game_state['turn']}:",
                          font= ("Georgia", 35),
                          fg="#EBE8CD",
                          bg="#486441",
                          justify="center")
    label.pack(pady=30)

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

def guess_button(janela, estado, game_state):
    b = Button(janela,
               text="Adivinhar",
               command=click_guess(estado, game_state),
               font= ("Georgia", 20),
               fg="#EBE8CD",
               bg="#617C5A",
               borderwidth=0,
               highlightthickness=0,
               width=10,
               )

    b.pack(pady=20)