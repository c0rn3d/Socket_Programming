import socket
import threading
from colorama import Fore, Style, init
import random
import signal
import sys

init()  # Initialize Colorama

# Server setup
HOST = 'localhost'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []
aliases = {}

# Define a list of colors
COLORS = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN,
    Fore.WHITE, Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX
]

def get_random_color():
    return random.choice(COLORS)

def handle_client(client_socket):
    client_color = get_random_color()
    client_alias = 'Anonymous'
    client_address = client_socket.getpeername()
    broadcast(f"{client_alias} has joined the chat from {client_address[0]}:{client_address[1]}", None)
    
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith('/alias '):
                # Set alias
                client_alias = message.split(' ', 1)[1]
                aliases[client_socket] = client_alias
                client_socket.send(f"Alias set to {client_alias}\n".encode())
            elif not message:
                break
            else:
                # Broadcast with alias if available
                formatted_message = f"{client_color}{client_alias}: {message}{Style.RESET_ALL}"
                broadcast(formatted_message, client_socket)
        except:
            break
    
    client_socket.close()
    clients.remove(client_socket)
    del aliases[client_socket]
    broadcast(f"{client_alias} has left the chat", None)

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)

def shutdown(signum, frame):
    print("\nShutting down server...")
    broadcast("Server is shutting down. Please disconnect.\n", None)
    for client in clients:
        try:
            client.close()
        except:
            pass
    server_socket.close()
    sys.exit(0)

# Setup signal handler for graceful shutdown
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
except KeyboardInterrupt:
    shutdown(None, None)
