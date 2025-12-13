import socket
import threading
import os
import zipfile
import time
import json
import subprocess
from protocal import send_msg, recv_msg

LOBBY_HOST = "127.0.0.1" # change for local
# LOBBY_HOST = "140.113.17.12"  # change for remote
LOBBY_PORT = 10090

def load_local_versions(username):
    """
    從 downloads/<username>/_versions.json 讀取本機已下載的遊戲版本。
    回傳 dict: { "game_id(str)": "version" }
    """
    base_dir = os.path.join("downloads", username)
    path = os.path.join(base_dir, "_versions.json")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {}

def save_local_version(username, game_id, version):
    """
    更新 downloads/<username>/_versions.json 裡的某個遊戲版本。
    """
    base_dir = os.path.join("downloads", username)
    os.makedirs(base_dir, exist_ok=True)
    path = os.path.join(base_dir, "_versions.json")

    data = load_local_versions(username)
    data[str(game_id)] = version

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

class PlayerClient:
    def __init__(self, host=LOBBY_HOST, port=LOBBY_PORT):
        self.sock = socket.create_connection((host, port))
        self.pending = None
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)

        self.user = None
        self.room_id = None
        self.on_game_start = None

        self.pending_review = None   # {"game_id": ..., "game_name": ...}
        self.waiting_action = None   # 目前 send_and_wait 在等哪個 action

        self.pending_game_start = None   # 等主 thread 來啟動遊戲

        threading.Thread(target=self.listen, daemon=True).start()

    # -------------------------------
    # 等待一個同步回應
    # -------------------------------
    def send_and_wait(self, obj):
        with self.cv:
            send_msg(self.sock, obj)
            self.pending = None
            self.waiting_action = obj.get("action")   # 記住我正在等誰的回應
            self.cv.wait(timeout=5)
            resp = self.pending or {
                "action": "error",
                "data": {"msg": "timeout"}
            }
            self.waiting_action = None               # 收完就清掉
            return resp

    # -------------------------------
    # 接收 Server 所有訊息（async）
    # -------------------------------
    def listen(self):
        while True:
            try:
                msg = recv_msg(self.sock)
                if not msg:
                    print("[Disconnected]")
                    break

                action = msg.get("action")
                data = msg.get("data", {})

                # === 遊戲開始訊號 ===
                if action == "game_start":
                    print(f"[Game] 遊戲即將開始：{data}")
                    with self.cv:
                        self.pending_game_start = data
                    print("\n按 Enter 加入遊戲...")
                    continue

                # === 遊戲結束後：Lobby 要求可以評分 ===
                if action == "review_prompt":
                    game_id = data.get("game_id")
                    game_name = data.get("game_name", "<未知>")
                    self.pending_review = {
                        "game_id": game_id,
                        "game_name": game_name
                    }
                    print()
                    print(f"[Review] 上一局「{game_name}」已結束，可在選單中選擇『評分上一局遊戲』留下評價。")
                    print("> ", end="", flush=True)
                    continue

                # === 系統事件 (user join/leave, room updates 等) ===
                if action in ["user_joined", "user_left", "room_member_joined",
                              "room_member_left", "room_new_host", "new_room_created"]:
                    print()
                    print(f"[Event] {action}: {data}")
                    print("> ", end="", flush=True)
                    continue

                # === game_selected：同時當事件 + send_and_wait 的回應 ===
                if action == "game_selected":
                    with self.cv:
                        waiting_for_select = (self.waiting_action == "select_game")

                        if waiting_for_select:
                            # 房主那一邊：當作 send_and_wait(select_game) 的回應，不在這裡印
                            self.pending = msg
                            self.cv.notify_all()
                        else:
                            # 其他玩家：純事件，這裡排版印出來
                            game_name = data.get("game_name", "<未知>")
                            latest = data.get("latest_version", "")
                            desc = data.get("description", "")

                            print()
                            print("🎮 房間已選擇遊戲：")
                            line = f"   {game_name}"
                            if latest:
                                line += f" (版本 {latest})"
                            if desc:
                                line += f"\n   簡介：{desc}"
                            print(line)
                            print()
                            print("> ", end="", flush=True)
                
                    continue

                # === 有玩家需要更新遊戲版本 ===
                if action == "update_required":
                    game_name = data.get("game_name", "<未知>")
                    latest = data.get("latest_version", "")
                    print()
                    print("⚠️ 你沒有最新的遊戲版本，需要下載最新版本才能開始遊戲。")
                    print(f"   遊戲：{game_name}")
                    if latest:
                        print(f"   需要版本：{latest}")
                    print("> ", end="", flush=True)
                    continue

                if action == "update_required_list":
                    missing = data.get("missing_players", [])
                    latest = data.get("latest_version", "")
                    print()
                    print("⚠️ 有玩家未擁有最新的遊戲版本，無法開始遊戲。")
                    if missing:
                        print("   需要更新的玩家：" + ", ".join(missing))
                    if latest:
                        print(f"   需求版本：{latest}")
                    print("> ", end="", flush=True)
                    continue

                # === 一般錯誤訊息 ===
                if action == "error":
                    with self.cv:
                        if self.waiting_action is not None:
                            # 某個 send_and_wait() 在等 → 當作回應
                            self.pending = msg
                            self.cv.notify_all()
                        else:
                            # 沒人在等 → 當作 async 事件印出來（包含 start_game 的錯誤）
                            print()
                            print(f"⚠️ 伺服器錯誤：{data.get('msg', 'Unknown error')}")
                            print("> ", end="", flush=True)
                    continue

                # === 啟動遊戲失敗 ===
                if action == "start_game_failed":
                    print()
                    print(f"⚠️ 啟動遊戲失敗：{data.get('msg', 'unknown')}")
                    print("> ", end="", flush=True)
                    continue
                
                # === Download header (binary 資訊) ===
                if action == "download_header":
                    size = data.get("size", 0)

                    # 在 listen thread 裡直接把 zip 收完
                    try:
                        binary = self.recv_binary(size)
                    except Exception as e:
                        print("[Download Error]", e)
                        binary = b""

                    # 把 binary 塞回 msg，一起給 send_and_wait 用
                    msg["binary"] = binary

                    with self.cv:
                        self.pending = msg
                        self.cv.notify_all()
                    continue

                # === 一般同步回應 ===
                with self.cv:
                    self.pending = msg
                    self.cv.notify_all()

            except Exception as e:
                print("[Listen Error]", e)
                break

    # -------------------------------
    # binary 接收器
    # -------------------------------
    def recv_binary(self, size: int) -> bytes:
        buf = b''
        while len(buf) < size:
            part = self.sock.recv(size - len(buf))
            if not part:
                raise ConnectionError("Binary recv failed")
            buf += part
        return buf

    # ============================================================
    # API 封裝
    # ============================================================
    def register(self, name, password):
        res = self.send_and_wait({
            "action": "register",
            "data": {"name": name, "passwordHash": password}
        })
        return res

    def login(self, name, password):
        owned_versions = load_local_versions(name)
        res = self.send_and_wait({
            "action": "login",
            "data": {
                "name": name, 
                "passwordHash": password,
                "versions": owned_versions
            }
        })
        if res.get("action") == "login_success":
            self.user = name
        return res
    
    def logout(self):
        return self.send_and_wait({"action": "logout"})

    def list_users(self):
        return self.send_and_wait({"action": "list_users"})

    def list_rooms(self):
        return self.send_and_wait({"action": "list_rooms"})

    def create_room(self, name):
        res = self.send_and_wait({
            "action": "create_room",
            "data": {"name": name}
        })
        if res.get("action") == "room_created":
            self.room_id = res["data"]["room_id"]
        return res

    def join_room(self, room_id):
        res = self.send_and_wait({
            "action": "join_room",
            "data": {"room_id": room_id}
        })
        if res.get("action") == "room_joined":
            self.room_id = room_id
        return res

    def leave_room(self):
        return self.send_and_wait({"action": "leave_room"})

    def get_room_info(self):
        return self.send_and_wait({"action": "get_room_info"})

    def list_games(self):
        return self.send_and_wait({"action": "list_games"})
    
    def get_game_info(self, game_id=None, game_name=None):
        data = {}
        if game_id is not None:
            data["id"] = game_id
        elif game_name is not None:
            data["name"] = game_name
        else:
            raise ValueError("game_id or game_name required")

        return self.send_and_wait({
            "action": "get_game_info",
            "data": data
        })
    
    def download_game(self, game_id=None, game_name=None):
        data = {}
        if game_id is not None:
            data["id"] = game_id
        elif game_name is not None:
            data["name"] = game_name
        else:
            raise ValueError("game_id or game_name required")

        return self.send_and_wait({
            "action": "download_game",
            "data": data
        })

    def select_game(self, game_id=None, game_name=None):
        data = {}
        if game_id is not None:
            data["game_id"] = game_id
        elif game_name is not None:
            data["game_name"] = game_name
        else:
            raise ValueError("game_id or game_name required")

        return self.send_and_wait({
            "action": "select_game",
            "data": data
        })

    def start_game(self):
        try:
            send_msg(self.sock, {"action": "start_game", "data": {}})
            return {"action": "start_game_sent", "data": {}}
        except Exception as e:
            return {"action": "error", "data": {"msg": str(e)}}

    def add_review(self, game_id, rating, comment):
        return self.send_and_wait({
            "action": "add_review",
            "data": {
                "game_id": game_id,
                "rating": rating,
                "comment": comment
            }
        })

# ============================================================
# 工具：下載 ZIP → 解壓縮
# ============================================================
def save_and_extract(binary, dst_dir, game_name, version, username, game_id):
    os.makedirs(dst_dir, exist_ok=True)

    zip_path = os.path.join(dst_dir, f"{game_name}_{version}.zip")

    with open(zip_path, "wb") as f:
        f.write(binary)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(os.path.join(dst_dir, game_name))

    print(f"✅ 遊戲已下載並解壓縮到: {dst_dir}/{game_name}")

    if username is not None and game_id is not None:
        save_local_version(username, game_id, version)

def input_game_lookup():
    key = input("輸入 Game ID 或名稱: ").strip()
    if not key:
        return None, None

    # 全為數字就當作 ID
    if key.isdigit():
        return int(key), None
    # 其他就當作名稱
    return None, key


# ============================================================
# Player Menu
# ============================================================
def main():
    client = PlayerClient(LOBBY_HOST, LOBBY_PORT)

    print("=== Player Client ===")

    # -------------------------------
    # Login / Register
    # -------------------------------
    while True:
        print("\n1) Login\n2) Register")
        op = input("> ").strip()

        if op == "2":
            username = input("Username: ").strip()
            pw = input("Password: ").strip()
            res = client.register(username, pw)
            print(res)
            continue

        if op == "1":
            username = input("Username: ").strip()
            pw = input("Password: ").strip()
            res = client.login(username, pw)
            print(res)
            if res.get("action") == "login_success":
                break
            continue

        print("[Error] 無效選項")

    DOWNLOAD_DIR = f"./downloads/{username}"
    print(f"下載資料夾：{DOWNLOAD_DIR}") # DEBUG

    # ------------------------------------------------
    # 當 Lobby 說 game_start，就啟動對應版本的 game_client
    # ------------------------------------------------
    def launch_game_client(start_data):
        host = start_data.get("host")
        port = start_data.get("port")
        game_name = start_data.get("game_name")
        version = start_data.get("version") 

        if not host or not port or not game_name:
            print("❌ game_start 資料不完整:", start_data)
            return

        # 假設下載解壓後路徑是：downloads/<username>/<game_name>/game_client.py
        game_dir = os.path.join("downloads", username, game_name)
        client_py = os.path.join(game_dir, "game_client.py")

        if not os.path.exists(client_py):
            print(f"❌ 找不到 game_client.py: {client_py}")
            print("請先下載或更新遊戲。")
            return

        print(f"啟動遊戲程式：{client_py}")
        try:
            subprocess.run(
                ["python3", client_py, host, str(port), username, str(client.room_id)]
            )
        except Exception as e:
            print(f"⚠️ 無法啟動遊戲: {e}")

    def check_and_run_game():
        """如果有等待中的 game_start，就在主 thread 啟動遊戲並 block 住 menu。"""
        with client.cv:
            start_data = client.pending_game_start
            client.pending_game_start = None
        if start_data:
            launch_game_client(start_data)

    def do_review():
        if not client.pending_review:
            print("目前沒有可以評分的遊戲。")
            return

        game_id = client.pending_review["game_id"]
        game_name = client.pending_review["game_name"]
        print(f"\n=== 評分上一局遊戲：{game_name} ===")

        # 問評分
        while True:
            rating_str = input("請輸入評分 (1-5)：").strip()
            try:
                rating = int(rating_str)
            except ValueError:
                print("請輸入 1~5 的整數。")
                continue
            if not (1 <= rating <= 5):
                print("評分必須介於 1 到 5 之間。")
                continue
            break

        comment = input("評論（可留空）：").strip()

        res = client.add_review(game_id, rating, comment)
        if res.get("action") == "review_added":
            print("✅ 已送出評論，感謝你的回饋。")
            client.pending_review = None
        else:
            msg = res.get("data", {}).get("msg", res)
            print("❌ 評價失敗：", msg)

    # -------------------------------
    # Menu Loop
    # -------------------------------
    while True:
        # === 依照是否在房間內，顯示不同選單 ===
        check_and_run_game()
        if client.room_id is None:
            # -------- 大廳階段 --------
            print("\n=== Lobby Menu ===")
            print("1. 遊戲列表")
            print("2. 遊戲資訊")
            print("3. 下載遊戲")
            print("4. 房間列表")
            print("5. 建立房間")
            print("6. 加入房間")
            if client.pending_review:
                print("7. 評分上一局遊戲")
            print("0. 登出並離開")
            op = input("> ").strip()

            # 手滑按 Enter，一律當作「忽略」，並重新輸出menu
            if op == "":
                
                continue

            # 遊戲列表
            if op == "1":
                res = client.list_games()

                games_obj = res.get("data", {}).get("games", {})
                rows = games_obj.get("rows", [])

                print("\n=== 遊戲列表 ===")
                if not rows:
                    print("(目前沒有遊戲)")
                else:
                    for row in rows:
                        # Game table: id, name, developer, description, latestVersion
                        gid, name, developer, desc, latest, status = row

                        line = f"[{gid}] {name}"
                        if developer:
                            line += f" | 開發者: {developer}"
                        if latest:
                            line += f" | 最新版本: {latest}"
                        print(line)

                # 停住，等你看完
                input("\n按 Enter 返回選單...")

            # 遊戲資訊：可用 ID 或 名稱
            elif op == "2":
                res = client.list_games()

                games_obj = res.get("data", {}).get("games", {})
                rows = games_obj.get("rows", [])

                print("\n=== 遊戲列表 ===")
                if not rows:
                    print("(目前沒有遊戲)")
                else:
                    for row in rows:
                        # Game table: id, name, developer, description, latestVersion
                        gid, name, developer, desc, latest, status = row

                        line = f"[{gid}] {name}"
                        if developer:
                            line += f" | 開發者: {developer}"
                        if latest:
                            line += f" | 最新版本: {latest}"
                        print(line)

                print()
                gid, gname = input_game_lookup()
                if gid is None and gname is None:
                    print("輸入不可為空")
                    continue

                res2 = client.get_game_info(game_id=gid, game_name=gname)

                if res2.get("action") != "game_info":
                    print("❌ 取得遊戲資訊失敗:", res2)
                    input("\n按 Enter 返回選單...")
                    continue

                data = res2.get("data", {})
                game = data.get("game", {})

                versions_obj = data.get("versions", {})
                reviews_obj  = data.get("reviews", {})
                # 這兩個都是 {"rows": [...]} 的形式
                versions = versions_obj.get("rows", []) if isinstance(versions_obj, dict) else []
                reviews  = reviews_obj.get("rows", []) if isinstance(reviews_obj, dict) else []
                avg      = data.get("avg_rating")

                print("\n=== 遊戲資訊 ===")
                print(f"[{game.get('id')}] {game.get('name', '')}")

                dev = game.get("developer")
                if dev:
                    print(f"開發者: {dev}")

                latest = game.get("latestVersion")
                if latest:
                    print(f"最新版本: {latest}")

                if avg is not None:
                    try:
                        print(f"平均評分: {float(avg):.2f}")
                    except (TypeError, ValueError):
                        print(f"平均評分: {avg}")

                desc = game.get("description")
                if desc:
                    print("\n描述:")
                    print(desc)

                # 版本列表
                print("\n版本列表:")
                if not versions:
                    print("  (沒有版本紀錄)")
                else:
                    for v in versions:
                        # GameVersion: id, gameId, version, zipPath, createdAt
                        vid, game_id, ver, zip_path, created_at = v
                        print(f"  - {ver} ({created_at})")

                # 評論列表（只顯示前幾筆就好）
                print("\n評論:")
                if not reviews:
                    print("  (尚無評論)")
                else:
                    for r in reviews[:5]:
                        # Review: id, gameId, user, rating, comment, createdAt
                        rid, game_id, user, rating, comment, created_at = r
                        line = f"  - {user} 給 {rating} 分"
                        if comment:
                            line += f"：{comment}"
                        line += f"  ({created_at})"
                        print(line)

                input("\n按 Enter 返回選單...")

            # 下載遊戲：先列出遊戲，再問 ID/名稱
            elif op == "3":
                # 先顯示遊戲列表，讓使用者看名字
                res_list = client.list_games()
                games_obj = res_list.get("data", {}).get("games", {})
                rows = games_obj.get("rows", [])

                print("\n=== 遊戲列表 ===")
                if not rows:
                    print("(目前沒有遊戲)")
                else:
                    for row in rows:
                        # Game table: id, name, developer, description, latestVersion
                        gid, name, developer, desc, latest, status = row

                        line = f"[{gid}] {name}"
                        if developer:
                            line += f" | 開發者: {developer}"
                        if latest:
                            line += f" | 最新版本: {latest}"
                        print(line)

                print("\n選擇要下載的遊戲：")
                gid, gname = input_game_lookup()
                if gid is None and gname is None:
                    print("輸入不可為空")
                    continue

                header = client.download_game(game_id=gid, game_name=gname)

                if header["action"] != "download_header":
                    print("❌ 下載錯誤:", header)
                    continue

                h = header["data"]
                version = h["version"]
                game_id = h["game_id"]

                # 這是 listen() 剛剛幫你收好的 zip
                raw = header.get("binary", b"")
                if not raw:
                    print("❌ 下載失敗：沒有收到檔案內容")
                    continue

                size = len(raw)
                print(f"📥 已接收 {size} bytes")

                # 用 game_id 再查一次拿到正式名稱
                info = client.get_game_info(game_id=game_id)
                game_name = info["data"]["game"]["name"]

                save_and_extract(raw, DOWNLOAD_DIR, game_name, version, username, game_id)

            # 房間列表
            elif op == "4":
                res = client.list_rooms()
                rooms = res.get("data", {}).get("list", [])

                print("\n=== 房間列表 ===")
                if not rooms:
                    print("(目前沒有房間)")
                else:
                    for r in rooms:
                        rid = r.get("id")
                        name = r.get("name", "")
                        status = r.get("status", "")
                        members = r.get("member_list") or []
                        game_name = r.get("game_name")  # 可能是 None

                        line = f"[{rid}] {name}"
                        if members:
                            line += " | 成員: " + ", ".join(members)
                        else:
                            line += " | 成員: (無)"

                        line += f" | 狀態: {status}"
                        if game_name:
                            line += f" | 遊戲: {game_name}"

                        print(line)

                input("\n按 Enter 返回選單...")

            # 建立房間 #TODO
            elif op == "5":
                room_name = input("Room name: ").strip()
                res = client.create_room(room_name)
                print(res)

            # 加入房間 #TODO
            elif op == "6":
                res = client.list_rooms()
                rooms = res.get("data", {}).get("list", [])
                print("\n=== 房間列表 ===")
                if not rooms:
                    print("(目前沒有房間)")
                else:
                    for r in rooms:
                        rid = r.get("id")
                        name = r.get("name", "")
                        status = r.get("status", "")
                        members = r.get("member_list") or []
                        game_name = r.get("game_name")  # 可能是 None

                        line = f"[{rid}] {name}"
                        if members:
                            line += " | 成員: " + ", ".join(members)
                        else:
                            line += " | 成員: (無)"

                        line += f" | 狀態: {status}"
                        if game_name:
                            line += f" | 遊戲: {game_name}"

                        print(line)
                
                rid = input("\nRoom ID: ").strip()
                if not rid.isdigit():
                    print("Room ID 必須是數字")
                    continue
                res = client.join_room(int(rid))
                print(res)

            # 評分上一局遊戲
            elif op == "7" and client.pending_review:
                do_review()

            # 登出 #TODO
            elif op == "0":
                print(client.logout())
                break

            else:
                print("無效選項")
                input("\n按 Enter 返回選單...")

        else:
            check_and_run_game()
            # -------- 房間內階段 --------
            print(f"\n=== Room Menu (Room {client.room_id}) ===")
            print("1. 房間資訊")
            print("2. 選擇遊戲 (房主)")
            print("3. 開始遊戲 (房主)")
            print("4. 下載目前房間遊戲")
            print("5. 離開房間")
            if client.pending_review:
                print("6. 評分上一局遊戲")
            print("0. 登出並離開房間")
            op = input("> ").strip()

            if op == "":
                # 剛玩完遊戲回來、手滑按 Enter，一律當作「忽略」
                continue

            if op == "1":
                res = client.get_room_info()
                if res.get("action") != "room_info":
                    print("❌ 無法取得房間資訊:", res)
                    input("\n按 Enter 返回選單...")
                    continue

                info = res.get("data", {})

                print("\n=== 房間資訊 ===")
                print(f"房間 ID: {info.get('id')}")
                print(f"房間名稱: {info.get('name', '')}")
                print(f"狀態: {info.get('status', '')}")
                print(f"房主: {info.get('host', '')}")

                members = info.get("members") or []
                if members:
                    print("成員: " + ", ".join(members))
                else:
                    print("成員: (無)")

                game_id = info.get("game_id")
                game_name = info.get("game_name")
                if game_id is not None:
                    if game_name:
                        print(f"已選遊戲: {game_name} (ID={game_id})")
                    else:
                        print(f"已選遊戲: (ID={game_id}, 名稱未知)")
                else:
                    print("已選遊戲: (尚未選擇)")

                input("\n按 Enter 返回選單...")

            # 選擇遊戲（房主），用 ID/名稱都可以
            elif op == "2":
                # 先列出全部遊戲，讓房主看名稱 / ID
                res_list = client.list_games()
                games_obj = res_list.get("data", {}).get("games", {})
                rows = games_obj.get("rows", [])

                print("\n=== 遊戲列表 ===")
                if not rows:
                    print("(目前沒有遊戲)")
                else:
                    for row in rows:
                        # Game table: id, name, developer, description, latestVersion
                        gid, name, developer, desc, latest, status = row

                        line = f"[{gid}] {name}"
                        if developer:
                            line += f" | 開發者: {developer}"
                        if latest:
                            line += f" | 最新版本: {latest}"
                        print(line)

                print("\n選擇房間要遊玩的遊戲：(ID / 名稱)")
                gid, gname = input_game_lookup()
                if gid is None and gname is None:
                    print("輸入不可為空")
                    continue
                res = client.select_game(game_id=gid, game_name=gname)

                if res.get("action") != "game_selected":
                    print("❌ 選擇遊戲失敗:", res)
                else:
                    d = res.get("data", {})
                    game_name = d.get("game_name", "<未知>")
                    latest = d.get("latest_version", "")
                    desc = d.get("description", "")

                    print("\n✅ 已設定房間遊戲：")
                    print(f"   名稱：{game_name}")
                    if latest:
                        print(f"   版本：{latest}")
                    if desc:
                        print(f"   簡介：{desc}")

                input("\n按 Enter 返回房間選單...")

            # 開始遊戲（房主)
            elif op == "3":
                res = client.start_game()
                if res.get("action") == "error":
                    print("❌ 無法送出開始遊戲請求:", res)
                else:
                    print("✅ 已送出開始遊戲請求，等待遊戲開始或版本檢查結果...")

            # 下載目前房間遊戲
            elif op == "4":
                # 先看房間有沒有選遊戲
                res = client.get_room_info()
                if res.get("action") != "room_info":
                    print("❌ 無法取得房間資訊:", res)
                    input("\n按 Enter 返回選單...")
                    continue

                info = res.get("data", {})
                game_id = info.get("game_id")
                game_name = info.get("game_name")

                if game_id is None:
                    print("房間尚未選擇遊戲，請先等房主選擇。")
                    input("\n按 Enter 返回選單...")
                    continue

                # 跟 Lobby 的下載一樣，但直接用 game_id，不再問使用者
                header = client.download_game(game_id=game_id)

                if header.get("action") != "download_header":
                    print("❌ 下載錯誤:", header)
                    input("\n按 Enter 返回選單...")
                    continue

                h = header["data"]
                size    = h["size"]
                version = h["version"]
                real_gid = h["game_id"]

                # 保險起見，用 game_id 再查一次正式名稱（避免房間資訊沒帶名字）
                if not game_name:
                    info2 = client.get_game_info(game_id=real_gid)
                    game_name = info2["data"]["game"]["name"]

                print(f"📥 正在接收 {size} bytes...")

                raw = header.get("binary", b"")

                if not raw:
                    print("❌ 下載失敗：沒有收到檔案內容")
                    input("\n按 Enter 返回選單...")
                    continue

                save_and_extract(raw, DOWNLOAD_DIR, game_name, version, username, game_id)
                input("\n按 Enter 返回選單...")

            # 離開房間 # TODO
            elif op == "5":
                res = client.leave_room()
                print(res)
                client.room_id = None  # 簡單粗暴地直接清掉

            # 評分上一局遊戲
            elif op == "6" and client.pending_review:
                do_review()

            # 直接登出 # TODO
            elif op == "0":
                print(client.logout())
                break

            else:
                print("無效選項")
                input("\n按 Enter 返回選單...")

if __name__ == "__main__":
    main()