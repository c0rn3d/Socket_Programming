import socket
import threading
import re

HOST = 'localhost'
PORT = 5000

# Regex pattern for valid alias: only lowercase letters and numbers
VALID_ALIAS_PATTERN = re.compile(r'^[a-z0-9]+$')

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            break

def get_valid_alias():
    while True:
        alias = input("Enter your alias (lowercase letters and numbers only): ")
        if VALID_ALIAS_PATTERN.match(alias):
            return alias
        else:
            print("Invalid alias. Please use only lowercase letters and numbers.")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Set alias
alias = get_valid_alias()
client_socket.send(f"/alias {alias}".encode())

# Start a thread to receive messages
threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

while True:
    message = input()
    if message.lower() == '/quit':
        break
    client_socket.send(message.encode())

client_socket.close()
