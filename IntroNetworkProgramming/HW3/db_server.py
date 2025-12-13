import socket, threading
from protocal import send_msg, recv_msg
from database import init_db, handle_request

HOST, PORT = "0.0.0.0", 10080

def handle_client(conn, addr):
    print(f"[+] Connected from {addr}")
    try:
        while True:
            req = recv_msg(conn)
            if req is None:
                break
            res = handle_request(req)
            send_msg(conn, res)
    except Exception as e:
        print(f"[Error] {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Disconnected {addr}")

def main():
    init_db()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[DB] Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start() # 使用 daemon thread(避免主程式結束後還有 thread 卡住)

if __name__ == "__main__":
    main()
