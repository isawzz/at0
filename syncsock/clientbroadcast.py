import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

def listen_for_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print("\n[Broadcast] " + data.decode(), end="\n> ")
        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    threading.Thread(target=listen_for_messages, args=(s,), daemon=True).start()

    print("Connected to the broadcast server. Type messages:")
    while True:
        msg = input("> ")
        if msg.lower() in ("quit", "exit"):
            break
        s.sendall(msg.encode())
