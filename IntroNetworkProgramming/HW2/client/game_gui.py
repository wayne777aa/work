import pygame
import sys
import threading
import socket
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common import send_msg, recv_msg

CELL = 30
COLS, ROWS = 10, 20
MARGIN = 20
OPP_SCALE = 0.4

class GameGUI:
    def __init__(self, host, port, username, room_id):
        self.host = host
        self.port = port
        self.username = username
        self.room_id = room_id
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.players = []
        self.my_board = [[0]*COLS for _ in range(ROWS)]
        self.opp_board = [[0]*COLS for _ in range(ROWS)]
        self.my_score = 0
        self.opp_score = 0

    def start(self):
        # --- Connect to server ---
        self.sock.connect((self.host, self.port))
        send_msg(self.sock, {"userId": self.username})

        # --- Start recv thread ---
        threading.Thread(target=self.recv_loop, daemon=True).start()

        # --- Initialize Pygame ---
        pygame.init()
        self.font = pygame.font.SysFont("Consolas", 20)
        self.bigfont = pygame.font.SysFont("Consolas", 40)
        self.window = pygame.display.set_mode(
            (COLS*CELL*2 + MARGIN*3, ROWS*CELL + MARGIN*2)
        )
        pygame.display.set_caption("Two-Player Tetris")

        clock = pygame.time.Clock()

        # --- Main loop ---
        while self.running:
            clock.tick(30)
            self.handle_events()
            self.draw_screen()

        pygame.quit()

    def recv_loop(self):
        while self.running:
            try:
                msg = recv_msg(self.sock)
                if not msg:
                    break
                self.handle_server_message(msg)
            except Exception as e:
                print(f"[GUI recv error] {e}")
                break

    def handle_server_message(self, msg):
        t = msg.get("type")
        if t == "SNAPSHOT":
            self.players = msg.get("players", [])
            # assume player[0] is me, player[1] is opponent
            for p in self.players:
                if p["name"] == self.username:
                    self.my_score = p["score"]
                    self.my_board = p["board"]
                else:
                    self.opp_score = p["score"]
                    self.opp_board = p["board"]

        elif t == "GAME_OVER":
            winner = msg.get("winner", "平手")
            results = msg.get("results", {})
            duration = msg.get("duration", 0)

            # 顯示結束文字
            print("遊戲結束！")
            print(f"勝利者：{winner}")
            print(f"遊戲時長：{duration:.2f} 秒")
            print("成績：")
            for name, score in results.items():
                print(f"  - {name}: {score}")
            self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                move = None
                if event.key == pygame.K_LEFT:
                    move = "left"
                elif event.key == pygame.K_RIGHT:
                    move = "right"
                elif event.key == pygame.K_DOWN:
                    move = "soft_drop"
                elif event.key == pygame.K_UP:
                    move = "hard_drop"
                elif event.key == pygame.K_z:
                    move = "rotate_ccw"
                elif event.key == pygame.K_x:
                    move = "rotate_cw"
                if move:
                    send_msg(self.sock, {"type": "INPUT", "action": move, "userId": self.username})

    def draw_screen(self):
        self.window.fill((30,30,30))
        # 我的區域
        self.draw_board(MARGIN, MARGIN, (200,200,255), self.my_board)
        # 對手
        self.draw_board(MARGIN*2 + COLS*CELL, MARGIN, (255,200,200), self.opp_board)
        # 分數
        mytext = self.font.render(f"{self.username}: {self.my_score}", True, (255,255,255))
        opptext = self.font.render(f"Opponent: {self.opp_score}", True, (255,255,255))
        self.window.blit(mytext, (MARGIN, MARGIN//2))
        self.window.blit(opptext, (MARGIN*2 + COLS*CELL, MARGIN//2))
        pygame.display.flip()

    def draw_board(self, x0, y0, color, board):
        # 背景
        pygame.draw.rect(self.window, (80,80,80), (x0, y0, COLS*CELL, ROWS*CELL))
        for y in range(ROWS):
            for x in range(COLS):
                val = board[y][x]
                if val == 1:
                    c = (0, 150, 255)     # 固定方塊：藍色
                elif val == 2:
                    c = (255, 200, 0)     # 掉落中方塊：黃色
                else:
                    c = (40, 40, 40)
                pygame.draw.rect(self.window, c, (x0+x*CELL, y0+y*CELL, CELL-1, CELL-1))
        pygame.draw.rect(self.window, color, (x0, y0, COLS*CELL, ROWS*CELL), 2)
