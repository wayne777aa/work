import socket
import threading
import subprocess
import random
import os
from datetime import datetime
from protocal import send_msg, recv_msg

# ==============================
#  基本參數
# ==============================
DB_HOST = "127.0.0.1"
DB_PORT = 10080

BIND_HOST  = "0.0.0.0"

LOBBY_HOST = "127.0.0.1" # change for local
# LOBBY_HOST = "140.113.17.12" # change for remote
LOBBY_PORT = 10090

# ============================================================
# Lobby Server 狀態
# ============================================================
player_states = {}  # username -> {conn, status, room_id, versions, can_review}
room_states = {}    # room_id -> {name, host, members, game_id, status}

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

# 廣播給所有玩家（可選擇只發給 idle 狀態的玩家）
def broadcast(action, data, exclude=None, only_idle=False):
    for username, state in player_states.items():
        if exclude and username == exclude:
            continue
        if only_idle and state["status"] != "idle":
            continue
        try:
            send_to(state["conn"], action, data)
        except Exception as e:
            print(f"[Broadcast error] {username}: {e}")

# 發訊息給該房間內所有人
def send_to_room(room_id, action, data, exclude=None):
    if room_id not in room_states:
        return
    for username  in room_states[room_id]["members"]:
        if exclude and username  == exclude:
            continue
        if username  in player_states:
            conn = player_states[username]["conn"]
            send_to(conn, action, data)

# 找出一個可用的 TCP port
def find_free_port(start=12000, end=13000):
    while True:
        port = random.randint(start, end)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue

# 離線或登出時呼叫清理邏輯
def remove_player(user):
    if user not in player_states:
        return  # 已經清理過了

    room_id = player_states[user].get("room_id")

    # ===== 在房間內：移除玩家 =====
    if room_id and room_id in room_states:
        room = room_states[room_id]

        # 先移除玩家
        if user in room["members"]:
            room["members"].remove(user)

        # ----- 房主離開：要轉交或刪除 -----
        if room["host"] == user:
            if len(room["members"]) > 0:
                new_host = room["members"][0]
                # 查 new_host 的 user_id
                res = db_request({
                    "collection": "User",
                    "action": "read",
                    "data": {"name": new_host}
                })
                new_host_id = res["data"]["row"][0]

                room["host"] = new_host

                send_to_room(room_id, "room_new_host", {"host": new_host})

                # 更新 DB
                db_request({
                    "collection": "Room",
                    "action": "update",
                    "data": {
                        "id": room_id,
                        "hostUserId": new_host_id,
                        "status": room["status"]
                    }
                })

            else:
                # 房間沒人 → 要刪除
                db_request({
                    "collection": "Room",
                    "action": "delete",
                    "data": {"id": room_id}
                })

                if room_id in room_states:
                    del room_states[room_id]

                broadcast("room_closed", {"room_id": room_id})

    db_request({
        "collection": "User",
        "action": "set_online",
        "data": {"name": user, "online": 0}
    })
    # ===== 從玩家列表移除 =====
    del player_states[user]

    # ===== 廣播 =====
    broadcast("user_left", {"name": user})

# ============================================================
# 處理每個 Client
# ============================================================
def handle_client(conn, addr):
    print(f"[+] {addr} connected")
    user = None

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
            # ---------- 註冊 ----------
            if action == "register":
                name = data.get("name", "").strip()
                pwd  = data.get("passwordHash", "").strip()

                if not name or not pwd:
                    send_to(conn, "error", {"msg": "Username/password cannot be empty"})
                    continue

                res = db_request({
                    "collection": "User",
                    "action": "read",
                    "data": {"name": name}
                })

                if res["data"]["row"] is not None:
                    send_to(conn, "error", {"msg": "User already exists"})
                    continue

                res = db_request({
                    "collection": "User",
                    "action": "create",
                    "data": data
                })

                send_to(conn, res["action"], res["data"])
                continue

            # ---------- 登入 ----------
            elif action == "login":
                name = data.get("name", "").strip()
                pwd  = data.get("passwordHash", "").strip()

                if not name or not pwd:
                    send_to(conn, "error", {"msg": "Username/password cannot be empty"})
                    continue

                res = db_request({
                    "collection": "User",
                    "action": "read",
                    "data": {"name": name}
                })

                if res["action"] != "user_read":
                    send_to(conn, "error", {"msg": "User not found"})
                    continue

                row = res["data"]["row"]  # DB 回傳 row tuple or dict
                if not row:
                    send_to(conn, "error", {"msg": "User not found"})
                    continue
                stored_hash = row[2]

                if pwd != stored_hash:
                    send_to(conn, "error", {"msg": "Wrong password"})
                    continue

                if name in player_states:
                    send_to(conn, "error", {"msg": "User already logged in"})
                    continue

                db_request({
                    "collection": "User",
                    "action": "set_online",
                    "data": {"name": name, "online": 1}
                })

                user = name

                client_versions = data.get("versions") or {}
                norm_versions = {}
                if isinstance(client_versions, dict):
                    for k, v in client_versions.items():
                        try:
                            gid = int(k)
                        except (TypeError, ValueError):
                            continue
                        norm_versions[gid] = v

                player_states[user] = {
                    "conn": conn,
                    "status": "idle",
                    "room_id": None,
                    "versions": norm_versions
                }

                send_to(conn, "login_success", {"name": user})
                broadcast("user_joined", {"name": user}, exclude=user)
                continue

            # ---------- 登出 ----------
            elif action == "logout":
                if user:
                    send_to(conn, "logout_success", {})
                    remove_player(user)
                    
                try:
                    conn.close()
                except:
                    pass

                break

            # ---------- 列出線上使用者 ----------
            elif action == "list_users":
                online_users = [
                    {"name": user, "status": st["status"], "room_id": st["room_id"]}
                    for user, st in player_states.items()
                ]
                send_to(conn, "users", {"list": online_users})
                continue

            # =====================================================
            # 房間相關操作
            # =====================================================
            # ---------- 建立房間 ----------
            elif action == "create_room":
                if not user:
                    send_to(conn, "error", {"msg": "Login first"})
                    continue

                # 建立 DB 紀錄
                req_data = {
                    "name": data.get("name", f"{user}_room"),
                    "hostUserId": user,
                    "status": "idle",
                    "createdAt": datetime.now().isoformat()
                }

                res = db_request({
                    "collection": "Room",
                    "action": "create",
                    "data": req_data
                })

                if res["action"] != "room_created":
                    send_to(conn, "error", {"msg": "DB create failed"})
                    continue

                room_id = res["data"]["room_id"]
                
                # 更新 Lobby 狀態
                room_states[room_id] = {
                    "name": req_data["name"],
                    "host": user,
                    "members": [user],
                    "game_id": None,
                    "status": "idle"
                }

                player_states[user]["status"] = "in_room"
                player_states[user]["room_id"] = room_id

                send_to(conn, "room_created", {"room_id": room_id})
                broadcast("new_room_created", {"room_id": room_id}, exclude=user)
                continue

            # ---------- 查詢房間 ----------
            elif action == "list_rooms":
                res = db_request({
                    "collection": "Room",
                    "action": "query",
                    "data": {}
                })

                if res["action"] != "room_query":
                    send_to(conn, "error", {"msg": "DB query failed"})
                    continue

                rows = res["data"]["rows"]
                out = []

                for row in rows:
                    rid, name, host, status, createdAt = row

                    # 更新本地快取
                    if rid not in room_states:
                        room_states[rid] = {
                            "name": name,
                            "host": host,
                            "members": [],
                            "game_id": None,
                            "status": status,
                        }

                    room = room_states[rid]
                    game_id = room.get("game_id")
                    game_name = None
                    if game_id is not None:
                        g_res = db_request({
                            "collection": "Game",
                            "action": "read",
                            "data": {"id": game_id}
                        })
                        if g_res.get("action") == "game_read":
                            game_name = g_res["data"]["name"]

                    # 顯示 DB 資料 + 即時人數
                    out.append({
                        "id": rid,
                        "name": room["name"],
                        "host": room["host"],
                        "members": len(room["members"]),
                        "member_list": list(room["members"]),
                        "status": room["status"],
                        "game_id": game_id,
                        "game_name": game_name,
                        "createdAt": createdAt
                    })

                send_to(conn, "rooms", {"list": out})
                continue
                
            # ---------- 加入房間 ----------
            elif action == "join_room":
                room_id = data["room_id"]

                if room_id not in room_states:
                    send_to(conn, "error", {"msg": "Room not found"})
                    continue

                room = room_states[room_id]

                # 防止重複加入
                if user in room["members"]:
                    send_to(conn, "error", {"msg": "Already in room"})
                    continue

                # 檢查人數上限
                if len(room["members"]) >= 2:
                    send_to(conn, "error", {"msg": "Room full"})
                    continue

                room["members"].append(user)
                player_states[user]["status"] = "in_room"
                player_states[user]["room_id"] = room_id

                send_to(conn, "room_joined", {"room_id": room_id})
                send_to_room(room_id, "room_member_joined", {"user": user}, exclude=user)
                continue
                
            # ---------- 離開房間 ----------
            elif action == "leave_room":
                room_id = player_states[user]["room_id"]

                if room_id not in room_states:
                    send_to(conn, "error", {"msg": "Room not found"})
                    continue

                room = room_states[room_id]

                if user not in room["members"]:
                    send_to(conn, "error", {"msg": "Not in room"})
                    continue
                
                # 從成員名單移除自己
                room["members"].remove(user)
                player_states[user]["status"] = "idle"
                player_states[user]["room_id"] = None

                # 若房主離開，改派或關房
                if room["host"] == user:
                    if len(room["members"]) > 0:
                        # 房主離開但還有人 → 自動讓第一個人成為新房主
                        new_host = room["members"][0]
                        room["host"] = new_host
                        send_to_room(room_id, "room_new_host", {"host": new_host})
                        db_request({
                            "collection": "Room",
                            "action": "update",
                            "data": {
                                "id": room_id,
                                "hostUserId": new_host,
                                "status": room["status"]
                            }
                        })
                    else:
                        # 沒人了 → 刪除房間
                        db_request({"collection": "Room", "action": "delete", "data": {"id": room_id}})
                        del room_states[room_id]
                        
                # 非房主離開
                else:
                    send_to_room(room_id, "room_member_left", {"user": user})

                send_to(conn, "room_left", {"room_id": room_id})
                continue

            # ---------- 查詢玩家所在房間資訊 ----------
            elif action == "get_room_info":
                if not user:
                    send_to(conn, "error", {"msg": "Login first"})
                    continue

                ps = player_states.get(user)
                if not ps or not ps.get("room_id"):
                    send_to(conn, "error", {"msg": "Not in room"})
                    continue

                room_id = ps["room_id"]
                room = room_states.get(room_id)

                # 理論上 room_states 一定要有，如果沒有就試著從 DB 撈一份回來補
                if room is None:
                    res = db_request({
                        "collection": "Room",
                        "action": "read",
                        "data": {"id": room_id}
                    })
                    if res.get("action") != "room_read" or not res["data"]["row"]:
                        send_to(conn, "error", {"msg": "Room not found"})
                        continue

                    rid, name, hostUserId, status, createdAt = res["data"]["row"]
                    room = room_states[room_id] = {
                        "name": name,
                        "host": hostUserId,
                        "members": [],
                        "game_id": None,
                        "status": status,
                    }

                # 補上 game_name（如果選過遊戲）
                game_id = room.get("game_id")
                game_name = None
                if game_id is not None:
                    g_res = db_request({
                        "collection": "Game",
                        "action": "read",
                        "data": {"id": game_id}
                    })
                    if g_res.get("action") == "game_read":
                        game_name = g_res["data"]["name"]

                send_to(conn, "room_info", {
                    "id": room_id,
                    "name": room["name"],
                    "host": room["host"],
                    "members": list(room["members"]),
                    "status": room["status"],
                    "game_id": game_id,
                    "game_name": game_name,
                })
                continue

            # =====================================================
            # 遊戲相關操作
            # =====================================================
            # ---------- 列出遊戲 ----------
            elif action == "list_games":
                res = db_request({
                    "collection": "Game",
                    "action": "query",
                    "data": {}
                })

                if res["action"] != "game_query":
                    send_to(conn, "error", {"msg": "Failed to query games"})
                    continue

                # 轉發給 client
                send_to(conn, "game_list", {"games": res["data"]})

            # ---------- 取得遊戲資訊 ------
            elif action == "get_game_info":
                lookup = {}
                if "id" in data:
                    lookup["id"] = data["id"]
                elif "name" in data:
                    lookup["name"] = data["name"]
                else:
                    send_to(conn, "error", {"msg": "id or name required"})
                    continue

                res = db_request({
                    "collection": "Game",
                    "action": "read",
                    "data": lookup
                })

                if res["action"] != "game_read":
                    send_to(conn, "error", {"msg": "Game not found"})
                    continue

                game_info = res["data"]
                game_id = game_info["id"]

                # 讀取版本列表
                version_res = db_request({
                    "collection": "GameVersion",
                    "action": "query",
                    "data": {"gameId": game_id}
                })

                versions = version_res["data"] if version_res["action"] == "gameversion_query" else []

                # 讀取評論列表
                review_res = db_request({
                    "collection": "Review",
                    "action": "query",
                    "data": {"gameId": game_id}
                })

                reviews = review_res["data"] if review_res["action"] == "review_query" else []

                # 平均評分
                avg_res = db_request({
                    "collection": "Review",
                    "action": "avg",
                    "data": {"gameId": game_id}
                })

                avg_rating = avg_res["data"].get("avg", None) if avg_res["action"] == "review_avg" else None

                send_to(conn, "game_info", {
                    "game": game_info,
                    "versions": versions,
                    "reviews": reviews,
                    "avg_rating": avg_rating
                })
                continue

            # ---------- 下載遊戲 ----------
            elif action == "download_game":
                lookup = {}
                if "id" in data:
                    lookup["id"] = data["id"]
                elif "name" in data:
                    lookup["name"] = data["name"]
                else:
                    send_to(conn, "error", {"msg": "id or name required"})
                    continue

                res = db_request({
                    "collection": "Game",
                    "action": "read",
                    "data": lookup
                })

                if res["action"] != "game_read":
                    send_to(conn, "error", {"msg": "Game not found"})
                    continue


                game = res["data"]
                if game.get("status") != "active":
                    send_to(conn, "error", {"msg": "該遊戲已被開發者下架，無法下載"})
                    continue

                game_info = res["data"]
                game_id = game_info["id"]
                game_version = game_info["latestVersion"]

                res2 = db_request({
                    "collection": "GameVersion",
                    "action": "read",
                    "data": {"gameId": game_id, "version": game_version}
                })

                row = res2["data"]["row"]
                if not row:
                    send_to(conn, "error", {"msg": "Version not found"})
                    continue

                zip_path = row[3]   # zipPath
                size = os.path.getsize(zip_path)

                send_to(conn, "download_header", {
                    "game_id": game_id,
                    "version": game_version,
                    "size": size
                })

                # binary data
                with open(zip_path, "rb") as f:
                    conn.sendall(f.read())

                # 玩家剛下載完 → 更新 server 上的版本紀錄
                if user in player_states:
                    player_states[user].setdefault("versions", {})[game_id] = game_version

            # ---------- 新增遊戲評論 ------
            elif action == "add_review":
                game_id = data.get("game_id")
                rating_raw  = data.get("rating")
                comment = data.get("comment")
            
                if not user:
                    send_to(conn, "error", {"msg": "Not logged in"})
                    continue

                # 只允許「剛剛被發 review_prompt 的那一款遊戲」
                ps = player_states.get(user)
                allowed = False
                if ps:
                    can = ps.get("can_review")
                    if can and can.get("game_id") == game_id:
                        allowed = True
                if not allowed:
                    send_to(conn, "error", {"msg": "You can only review right after finishing a game"})
                    continue

                # 嘗試轉成 int，若失敗直接擋掉
                try:
                    rating = int(rating_raw)
                except:
                    send_to(conn, "error", {"msg": "Rating must be an integer"})
                    continue

                if rating < 1 or rating > 5:
                    send_to(conn, "error", {"msg": "Rating must be an integer between 1 and 5"})
                    continue

                res = db_request({
                    "collection": "Review",
                    "action": "create",
                    "data": {
                        "gameId": game_id,
                        "user": user,
                        "rating": rating,
                        "comment": comment
                    }
                })

                if res["action"] != "review_created":
                    send_to(conn, "error", {"msg": "Failed to add review"})
                    continue

                # 評完就把權利用掉（避免同一局一直刷）
                if ps:
                    ps["can_review"] = None

                send_to(conn, "review_added", {})
                continue

            # ---------- 選擇遊戲 ----------
            elif action == "select_game":
                room_id = player_states[user]["room_id"]

                if not room_id:
                    send_to(conn, "error", {"msg": "Not in room"})
                    continue

                # 使用 id 或 name 都可
                lookup = {}
                if "game_id" in data:
                    lookup["id"] = data["game_id"]
                elif "game_name" in data:
                    lookup["name"] = data["game_name"]
                else:
                    send_to(conn, "error", {"msg": "game_id or game_name required"})
                    continue

                res = db_request({"collection": "Game", "action": "read", "data": lookup})

                if res["action"] != "game_read":
                    send_to(conn, "error", {"msg": "Game not found"})
                    continue

                game_info = res["data"]

                if game_info.get("status") != "active":
                    send_to(conn, "error", {"msg": "該遊戲已被開發者下架，無法在新房間使用"})
                    continue

                room = room_states[room_id]

                if room["host"] != user:
                    send_to(conn, "error", {"msg": "Only host can choose game"})
                    continue

                room["game_id"] = game_info["id"]  # 更新選擇

                # 廣播給房間內所有玩家
                send_to_room(room_id, "game_selected", {
                    "game_id": game_info["id"],
                    "game_name": game_info["name"],
                    "latest_version": game_info["latestVersion"],
                    "description": game_info["description"]
                })
                continue

            # ---------- 開始遊戲 ----------
            elif action == "start_game":
                room_id = player_states[user]["room_id"]

                if not room_id or room_id not in room_states:
                    send_to(conn, "error", {"msg": "Room not found"})
                    continue

                room = room_states[room_id]

                if room["host"] != user:
                    send_to(conn, "error", {"msg": "Only host can start"})
                    continue

                if len(room["members"]) != 2:
                    send_to(conn, "error", {"msg": "Need 2 players to start"})
                    continue

                if "game_id" not in room or room["game_id"] is None:
                    send_to(conn, "error", {"msg": "No game selected"})
                    continue

                game_id = room["game_id"]

                res = db_request({
                    "collection": "Game",
                    "action": "read",
                    "data": {"id": game_id}
                })

                if res["action"] != "game_read":
                    send_to(conn, "error", {"msg": "Invalid game"})
                    continue

                game = res["data"]

                if game.get("status") != "active":
                    send_to(conn, "error", {"msg": "該遊戲已被開發者下架，無法建立新遊戲局"})
                    continue

                latest_version = res["data"]["latestVersion"]
                game_name = res["data"]["name"]

                # ======== 檢查所有玩家版本 ========
                outdated_players = []
                for p in room["members"]:
                    versions = player_states.get(p, {}).get("versions", {})
                    player_ver = versions.get(game_id)
                    if player_ver != latest_version:
                        outdated_players.append(p)

                if outdated_players:
                    # 給版本過期的玩家各自發 update_required
                    for p in outdated_players:
                        conn_p = player_states[p]["conn"]
                        send_to(conn_p, "update_required", {
                            "game_id": game_id,
                            "game_name": game_name,
                            "latest_version": latest_version
                        })

                    # 告知房主是哪幾位玩家版本落後
                    send_to(conn, "update_required_list", {
                        "missing_players": outdated_players,
                        "latest_version": latest_version
                    })

                    continue  # 不啟動遊戲

                # 1. 找空 port
                port = find_free_port()

                try:
                    subprocess.Popen([ # TODO: 要設定server.py的開啟條件，還有遊戲的資料夾
                        "python3",
                        f"server_games/{game_name}/game_server.py",
                        str(port),
                        str(room_id)
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                    )
                except Exception as e:
                    send_to(conn, "start_game_failed", {"msg": str(e)})
                    continue

                # 2. 通知房間內所有玩家遊戲開始
                send_to_room(room_id, "game_start", {
                    "game_id": game_id,
                    "game_name": game_name,
                    "host": LOBBY_HOST,
                    "port": port,
                    "version": latest_version
                })

                # 3. 更新房間狀態
                room["status"] = "playing"
                db_request({
                    "collection": "Room",
                    "action": "update",
                    "data": {"id": room_id, "status": "playing"}
                })


                print(f"[Lobby] Room {room_id} started game on port {port}")

            # ---------- GAME OVER ---------- 
            elif action == "GAME_OVER":
                room_id = data.get("room_id")

                room = room_states.get(room_id)
                if room:
                    room_states[room_id]["status"] = "idle"
                    print(f"[Lobby] Room {room_id} game ended.")
                else:
                    print(f"[Lobby] Room {room_id} game ended (unknown room).")

                db_request({
                    "collection": "Room",
                    "action": "update",
                    "data": {"id": room_id, "status": "idle"}
                })

                # 這一局是哪個遊戲？
                if not room:
                    continue
                game_id = room.get("game_id")
                if not game_id:
                    continue

                # 查一下遊戲名字
                res_game = db_request({
                    "collection": "Game",
                    "action": "read",
                    "data": {"id": game_id}
                })
                game_name = None
                if res_game.get("action") == "game_read":
                    game_name = res_game["data"].get("name")

                # 給房內每個玩家一個「可針對這款遊戲評分」的權利
                if game_name:
                    for username in room["members"]:
                        ps = player_states.get(username)
                        if not ps:
                            continue
                        # 記住這個人可以評哪個遊戲
                        ps["can_review"] = {"game_id": game_id}

                        conn_u = ps["conn"]
                        send_to(conn_u, "review_prompt", {
                            "game_id": game_id,
                            "game_name": game_name
                        })
                continue
                
            # =====================================================
            # UNKNOWN
            # =====================================================
            else:
                send_to(conn, "error", {"msg": f"Unknown action"})

    except Exception as e:
        print(f"[Error] {addr}: {e}")

    finally:
        if user:
            remove_player(user)

        conn.close()
        print(f"[-] {addr} disconnected")


# -------------------------------------------------
# 伺服器主程式
# -------------------------------------------------
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((BIND_HOST, LOBBY_PORT))
    s.listen(5)
    print(f"[Lobby] listening on {BIND_HOST}:{LOBBY_PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
