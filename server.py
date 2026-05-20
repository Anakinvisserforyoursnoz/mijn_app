#!/usr/bin/env python3
import socket
import threading
import json

HOST = '0.0.0.0'
PORT = 5555

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)

        clients.remove(client)

        username = usernames[index]
        usernames.remove(username)

        client.close()

        print(f"[-] {username} disconnected")

        message = json.dumps({
            "user": "System",
            "message": f"{username} left the chat"
        })

        broadcast(message.encode())

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            broadcast(message)

        except:
            break

    remove_client(client)

def receive_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen()

    print(f"[+] Server running on {HOST}:{PORT}")

    while True:
        client, address = server.accept()

        print(f"[+] Connected: {str(address)}")

        username = client.recv(1024).decode()

        clients.append(client)
        usernames.append(username)

        print(f"[+] Username: {username}")

        message = json.dumps({
            "user": "System",
            "message": f"{username} joined the chat"
        })

        broadcast(message.encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive_connections()
