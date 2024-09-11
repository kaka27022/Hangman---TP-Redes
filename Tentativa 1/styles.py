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