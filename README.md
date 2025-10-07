# 🎮 Jogo da Forca em Rede

Este projeto foi desenvolvido como parte da disciplina **Redes de Computadores**, com o objetivo de aplicar conceitos de comunicação cliente-servidor, threads e sockets TCP em Python. O sistema implementa um jogo da forca multiplayer com interface gráfica e feedback sonoro.

## 🧩 Funcionalidades

- Comunicação entre servidor e múltiplos clientes usando TCP
- Gerenciamento de turnos entre dois jogadores
- Interface gráfica construída com Tkinter e Pygame
- Atualização em tempo real do estado do jogo (palavra, letras erradas, erros, vencedor etc.)
- Diferentes níveis de dificuldade
- Sons para eventos do jogo (vitória, erro, escolha etc.)

## ⚙️ Como Executar

### 1. Clonar o repositório
git clone https://github.com/kaka27022/Hangman---TP-Redes.git

### 2. Instalar as dependências
Certifique-se de ter o **Python 3** instalado.
Instale as bibliotecas necessárias:
pip install pygame

### 3. Iniciar o servidor
Em um terminal:
python server.py

### 4. Iniciar os clientes
Em dois terminais diferentes (ou máquinas diferentes):
python client.py

O **primeiro cliente conectado** escolherá o nível de dificuldade.
Depois, os jogadores se alternam tentando adivinhar as letras da palavra.

## 🧠 Conceitos de Redes Aplicados

- Socket TCP: estabelece a comunicação confiável entre clientes e servidor.
- Threads: permitem o atendimento simultâneo de múltiplos clientes.
- Protocolo de mensagens customizado: troca de dados em formato JSON para sincronização do estado do jogo.
- Controle de concorrência: uso de threading.Lock para evitar inconsistências no estado compartilhado.

## 👩‍💻 Autoria
Projeto desenvolvido por [Maria Clara Silva Perpetuo](https://github.com/kaka27022) e [Luiz Humberto Fonseca](https://github.com/LuizHumbertoF)
Disciplina: **Redes de Computadores**
Universidade Federal de Ouro Preto (UFOP)

## 📜 Licença
Este projeto é apenas para fins educacionais e acadêmicos.

