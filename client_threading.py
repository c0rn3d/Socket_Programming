import socket
import threading

HOST = 'localhost'
PORT = 5000

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Disconnected from server.")
                break
            print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def get_alias():
    return input("Enter your alias: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))

    # Set alias
    alias = get_alias()
    client_socket.send(f"/alias {alias}".encode())

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        message = input()
        if message.lower() == '/quit':
            client_socket.send(message.encode())
            break
        if message:
            client_socket.send(message.encode())

except ConnectionRefusedError:
    print("Could not connect to the server. Ensure the server is running and try again.")
except KeyboardInterrupt:
    print("\nDisconnected from server.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_socket.close()
