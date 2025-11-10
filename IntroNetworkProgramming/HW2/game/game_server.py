import socket
import threading
import time
import sys
import random
import os

# 讓它能 import 根目錄的 common.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common import send_msg, recv_msg
from game_logic import GameLogic

TICK_MS = 500          # 每 0.5s 更新一次
SNAPSHOT_INTERVAL = 0.5 # 每 0.5秒 廣播一次狀態
LOBBY_PORT = 10090

class PlayerConn:
    def __init__(self, conn, addr, name, seed):
        self.conn = conn
        self.addr = addr
        self.name = name
        self.logic = GameLogic(seed)
        self.last_input = None
        self.role = None  # "P1" or "P2"

class GameServer:
    def __init__(self, port, room_id):
        self.port = port
        self.room_id = room_id
        self.players = []     # [PlayerConn, PlayerConn]
        self.seed = random.randint(0, 2**31)
        self.last_snapshot = time.time()
        self.lock = threading.Lock()
        self.tick = 0
        self.running = False
        self.max_duration = 120

    # === 接受連線 ===
    def start(self):
        print(f"[Game] Listening on port {self.port} (room {self.room_id})")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", self.port))
            s.listen(2)
            self.wait_for_players(s)
            # 開始主遊戲迴圈
            self.run_game()

    # === 等待兩位玩家連線 ===
    def wait_for_players(self, s):
        while len(self.players) < 2:
            conn, addr = s.accept()
            print(f"[Conn] {addr} connected")
            t = threading.Thread(target=self.handle_join, args=(conn, addr), daemon=True)
            t.start()
            # 等待 handle_join() 完成 append
            while len(self.players) < 2 and t.is_alive():
                time.sleep(0.1)

    # === 玩家連線流程 ===
    def handle_join(self, conn, addr):
        try:
            hello = recv_msg(conn)
            name = hello.get("userId", f"Player{len(self.players)+1}")
            with self.lock:
                player = PlayerConn(conn, addr, name, self.seed)
                player.role = f"P{len(self.players)+1}"
                self.players.append(player)
            print(f"[+] {name} joined as {player.role}")

            send_msg(conn, {
                "type": "WELCOME",
                "role": player.role,
                "seed": self.seed,
                "bagRule": "7bag",
                "msg": f"Welcome {player.role}"
            })

            # 獨立 thread 收玩家輸入
            threading.Thread(target=self.handle_input, args=(player,), daemon=True).start()
        except Exception as e:
            print(f"[Error] handle_join: {e}")

    # === 處理單一玩家輸入 ===
    def handle_input(self, player):
        while True:
            try:
                msg = recv_msg(player.conn)
                if not msg:
                    continue
                if msg["type"] == "INPUT":
                    action = msg["action"]
                    player.last_input = action

                    if action == "left":
                        player.logic.move_left()
                    elif action == "right":
                        player.logic.move_right()
                    elif action == "soft_drop":
                        player.logic.soft_drop()
                    elif action == "hard_drop":
                        player.logic.hard_drop()
                    elif action == "rotate_ccw":
                        player.logic.rotate_ccw()
                    elif action == "rotate_cw":
                        player.logic.rotate_cw()
                    elif action == "hold":
                        pass # TODO
            except Exception as e:
                print(f"[Error] recv from {player.name}: {e}")
                break

    # === 遊戲主迴圈 ===
    def run_game(self):
        self.running = True
        print("[Game] start.")

        self.start_time = time.time()

        while self.running:
            self.tick += 1
            # 遊戲狀態更新邏輯
            for p in self.players:
                if not p.logic.alive:
                    continue
                p.logic.soft_drop()

            # 定期廣播快照
            if time.time() - self.last_snapshot >= SNAPSHOT_INTERVAL:
                self.broadcast_snapshot()
                self.last_snapshot = time.time()
        

            # 測試結束條件：180 秒後自動結束
            all_dead = all(not p.logic.alive for p in self.players)
            elapsed = time.time() - self.start_time

            if all_dead:
                print("[Game] All players dead. Game over.")
                self.running = False

            elif elapsed >= self.max_duration:
                print(f"[Game] Time limit reached ({self.max_duration}s). Game over.")
                self.running = False

            if not self.running:
                self.broadcast_game_over()
                break
            time.sleep(TICK_MS / 1000.0)

    # === 廣播遊戲狀態 ===
    def broadcast_snapshot(self):
        snapshot = {
            "type": "SNAPSHOT",
            "tick": self.tick,
            "timestamp": time.time(),
            "players": [
                {
                    "name": p.name,
                    "score": p.logic.score,
                    "alive": p.logic.alive,
                    "board": p.logic.get_combined_board(),
                    "active": p.logic.active
                }
                for p in self.players
            ]
        }

        for p in self.players:
            try:
                send_msg(p.conn, snapshot)
            except Exception as e:
                print(f"[Error] send snapshot to {p.name}: {e}")
        # print(f"[SNAPSHOT] tick={self.tick}")

    # === 結束遊戲 ===
    def broadcast_game_over(self):
        results = {p.name: p.logic.score for p in self.players}
        start_time = self.start_time
        end_time = time.time()
        duration = round(time.time() - self.start_time, 2)
        scores = list(results.values())
        if len(set(scores)) == 1:
            winner = None
        else:
            winner = max(results, key=results.get)
        msg = {"type": "GAME_OVER", 
               "winner": winner or "平手",
               "results": results, 
               "duration": duration}
        for p in self.players:
            send_msg(p.conn, msg)
        
        try:
            lobby_sock = socket.create_connection(("127.0.0.1", LOBBY_PORT))
            send_msg(lobby_sock, {
                "action": "GAME_OVER",
                "data": {
                    "room_id": self.room_id,
                    "result": results,
                    "startAt": start_time,
                    "endAt": end_time
                }
            })
            lobby_sock.close()
        except Exception as e:
            print(f"[GameServer] Failed to report to lobby: {e}")

        print(f"[Game Over] Results: {results}")

# === 主程式入口 ===
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 game_server.py <port> <room_id>")
        sys.exit(1)
    port = int(sys.argv[1])
    room_id = int(sys.argv[2])
    server = GameServer(port, room_id)
    server.start()
