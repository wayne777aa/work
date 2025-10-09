import socket
import threading
import json
import os
import tempfile
import shutil

HOST = '0.0.0.0'   # 允許外部連入
PORT = 12000
DB_FILE = 'user_db.json'

# 全域 lock
db_lock = threading.Lock()

# 載入帳號資料庫
def load_db():
    with db_lock:
        if not os.path.exists(DB_FILE):
            return {}
        with open(DB_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("[ERROR] JSON decode error in DB file. Returning empty DB.")
                return {}

# 儲存帳號資料庫
def save_db(db):
    with db_lock:
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            json.dump(db, tmp, indent=4)
            tmp_path = tmp.name
        shutil.move(tmp_path, DB_FILE)

# 處理每個 client 的登入/註冊
def handle_client(conn, addr):
    print(f"[INFO] Connected by {addr}")
    db = load_db()

    try:
        data = conn.recv(1024).decode()
        req = json.loads(data)

        action = req.get("action")
        username = req.get("username")
        password = req.get("password")

        if action == "register":
            if username in db:
                conn.sendall(b'{"status": "REGISTER_FAIL", "reason": "User exists"}')
            else:
                db[username] = {
                    "password": password,
                    "win": 0,
                    "draw": 0,
                    "lose": 0,
                    "online": False
                }
                save_db(db)
                conn.sendall(b'{"status": "REGISTER_SUCCESS"}')

        elif action == "login":
            if username not in db or db[username]["password"] != password: # 找不到帳號或密碼對不上
                conn.sendall(b'{"status": "LOGIN_FAIL", "reason": "Wrong credentials"}')
            elif db[username]["online"]: # 已登入的情況
                conn.sendall(b'{"status": "LOGIN_FAIL", "reason": "User already logged in. Please logout first"}')
            else:
                db[username]["online"] = True
                save_db(db)
                stats = db[username]
                resp = {
                "status": "LOGIN_SUCCESS",
                "win": stats["win"],
                "draw": stats["draw"],
                "lose": stats["lose"]
                }
                conn.sendall(json.dumps(resp).encode())
        
        elif action == "update_stats":
            updates = req.get("updates", [])
            if not isinstance(updates, list):
                conn.sendall(b'{"status": "FAIL", "reason": "Invalid updates format"}')
            else:
                failed = []
                for update in updates:
                    username = update.get("username")
                    stats = update.get("stats", {})
                    if username in db:
                        db[username]["win"] += stats.get("win", 0)
                        db[username]["draw"] += stats.get("draw", 0)
                        db[username]["lose"] += stats.get("lose", 0)
                    else:
                        failed.append(username)
                save_db(db)
                if failed:
                    conn.sendall(json.dumps({
                        "status": "PARTIAL_SUCCESS",
                        "failed": failed
                    }).encode())
                else:
                    conn.sendall(b'{"status": "UPDATE_SUCCESS"}')
        
        elif action == "logout":
            if username not in db:
                conn.sendall(b'{"status": "FAIL", "reason": "User not found"}')
            else:
                db[username]["online"] = False
                save_db(db)
                conn.sendall(b'{"status": "LOGOUT_SUCCESS"}')

        else:
            conn.sendall(b'{"status": "FAIL", "reason": "Unknown action"}')

    except Exception as e:
        print(f"[ERROR] {e}")
        conn.sendall(b'{"status": "ERROR"}')
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # TCP socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse socket
        s.bind((HOST, PORT))
        s.listen()
        print(f"[START] Lobby Server listening on port {PORT}")

        try:
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr)).start()
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down server...")
            db = load_db()
            for user in db.values():
                user["online"] = False
            save_db(db)
            s.close()
            print("[INFO] Server closed cleanly.")

if __name__ == "__main__":
    main()
