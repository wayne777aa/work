import socket
import threading
import subprocess
import random
import sys
import os
from datetime import datetime
from common import send_msg, recv_msg

# === 參數 ===
DB_HOST = "127.0.0.1"
DB_PORT = 10080
LOBBY_HOST = "127.0.0.1" # change for local
# LOBBY_HOST = "140.113.17.12" # change for remote
LOBBY_PORT = 10090
SYNC_ON_LIST = True  # 改成 False → 只查 DB，不更新本地快取

# -------------------------------------------------
# 與 DB Server 溝通的函式
# -------------------------------------------------
def db_request(req: dict) -> dict:
    # 將請求送到 DB Server,回傳結果 JSON
    try:
        with socket.create_connection((DB_HOST, DB_PORT), timeout=3) as db_sock:
            send_msg(db_sock, req)
            res = recv_msg(db_sock)
            return res
    except Exception as e:
        return {"ok": False, "msg": f"DB connection failed: {e}"}


# -------------------------------------------------
# 狀態管理
# -------------------------------------------------
player_states = {}  # username -> {conn, status, room_id, addr}
room_states = {}    # room_id -> {name, host, members, visibility, status}
room_invitations = {} # room_id -> set of invited player names

next_room_id = 1  # 簡單自增用


# 廣播給所有玩家（可選擇只發給 idle 狀態的玩家）
def broadcast(msg: dict, exclude_user=None, only_idle=False):
    for name, state in player_states.items():
        if exclude_user and name == exclude_user:
            continue
        if only_idle and state["status"] != "idle":
            continue
        try:
            send_msg(state["conn"], msg)
        except Exception as e:
            print(f"[Broadcast error] {name}: {e}")

# 發訊息給該房間內所有人
def send_to_room(room_id, msg: dict, exclude_user=None):
    if room_id not in room_states:
        return
    for name in room_states[room_id]["members"]:
        if exclude_user and name == exclude_user:
            continue
        if name in player_states:
            try:
                send_msg(player_states[name]["conn"], msg)
            except:
                pass

# 回傳線上玩家列表（含狀態）
def get_online_list():
    return [
        {"name": name, "status": s["status"], "room": s["room_id"]}
        for name, s in player_states.items()
    ]

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

# -------------------------------------------------
# 處理每個 client 的函式
# -------------------------------------------------
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

            # ---------- 註冊 ----------
            if action == "register":
                db_res = db_request({
                    "collection": "User",
                    "action": "create",
                    "data": data
                })
                send_msg(conn, db_res)

            # ---------- 登入 ----------
            elif action == "login":
                db_res = db_request({
                    "collection": "User",
                    "action": "read",
                    "data": {"name": data["name"]}
                })
                if db_res.get("ok") and db_res["data"]:
                    row = db_res["data"]
                    stored_hash = row[3]  # 第4欄 passwordHash
                    if stored_hash == data["passwordHash"]:
                        user = data["name"]
                        player_states[user] = {
                            "conn": conn,
                            "status": "idle",
                            "room_id": None,
                            "addr": addr
                        }
                        db_request({
                            "collection": "User",
                            "action": "update",
                            "data": {"name": user}
                        })
                        send_msg(conn, {"ok": True, "msg": f"Welcome {user}!"})
                        broadcast({"type": "SYSTEM", "msg": f"{user} joined the lobby."}, exclude_user=user)
                    else:
                        send_msg(conn, {"ok": False, "msg": "Wrong password"})
                else:
                    send_msg(conn, {"ok": False, "msg": "User not found"})

            # ---------- 登出 ----------
            elif action == "logout":
                if user and user in player_states:
                    # 若在房間內也要自動離開
                    room_id = player_states[user]["room_id"]
                    if room_id and room_id in room_states:
                        room = room_states[room_id]
                        if user in room["members"]:
                            room["members"].remove(user)
                        if room["host"] == user:
                            if len(room["members"]) > 0:
                                # 房主離開但還有人 → 自動讓第一個人成為新房主
                                new_host = room["members"][0]
                                room["host"] = new_host
                                room_states[room_id].update({
                                    "host": new_host,
                                    "status": room["status"]
                                })
                                send_to_room(room_id, {"type": "ROOM", "msg": f"{user} left. {new_host} is new host."})
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
                                broadcast({"type": "SYSTEM", "msg": f"Room {room_id} closed."})

                    for inv in room_invitations.values():
                        inv.discard(user)
                    
                    del player_states[user]
                    broadcast({"type": "SYSTEM", "msg": f"{user} left the lobby."})
                    send_msg(conn, {"ok": True, "msg": "Logged out"})
                break

            # ---------- 列出線上使用者 ----------
            elif action == "list_users":
                send_msg(conn, {"ok": True, "users": get_online_list()})

            # ========== 房間相關操作 ==========
            # ---------- 建立房間 ----------
            elif action == "create_room":
                if not user:
                    send_msg(conn, {"ok": False, "msg": "Login first"})
                    continue

                # 建立 DB 紀錄
                db_res = db_request({
                    "collection": "Room",
                    "action": "create",
                    "data": {
                        "name": data.get("name", f"{user}_room"),
                        "hostUserId": user,
                        "visibility": data.get("visibility", "public"),
                        "status": "idle",
                        "createdAt": datetime.now().isoformat()
                    }
                })

                if not db_res.get("ok"):
                    send_msg(conn, {"ok": False, "msg": "Room creation failed"})
                    continue

                room_id = db_res.get("room_id")
                
                # 更新 Lobby 狀態
                room_states[room_id] = {
                    "name": data.get("name", f"Room{room_id}"),
                    "host": user,
                    "members": [user],
                    "visibility": data.get("visibility", "public"),
                    "status": "idle"
                }

                player_states[user]["status"] = "in_room"
                player_states[user]["room_id"] = room_id
                room_invitations[room_id] = set() # 每間房的邀請列表

                send_msg(conn, {"ok": True, "msg": f"Room {room_id} created", "room_id": room_id})
                broadcast({"type": "SYSTEM", "msg": f"{user} created room {room_id}"}, exclude_user=user)

            # ---------- 查詢房間 ----------
            elif action == "list_rooms":
                db_res = db_request({
                    "collection": "Room",
                    "action": "query",
                    "data": {}
                })

                if not db_res.get("ok"):
                    send_msg(conn, {"ok": False, "msg": "Failed to query rooms from DB"})
                    continue

                db_rooms = db_res.get("data", [])
                rooms = []

                for r in db_rooms:
                    rid, name, host, visibility, status, createdAt = r

                    # 同步功能，更新本地快取
                    if SYNC_ON_LIST:
                        if rid not in room_states:
                            room_states[rid] = {
                                "name": name,
                                "host": host,
                                "members": [host],
                                "visibility": visibility,
                                "status": status
                            }
                        else:
                            # 若已存在，只更新狀態與基本欄位
                            room_states[rid].update({
                                "name": name,
                                "host": host,
                                "visibility": visibility,
                                "status": status
                            })

                    # 顯示 DB 資料 + 即時人數
                    members = room_states[rid]["members"] if rid in room_states else []
                    rooms.append({
                        "id": rid,
                        "name": name,
                        "host": host,
                        "members": len(members),
                        "member_list": members,
                        "status": status,
                        "visibility": visibility,
                        "createdAt": createdAt
                    })

                send_msg(conn, {"ok": True, "rooms": rooms})

            # -----------邀請玩家-----------
            elif action == "invite_player":
                target = data.get("target")
                if not user or user not in player_states:
                    send_msg(conn, {"ok": False, "msg": "Login first"})
                    continue

                room_id = player_states[user]["room_id"]
                if not room_id or room_id not in room_states:
                    send_msg(conn, {"ok": False, "msg": "You are not in a room"})
                    continue

                room = room_states[room_id]
                if room["host"] != user:
                    send_msg(conn, {"ok": False, "msg": "Only host can invite"})
                    continue

                # 加入邀請清單
                if target not in player_states:
                    send_msg(conn, {"ok": False, "msg": f"User '{target}' is not online"})
                    continue

                invited_set = room_invitations.setdefault(room_id, set())
                if target in invited_set:
                    send_msg(conn, {"ok": False, "msg": f"{target} already invited"})
                    continue

                invited_set.add(target)
                send_msg(conn, {"ok": True, "msg": f"{target} invited to room {room_id}"})

                # 如果對方在線，通知他
                if target in player_states:
                    send_msg(player_states[target]["conn"], {
                        "type": "INVITE",
                        "from": user,
                        "room_id": room_id,
                        "msg": f"{user} invited you to join room {room_id}"
                    })

            # -----------查看邀請清單-----------
            elif action == "list_invites":
                if not user or user not in player_states:
                    send_msg(conn, {"ok": False, "msg": "Login first"})
                    continue

                invites = []
                for rid, invitees in room_invitations.items():
                    if user in invitees and rid in room_states:
                        room = room_states[rid]
                        invites.append({
                            "room_id": rid,
                            "from": room["host"],
                            "name": room["name"],
                            "visibility": room["visibility"]
                        })

                send_msg(conn, {"ok": True, "invites": invites})

            # -----------接受邀請-----------
            elif action == "accept_invite":
                if not user or user not in player_states:
                    send_msg(conn, {"ok": False, "msg": "Login first"})
                    continue

                room_id = data.get("room_id")
                if not room_id or room_id not in room_invitations:
                    send_msg(conn, {"ok": False, "msg": "Invalid room_id"})
                    continue

                # 檢查是否真的被邀請
                invited_set = room_invitations.get(room_id, set())
                if user not in invited_set:
                    send_msg(conn, {"ok": False, "msg": "You were not invited to this room"})
                    continue

                # 確保房間存在且沒滿
                if room_id not in room_states:
                    send_msg(conn, {"ok": False, "msg": "Room no longer exists"})
                    continue

                room = room_states[room_id]
                if len(room["members"]) >= 2:
                    send_msg(conn, {"ok": False, "msg": "Room is full"})
                    continue

                # 直接加入（等同 join_room）
                room["members"].append(user)
                player_states[user]["status"] = "in_room"
                player_states[user]["room_id"] = room_id

                # 清除邀請紀錄
                invited_set.remove(user)

                # db_request({
                #     "collection": "Room",
                #     "action": "update",
                #     "data": {"id": room_id, "status": room["status"]}
                # })

                send_msg(conn, {"ok": True, "msg": f"Joined room {room_id}"})
                send_to_room(room_id, {"type": "ROOM", "msg": f"{user} joined room {room_id}"}, exclude_user=user)
                
            # ---------- 加入房間 ----------
            elif action == "join_room":
                room_id = data.get("room_id")
                if room_id not in room_states:
                    send_msg(conn, {"ok": False, "msg": "Room not found"})
                    continue

                room = room_states[room_id]

                # 如果是 private，就檢查是否被邀請
                if room.get("visibility", "public") == "private":
                    if user != room["host"] and user not in room_invitations.get(room_id, set()):
                        send_msg(conn, {"ok": False, "msg": "This room is private. You are not invited."})
                        continue

                # 防止重複加入
                if user in room["members"]:
                    send_msg(conn, {"ok": False, "msg": "Already in this room"})
                    continue

                # 檢查人數上限
                if len(room["members"]) >= 2:
                    send_msg(conn, {"ok": False, "msg": "Room full"})
                    continue

                room["members"].append(user)
                player_states[user]["status"] = "in_room"
                player_states[user]["room_id"] = room_id

                # 如果這是私人房間，被邀請者進來後清除邀請紀錄
                if room_id in room_invitations and user in room_invitations[room_id]:
                    room_invitations[room_id].remove(user)

                # db_request({
                #     "collection": "Room",
                #     "action": "update",
                #     "data": {"id": room_id, "status": room["status"]}
                # })


                send_msg(conn, {"ok": True, "msg": f"Joined room {room_id}"})
                send_to_room(room_id, {"type": "ROOM", "msg": f"{user} joined room {room_id}"}, exclude_user=user)
                

            # ---------- 開始遊戲 ----------
            elif action == "start_game":
                if not user or user not in player_states:
                    send_msg(conn, {"ok": False, "msg": "Login first"})
                    continue

                room_id = player_states[user]["room_id"]
                if not room_id or room_id not in room_states:
                    send_msg(conn, {"ok": False, "msg": "You are not in a room"})
                    continue

                room = room_states[room_id]
                if room["host"] != user:
                    send_msg(conn, {"ok": False, "msg": "Only host can start game"})
                    continue

                if len(room["members"]) != 2:
                    send_msg(conn, {"ok": False, "msg": "Need exactly 2 players to start"})
                    continue

                # 1. 找空 port
                port = find_free_port()

                # 2. 啟動 Game Server
                try:
                    subprocess.Popen(["python3", "game/game_server.py", str(port), str(room_id)])
                    # subprocess.Popen(["python3", "game/game_server.py", str(port), str(room_id)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception as e:
                    send_msg(conn, {"ok": False, "msg": f"Failed to start Game Server: {e}"})
                    continue

                # 3. 更新房間狀態
                room["status"] = "playing"
                db_request({
                    "collection": "Room",
                    "action": "update",
                    "data": {"id": room_id, "status": "playing"}
                })

                # 4. 廣播給兩位玩家遊戲資訊
                game_info = {
                    "type": "GAME_START",
                    "msg": f"Game started on port {port}",
                    "host": LOBBY_HOST,
                    "port": port,
                    "room_id": room_id
                }
                send_to_room(room_id, game_info)
                print(f"[Lobby] Room {room_id} started game on port {port}")

            # ---------- 離開房間 ----------
            elif action == "leave_room":
                if not user or player_states[user]["room_id"] is None:
                    send_msg(conn, {"ok": False, "msg": "Not in room"})
                    continue

                room_id = player_states[user]["room_id"]
                room = room_states.get(room_id)
                if not room:
                    send_msg(conn, {"ok": False, "msg": "Room not found"})
                    continue

                if user not in room["members"]:
                    send_msg(conn, {"ok": False, "msg": "User not in this room"})
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
                        send_to_room(room_id, {"type": "ROOM", "msg": f"{user} left. {new_host} is new host."}, exclude_user=user)
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
                        broadcast({"type": "SYSTEM", "msg": f"Room {room_id} closed."}, exclude_user=user)
                        
                # 非房主離開
                else:
                    send_to_room(room_id, {"type": "ROOM", "msg": f"{user} left room {room_id}"}, exclude_user=user)

                send_msg(conn, {"ok": True, "msg": f"Left room {room_id}"})

            # ---------- GAME OVER ---------- 
            elif action == "GAME_OVER":
                room_id = data.get("room_id")
                result = data.get("result")

                db_request({
                    "collection": "GameLog",
                    "action": "create",
                    "data": {
                        "roomId": room_id,
                        "users": list(result.keys()),
                        "startAt": datetime.now().isoformat(),
                        "endAt": datetime.now().isoformat(),
                        "result": result
                    }
                })

                if room_id in room_states:
                    # 更新狀態：房間可再次加入或標記為結束
                    room_states[room_id]["status"] = "idle"
                    print(f"[Lobby] Room {room_id} game ended.")
                db_request({
                    "collection": "Room",
                    "action": "update",
                    "data": {"id": room_id, "status": "idle"}
                })
                
                send_msg(conn, {"ok": True})
            # ---------- SHOWLOG ---------- 
            elif action == "list_gamelog":
                db_res = db_request({
                    "collection": "GameLog",
                    "action": "query",
                    "data": {}
                })

                if not db_res.get("ok"):
                    send_msg(conn, {"ok": False, "msg": "Failed to get gamelog"})
                    continue

                logs = db_res.get("data", [])
                formatted = []
                for log in logs:
                    # 假設 GameLog schema 為 (id, roomId, users, startAt, endAt, result)
                    try:
                        lid, room_id, users, startAt, endAt, result = log
                        formatted.append({
                            "id": lid,
                            "roomId": room_id,
                            "users": users,
                            "startAt": startAt,
                            "endAt": endAt,
                            "result": result
                        })
                    except:
                        formatted.append(log)
                
                send_msg(conn, {"ok": True, "logs": formatted})
                

            else:
                send_msg(conn, {"ok": False, "msg": "Unknown action"})

    except Exception as e:
        print(f"[Error] {addr}: {e}")

    finally:
        try:
            if user and user in player_states:
                room_id = player_states[user].get("room_id")
                if room_id and room_id in room_states:
                    room = room_states[room_id]
                    if user in room["members"]:
                        room["members"].remove(user)
                    # 若房主離線，改派或關房
                    if room["host"] == user:
                        if len(room["members"]) > 0:
                            new_host = room["members"][0]
                            room["host"] = new_host
                            room_states[room_id].update({
                                "host": new_host,
                                "status": room["status"]
                            })
                            send_to_room(room_id, {
                                "type": "ROOM",
                                "msg": f"{user} disconnected. {new_host} is new host."
                            }, exclude_user=user)
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
                            db_request({
                                "collection": "Room",
                                "action": "delete",
                                "data": {"id": room_id}
                            })
                            if room_id in room_states:
                                del room_states[room_id]
                            broadcast({
                                "type": "SYSTEM",
                                "msg": f"Room {room_id} closed."
                            })
                
                # 清除所有邀請紀錄
                for inv in room_invitations.values():
                    inv.discard(user)

                del player_states[user]
                broadcast({"type": "SYSTEM", "msg": f"{user} disconnected."})
                
        except Exception as e:
            print(f"[Lobby] cleanup error: {e}")
        


        finally:
            conn.close()
            print(f"[-] {addr} disconnected")


# -------------------------------------------------
# 伺服器主程式
# -------------------------------------------------
def main():
    print(f"[Lobby] Listening on port {LOBBY_PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", LOBBY_PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
