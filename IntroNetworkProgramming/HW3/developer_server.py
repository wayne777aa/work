import socket
import threading
import os
import zipfile
from protocal import send_msg, recv_msg

# ==============================
#  基本參數
# ==============================
DB_HOST = "127.0.0.1"
DB_PORT = 10080

DEV_HOST = "127.0.0.1" # change for local
# DEV_HOST = "140.113.17.12" # change for remote
DEV_PORT = 10070

SERVER_GAMES_ROOT = "./server_games"

# 線上開發者狀態
developer_states = {}  # name -> {"conn": conn}


# ============================================================
# DB Connection Wrapper
# ============================================================
def db_request(req: dict) -> dict:
    # 將請求送到 DB Server,回傳結果 JSON
    try:
        with socket.create_connection((DB_HOST, DB_PORT), timeout=3) as db_sock:
            send_msg(db_sock, req)
            res = recv_msg(db_sock)
            return res
    except Exception as e:
        return {"action": "error", "data": {"msg": str(e)}}

def db_ok(res, expect_action):
    return res and res.get("action") == expect_action

# ============================================================
# Utilities
# ============================================================
def send_to(conn, action, data):
    send_msg(conn, {"action": action, "data": data})

def recv_binary(sock, size: int) -> bytes:
    buf = b""
    while len(buf) < size:
        part = sock.recv(size - len(buf))
        if not part:
            raise ConnectionError("Binary recv failed")
        buf += part
    return buf

# ==============================
# Auth：Developer register / login
# ==============================
def handle_register(conn, data):
    """
    Developer 註冊：
    collection = "Developer"
    action = "create" / "read"
    """
    name = data.get("name", "").strip()
    pwd = data.get("passwordHash", "").strip()

    if not name or not pwd:
        send_to(conn, "error", {"msg": "Username/password cannot be empty"})
        return

    # 檢查是否已存在
    res = db_request({
        "collection": "Developer",
        "action": "read",
        "data": {"name": name}
    })

    if res.get("action") == "developer_read" and res.get("data", {}).get("row"):
        send_to(conn, "error", {"msg": "Developer already exists"})
        return

    # 建立 Developer
    res = db_request({
        "collection": "Developer",
        "action": "create",
        "data": {
            "name": name,
            "passwordHash": pwd
        }
    })

    if not db_ok(res, "developer_created"):
        send_to(conn, "error", {"msg": "DB create developer failed"})
        return

    send_to(conn, "developer_created", {})


def handle_login(conn, data, current_dev_name):
    """
    Developer 登入：
    collection = "Developer"
    action = "read"
    """
    name = data.get("name", "").strip()
    pwd = data.get("passwordHash", "").strip()

    if not name or not pwd:
        send_to(conn, "error", {"msg": "Username/password cannot be empty"})
        return current_dev_name

    # 查 Developer
    res = db_request({
        "collection": "Developer",
        "action": "read",
        "data": {"name": name}
    })

    if res.get("action") != "developer_read":
        send_to(conn, "error", {"msg": "Developer not found"})
        return current_dev_name

    row = res.get("data", {}).get("row")
    if not row:
        send_to(conn, "error", {"msg": "Developer not found"})
        return current_dev_name

    # 假設欄位：id, name, passwordHash
    stored_hash = row[2]
    if pwd != stored_hash:
        send_to(conn, "error", {"msg": "Wrong password"})
        return current_dev_name

    # 檢查是否已在其他連線登入
    if name in developer_states and developer_states[name]["conn"] is not conn:
        send_to(conn, "error", {"msg": "Developer already logged in"})
        return current_dev_name

    developer_states[name] = {"conn": conn}
    send_to(conn, "login_success", {"name": name})
    return name

# ==============================
# 新遊戲第一次上架
# ==============================
def handle_dev_upload_new(conn, data, dev_name):
    """
    action = "dev_upload"
    data: {
        "game_name": str,
        "version": str,
        "description": str,
        "size": int   # zip 檔大小
    }
    """
    game_name = data.get("game_name", "").strip()
    version = data.get("version", "").strip()
    description = data.get("description", "")
    size = data.get("size", 0)

    if not game_name or not version or size <= 0:
        send_to(conn, "error",
                {"msg": "game_name / version / size invalid"})
        return

    # 1) 檢查有沒有同名遊戲
    res = db_request({
        "collection": "Game",
        "action": "read",
        "data": {"name": game_name}
    })

    if res.get("action") == "game_read":
        # 已經有這款遊戲 → 應該走 dev_upload_version
        send_to(conn, "error",
                {"msg": "Game already exists. Use dev_upload_version"})
        return
    elif res.get("action") == "error" and res.get("data", {}).get("msg") != "game_not_found":
        # 其他 DB 錯誤
        send_to(conn, "error", {"msg": "DB error on Game.read"})
        return

    # 2) 建立 Game
    res = db_request({
        "collection": "Game",
        "action": "create",
        "data": {
            "name": game_name,
            "developer": dev_name,
            "description": description,
            "latestVersion": version
        }
    })

    if not db_ok(res, "game_created"):
        send_to(conn, "error", {"msg": "DB create Game failed"})
        return

    game_id = res["data"]["game_id"]

    # 3) 準備 server_games 路徑
    game_dir = os.path.join(SERVER_GAMES_ROOT, game_name)
    os.makedirs(game_dir, exist_ok=True)
    zip_path = os.path.join(game_dir, f"{version}.zip")

    # 告訴 client 可以開始傳 zip
    send_to(conn, "dev_upload_ready", {
        "game_id": game_id,
        "zipPath": zip_path,
        "size": size
    })

    # 4) 收 zip binary
    binary = recv_binary(conn, size)
    with open(zip_path, "wb") as f:
        f.write(binary)

    # 解壓成目前最新版（Lobby 的 start_game 會直接跑這裡的 game_server.py）
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(game_dir)

    # 5) 建立 GameVersion
    res = db_request({
        "collection": "GameVersion",
        "action": "create",
        "data": {
            "gameId": game_id,
            "version": version,
            "zipPath": zip_path
        }
    })

    if not db_ok(res, "gameversion_created"):
        send_to(conn, "error", {"msg": "DB create GameVersion failed"})
        return

    send_to(conn, "dev_uploaded", {
        "game_id": game_id,
        "game_name": game_name,
        "version": version
    })


# ==============================
# 既有遊戲新增版本
# ==============================
def handle_dev_upload_version(conn, data, dev_name):
    """
    action = "dev_upload_version"
    data: {
        "game_name": str,
        "version": str,
        "description": str,
        "size": int
    }
    """
    game_name = data.get("game_name", "").strip()
    version = data.get("version", "").strip()
    description = data.get("description", "")
    size = data.get("size", 0)

    if not game_name or not version or size <= 0:
        send_to(conn, "error",
                {"msg": "game_name / version / size invalid"})
        return

    # 1) 先查 Game
    res = db_request({
        "collection": "Game",
        "action": "read",
        "data": {"name": game_name}
    })

    if res.get("action") != "game_read":
        send_to(conn, "error", {"msg": "Game not found"})
        return

    game_info = res["data"]
    game_id = game_info["id"]
    dev_db = game_info["developer"]

    if dev_db != dev_name:
        send_to(conn, "error",
                {"msg": "Permission denied: not this game's developer"})
        return

    # 2) 檢查 version 是否已存在
    res = db_request({
        "collection": "GameVersion",
        "action": "read",
        "data": {
            "gameId": game_id,
            "version": version
        }
    })

    if res.get("action") == "gameversion_read":
        row = res.get("data", {}).get("row")
        if row is not None:
            send_to(conn, "error", {"msg": "Version already exists"})
            return

    # 3) 更新 Game.latestVersion (+ 可選 description)
    update_data = {
        "id": game_id,
        "latestVersion": version
    }
    if description:
        update_data["description"] = description

    res = db_request({
        "collection": "Game",
        "action": "update",
        "data": update_data
    })

    if not db_ok(res, "game_updated"):
        send_to(conn, "error", {"msg": "Update Game failed"})
        return

    # 4) 準備 zip 路徑，通知 client 傳檔
    game_dir = os.path.join(SERVER_GAMES_ROOT, game_name)
    os.makedirs(game_dir, exist_ok=True)
    zip_path = os.path.join(game_dir, f"{version}.zip")

    send_to(conn, "dev_upload_ready", {
        "game_id": game_id,
        "zipPath": zip_path,
        "size": size
    })

    binary = recv_binary(conn, size)
    with open(zip_path, "wb") as f:
        f.write(binary)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(game_dir)

    # 5) 新增 GameVersion
    res = db_request({
        "collection": "GameVersion",
        "action": "create",
        "data": {
            "gameId": game_id,
            "version": version,
            "zipPath": zip_path
        }
    })

    if not db_ok(res, "gameversion_created"):
        send_to(conn, "error", {"msg": "DB create GameVersion failed"})
        return

    send_to(conn, "dev_uploaded_version", {
        "game_id": game_id,
        "game_name": game_name,
        "version": version
    })

# ==============================
# 下/上架遊戲
# ==============================
def handle_dev_offline(conn, data, dev_name):
    """
    action = "dev_offline"
    data: {"game_name": str}
    """
    game_name = data.get("game_name", "").strip()
    if not game_name:
        send_to(conn, "error", {"msg": "game_name required"})
        return

    # 1) 讀 Game
    res = db_request({
        "collection": "Game",
        "action": "read",
        "data": {"name": game_name}
    })

    if res.get("action") != "game_read":
        send_to(conn, "error", {"msg": "Game not found"})
        return

    game_info = res["data"]
    game_id = game_info["id"]

    # 只能下架自己的遊戲
    if game_info["developer"] != dev_name:
        send_to(conn, "error", {"msg": "Permission denied: not this game's developer"})
        return

    # 2) 設成 offline（不再接受新房間）
    res2 = db_request({
        "collection": "Game",
        "action": "set_status",
        "data": {
            "id": game_id,
            "status": "offline"
        }
    })

    if res2.get("action") != "game_status_updated":
        send_to(conn, "error", {"msg": "DB set_status failed"})
        return

    send_to(conn, "dev_offlined", {
        "game_id": game_id,
        "game_name": game_name
    })

def handle_dev_online(conn, data, dev_name):
    """
    action = "dev_online"
    data: {"game_name": str}
    """
    game_name = data.get("game_name", "").strip()
    if not game_name:
        send_to(conn, "error", {"msg": "game_name required"})
        return

    res = db_request({
        "collection": "Game",
        "action": "read",
        "data": {"name": game_name}
    })
    if res.get("action") != "game_read":
        send_to(conn, "error", {"msg": "Game not found"})
        return

    game_info = res["data"]
    game_id = game_info["id"]

    # 確認真的是這個開發者的遊戲
    if game_info["developer"] != dev_name:
        send_to(conn, "error", {"msg": "Permission denied: not this game's developer"})
        return

    # 把 status 改回 active
    res2 = db_request({
        "collection": "Game",
        "action": "set_status",
        "data": {"id": game_id, "status": "active"}
    })
    if res2.get("action") != "game_status_updated":
        send_to(conn, "error", {"msg": "DB set_status failed"})
        return

    send_to(conn, "dev_onlined", {
        "game_id": game_id,
        "game_name": game_name
    })
# ==============================
# 每個 Developer Client 的 handler
# ==============================
def handle_client(conn, addr):
    print(f"[Dev] {addr} connected")
    dev_name = None

    try:
        while True:
            req = recv_msg(conn)
            if req is None:
                break

            action = req.get("action")
            data = req.get("data", {})

            # =====================================================
            # 用戶相關操作
            # =====================================================
            # ----- 註冊 -----
            if action == "register":
                handle_register(conn, data)
                continue

            # ----- 登入 -----
            if action == "login":
                dev_name = handle_login(conn, data, dev_name)
                continue

            # 後面所有動作都需要已登入
            if not dev_name:
                send_to(conn, "error", {"msg": "Not logged in"})
                continue

            # ----- 新遊戲第一次上傳 -----
            if action == "dev_upload":
                handle_dev_upload_new(conn, data, dev_name)
                continue

            # ----- 既有遊戲新增版本 -----
            if action == "dev_upload_version":
                handle_dev_upload_version(conn, data, dev_name)
                continue

            # ----- 下架遊戲 -----
            if action == "dev_offline":
                handle_dev_offline(conn, data, dev_name)
                continue

            # ----- 上架遊戲 -----
            if action == "dev_online":
                handle_dev_online(conn, data, dev_name)
                continue

            # （可選）登出
            if action == "logout":
                send_to(conn, "logout_success", {})
                break

            # 未知 action
            send_to(conn, "error", {"msg": f"Unknown action: {action}"})

    except Exception as e:
        print(f"[Dev Error] {addr}: {e}")

    finally:
        # 清理登入狀態
        if dev_name and dev_name in developer_states:
            del developer_states[dev_name]

        try:
            conn.close()
        except:
            pass

        print(f"[Dev] {addr} disconnected")

# ==============================
# 伺服器主程式
# ==============================
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((DEV_HOST, DEV_PORT))
    s.listen(5)
    print(f"[DevServer] listening on {DEV_HOST}:{DEV_PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
