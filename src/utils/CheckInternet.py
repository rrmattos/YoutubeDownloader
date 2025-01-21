import socket

def check_internet_connection():
    try:
        # --- Tenta se conectar ao Google DNS (8.8.8.8) na porta 53 ---
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except (socket.timeout, socket.gaierror):
        return False
