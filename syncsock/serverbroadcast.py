import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

clients = []

def broadcast(message, sender_conn):
    for conn in clients:
        if conn != sender_conn:
            try:
                conn.sendall(message)
            except:
                pass  # Ignore broken pipes or closed connections

def handle_client(conn, addr):
    print(f"[NEW] {addr} connected.")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[{addr}] {data.decode()}")
            broadcast(data, conn)
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        print(f"[DISCONNECTED] {addr}")
        clients.remove(conn)
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER STARTED] on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    main()
