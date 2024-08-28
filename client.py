import socket

def client(host='localhost', port=8082):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)

            if "Choose difficulty" in message:
                difficulty = input("Type difficulty: ")
                client_socket.send(difficulty.encode('utf-8'))
            
            if "Your turn" in message:
                guess = input("Enter a letter: ")
                client_socket.send(guess.encode('utf-8'))

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

client()

