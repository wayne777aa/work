import socket
import json
import time

LOBBY_HOST = '127.0.0.1'  # TODO: change the Lobby IP
LOBBY_PORT = 12000

def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

def print_board(board):
    print("   0   1   2")
    for i, row in enumerate(board):
        row_str = f"{i}  " + " | ".join(row)
        print(row_str)
        if i < 2:
            print("  ---+---+---")
    print()

def make_move(board, row, col, player_symbol):
    if board[row][col] == ' ':
        board[row][col] = player_symbol
        return True
    else:
        print("[WARN] That spot is already taken.")
        return False

def check_winner(board, player_symbol):
    for i in range(3):
        if all(board[i][j] == player_symbol for j in range(3)) or \
           all(board[j][i] == player_symbol for j in range(3)):
            return True
    if all(board[i][i] == player_symbol for i in range(3)) or \
       all(board[i][2-i] == player_symbol for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def update_stats(updates):
    
    assert isinstance(updates, list), 'updates: list of {"username": str, "stats": {"win": ?, "draw": ?, "lose": ?}}'

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((LOBBY_HOST, LOBBY_PORT))
            req = {
                "action": "update_stats",
                "updates": updates
            }
            s.sendall(json.dumps(req).encode())
            resp = s.recv(1024).decode()
            try:
                result = json.loads(resp)
                if result.get("status") == "UPDATE_SUCCESS":
                    print("[DEBUG] Stats updated successfully.")
                else:
                    print(f"[WARN] Failed to update stats: {result}")
            except json.JSONDecodeError:
                print("[ERROR] Invalid JSON response from server.")
    except Exception as e:
        print(f"[ERROR] Failed to update stats: {e}")


def game_loop(sock, username, is_first):
    sock.sendall(username.encode())
    opponent_username = sock.recv(1024).decode()
    board = create_board()
    my_symbol = 'X' if is_first else 'O'
    opp_symbol = 'O' if is_first else 'X'
    is_my_turn = is_first
    try:
        while True:
            print_board(board)
            if is_my_turn:
                print(f"[TURN] Your move ({my_symbol})")
                try:
                    row = int(input("Enter row(─) (0-2): "))
                    col = int(input("Enter col(|) (0-2): "))
                    if row not in range(3) or col not in range(3):
                        print("[WARN] Invalid position. Try again.")
                        continue
                except ValueError:
                    print("[WARN] Invalid input. Try again.")
                    continue

                if make_move(board, row, col, my_symbol):
                    msg = json.dumps({"action": "move", "row": row, "col": col})
                    sock.sendall(msg.encode())

                    if check_winner(board, my_symbol):
                        print_board(board)
                        print("[WIN] You win!")
                        update_stats([
                            {"username": username, "stats": {"win": 1, "draw": 0, "lose": 0}},
                            {"username": opponent_username, "stats": {"win": 0, "draw": 0, "lose": 1}}
                        ])
                        time.sleep(0.1)
                        return
                    elif is_draw(board):
                        print_board(board)
                        print("[DRAW] The game is a draw.")
                        update_stats([
                            {"username": username, "stats": {"win": 0, "draw": 1, "lose": 0}},
                            {"username": opponent_username, "stats": {"win": 0, "draw": 1, "lose": 0}}
                        ])
                        time.sleep(0.1)
                        return
                    
                    is_my_turn = False

            else:
                print("[WAIT] Waiting for opponent's move...")
                try:
                    data = sock.recv(1024).decode()
                    if not data:
                        print("[DISCONNECT] Opponent disconnected.") # 對方離開算贏
                        print("[WIN] You win!")
                        update_stats([
                            {"username": username, "stats": {"win": 1, "draw": 0, "lose": 0}},
                            {"username": opponent_username, "stats": {"win": 0, "draw": 0, "lose": 1}}
                        ])
                        time.sleep(0.1)
                        return
                    
                    msg = json.loads(data)
                    if msg["action"] == "move":
                        row = msg["row"]
                        col = msg["col"]
                        make_move(board, row, col, opp_symbol)

                        if check_winner(board, opp_symbol):
                            print_board(board)
                            print("[LOSE] You lost.")
                            time.sleep(0.1)
                            return
                        
                        elif is_draw(board):
                            print_board(board)
                            print("[DRAW] The game is a draw.")
                            time.sleep(0.1)
                            return
                        
                        is_my_turn = True

                    else:
                        print(f"[WARN] Unknown action: {msg}")
                        continue

                except json.JSONDecodeError:
                    print("[ERROR] Malformed JSON from opponent. Ignored.")
                    continue
                except Exception as e:
                    print(f"[ERROR] Unexpected error: {e}")
                    return
    except KeyboardInterrupt:
                    print("\n[EXIT] hey, you are loser")
                    return
            
