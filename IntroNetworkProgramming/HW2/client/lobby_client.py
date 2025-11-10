import socket
import threading
import sys
import os

# 讓它能 import 根目錄的 common.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common import send_msg, recv_msg


class LobbyClient:
    def __init__(self, host, port):
        self.sock = socket.create_connection((host, port))
        self.user = None
        self.room_id = None
        self.on_game_start = None      # callback
        self.pending_response = None   # 暫存同步請求結果
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)

        # 啟動接收 thread
        threading.Thread(target=self.listen_server, daemon=True).start()

    # === 基礎功能 ===
    def send_and_wait(self, obj):
        """送出一個請求，並同步等待下一個伺服器回應"""
        with self.cv:
            send_msg(self.sock, obj)
            self.pending_response = None
            self.cv.wait(timeout=3)  # 最多等3秒
            return self.pending_response or {"ok": False, "msg": "No response"}

    def listen_server(self):
        """單一接收thread：負責所有伺服器訊息"""
        while True:
            try:
                msg = recv_msg(self.sock)
                if not msg:
                    break

                msg_type = msg.get("type")

                # 🎮 遊戲開始通知
                if msg_type == "GAME_START":
                    print(f"[Lobby] Game start!")
                    if self.on_game_start:
                        self.on_game_start(msg)
                    print("> ", end="", flush=True)

                # 📢 房間內廣播（像是有玩家加入、離開）
                elif msg_type == "ROOM":
                    print(f"[Room] {msg['msg']}")
                    print("> ", end="", flush=True)

                # 🌐 系統訊息（如誰登入登出）
                elif msg_type == "SYSTEM":
                    print(f"[System] {msg['msg']}")
                    print("> ", end="", flush=True)

                elif msg_type == "INVITE":
                    print(f"[Invite] {msg['msg']}")
                    print("> ", end="", flush=True)

                # 若是一般請求回應（例如 list_rooms, create_room）
                with self.cv:
                    self.pending_response = msg
                    self.cv.notify_all()

            except Exception as e:
                print(f"[Lobby Error] {e}")
                break

    # === 封裝 API ===
    def register(self, name, email, password):
        return self.send_and_wait({
            "action": "register",
            "data": {
                "name": name,
                "email": email,
                "passwordHash": password
            }
        })

    def login(self, name, password):
        res = self.send_and_wait({
            "action": "login",
            "data": {
                "name": name,
                "passwordHash": password
            }
        })
        if res.get("ok"):
            self.user = name
        return res
    
    def list_users(self):
        return self.send_and_wait({
            "action": "list_users"
        })

    def list_rooms(self):
        return self.send_and_wait({
            "action": "list_rooms"
        })

    def create_room(self, name="MyRoom", visibility="public"):
        res = self.send_and_wait({
            "action": "create_room",
            "data": {
                "name": name,
                "visibility": visibility
            }
        })
        if res.get("ok"):
            self.room_id = res["room_id"]
        return res
    
    def invite_user(self, invitee):
        return self.send_and_wait({
            "action": "invite_player",
            "data": {"target": invitee}
        })

    def join_room(self, room_id):
        res = self.send_and_wait({
            "action": "join_room",
            "data": {"room_id": room_id}
        })
        if res.get("ok"):
            self.room_id = room_id
        return res
    
    def list_invites(self):
        return self.send_and_wait({
            "action": "list_invites"
        })
    
    def accept_invite(self, room_id):
        try:
            room_id = int(room_id)
        except ValueError:
            return {"ok": False, "msg": "Invalid room_id format"}
        
        return self.send_and_wait({
            "action": "accept_invite",
            "data": {"room_id": room_id}
        })

    def leave_room(self):
        return self.send_and_wait({
            "action": "leave_room"
        })

    def start_game(self):
        send_msg(self.sock, {"action": "start_game"})

    def exit(self):
        return self.send_and_wait({
            "action": "logout"
        })
    
    def list_gamelog(self):
        return self.send_and_wait({
            "action": "list_gamelog"
        })


