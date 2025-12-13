import socket
import threading
import time
import sys

from protocal import send_msg, recv_msg

LOBBY_HOST = "127.0.0.1"  # 和 lobby_server 裡的 LOBBY_HOST 保持一致
LOBBY_PORT = 10090

WIN_ROUNDS = 2       # 三戰兩勝
MAX_ROUNDS = 10

CHOICES = ["rock", "paper", "scissors"]

class PlayerConn:
    def __init__(self, conn, addr, name):
        self.conn = conn
        self.addr = addr
        self.name = name
        self.score = 0

class RPSServer:
    def __init__(self, port, room_id):
        self.port = port
        self.room_id = room_id
        self.players = []  # [PlayerConn, PlayerConn]
        self.running = False
        self.start_time = None

    def start(self):
        print(f"[RPS] Listening on port {self.port} (room {self.room_id})")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", self.port))
            s.listen(2)
            print("[RPS] after bind/listen")
            self.wait_for_players(s)
            print("[RPS] now have", len(self.players), "players")
            self.run_game()

    def wait_for_players(self, s):
        while len(self.players) < 2:
            conn, addr = s.accept()
            print(f"[RPS] {addr} connected")
            hello = recv_msg(conn)
            name = hello.get("userId", f"Player{len(self.players)+1}")
            player = PlayerConn(conn, addr, name)
            self.players.append(player)
            send_msg(conn, {
                "type": "WELCOME",
                "msg": f"Welcome {name}, 等待另一名玩家..."
            })
        # 兩個人都到了，通知開始
        for i, p in enumerate(self.players, start=1):
            send_msg(p.conn, {
                "type": "GAME_START",
                "msg": f"遊戲開始! 你是 Player {i}. 第一個到 {WIN_ROUNDS} 勝的贏)."
            })

    def run_game(self):
        self.running = True
        self.start_time = time.time()
        round_no = 1

        while self.running and round_no <= MAX_ROUNDS:
            # 啟動新一回合
            for p in self.players:
                send_msg(p.conn, {
                    "type": "ROUND_START",
                    "round": round_no
                })

            # 先同時要求所有玩家出拳（兩邊終端機會同時看到提示）
            for p in self.players:
                send_msg(p.conn, {
                    "type": "ASK_MOVE",
                    "round": round_no,
                    "valid": CHOICES
                })

            # 收兩邊出拳（會等到兩個人都出完才往下算結果）
            moves = {}
            for p in self.players:
                choice = self.recv_move(p, round_no)
                if choice is None:
                    # 有人斷線，直接結束
                    self.running = False
                    break
                moves[p.name] = choice

            if not self.running:
                break

            # 判定勝負
            p1, p2 = self.players
            c1 = moves[p1.name]
            c2 = moves[p2.name]
            winner = self.judge_round(c1, c2)

            if winner == 1:
                p1.score += 1
                round_winner = p1.name
            elif winner == 2:
                p2.score += 1
                round_winner = p2.name
            else:
                round_winner = None

            # 廣播回合結果
            for p in self.players:
                send_msg(p.conn, {
                    "type": "ROUND_RESULT",
                    "round": round_no,
                    "p1": {"name": p1.name, "choice": c1},
                    "p2": {"name": p2.name, "choice": c2},
                    "winner": round_winner,
                    "score": {p1.name: p1.score, p2.name: p2.score}
                })

            # 檢查是否有人達成 WIN_ROUNDS
            if p1.score >= WIN_ROUNDS or p2.score >= WIN_ROUNDS:
                break
            
            round_no += 1

        self.game_over()

    def recv_move(self, player, round_no):
        """從某玩家讀取一個合法的 MOVE。"""
        try:
            while True:
                msg = recv_msg(player.conn)
                if not msg:
                    return None
                if msg.get("type") != "MOVE":
                    # 亂傳別的就丟掉，繼續等 MOVE
                    continue
                choice = msg.get("choice", "").lower()
                if choice in CHOICES:
                    return choice
                else:
                    # 非法輸入，請他重來
                    send_msg(player.conn, {
                        "type": "INVALID_MOVE",
                        "valid": CHOICES
                    })
        except Exception as e:
            print(f"[RPS] recv move error from {player.name}: {e}")
            return None

    @staticmethod
    def judge_round(c1, c2):
        """回傳 0: 平手, 1: P1 贏, 2: P2 贏"""
        if c1 == c2:
            return 0
        if ((c1 == "rock" and c2 == "scissors") or
            (c1 == "scissors" and c2 == "paper") or
            (c1 == "paper" and c2 == "rock")):
            return 1
        return 2

    def game_over(self):
        end_time = time.time()
        duration = round(end_time - self.start_time, 2)
        results = {p.name: p.score for p in self.players}
        scores = list(results.values())

        if len(set(scores)) == 1:
            winner_name = None
        else:
            winner_name = max(results, key=results.get)

        # 通知兩位玩家
        msg = {
            "type": "GAME_OVER",
            "winner": winner_name or "平手",
            "results": results,
            "duration": duration
        }
        for p in self.players:
            try:
                send_msg(p.conn, msg)
            except Exception as e:
                print(f"[RPS] send GAME_OVER to {p.name} failed: {e}")

        # 回報給 lobby_server（格式跟 Tetris 的 game_server 一樣）
        try:
            lobby_sock = socket.create_connection(("127.0.0.1", LOBBY_PORT))
            send_msg(lobby_sock, {
                "action": "GAME_OVER",
                "data": {
                    "room_id": self.room_id,
                    "result": results,
                    "startAt": self.start_time,
                    "endAt": end_time
                }
            })
            lobby_sock.close()
        except Exception as e:
            print(f"[RPS] Failed to report to lobby: {e}")

        print(f"[RPS] Game over. Results: {results}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 game_server.py <port> <room_id>")
        sys.exit(1)
    port = int(sys.argv[1])
    room_id = int(sys.argv[2])
    server = RPSServer(port, room_id)
    server.start()
