import socket
import sys
import time

from protocal import send_msg, recv_msg

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 game_client.py <host> <port> <username> <room_id>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    username = sys.argv[3]
    room_id = int(sys.argv[4])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting to", host, port)

    for i in range(10):
        try:
            sock.connect((host, port))
            break
        except ConnectionRefusedError:
            # game_server 可能還沒 bind，等一下再試
            time.sleep(0.2)
    else:
        print("連線失敗：多次嘗試仍被拒絕。")
        return

    # 跟 server 打招呼
    send_msg(sock, {"userId": username})

    print(f"== Rock-Paper-Scissors (room {room_id}) ==")
    print("指令：rock / paper / scissors（可簡寫 r / p / s）")

    try:
        while True:
            msg = recv_msg(sock)
            if not msg:
                print("[Client] disconnected from server.")
                break

            t = msg.get("type")

            if t == "WELCOME":
                print(msg.get("msg", ""))

            elif t == "GAME_START":
                print(msg.get("msg", ""))

            elif t == "ROUND_START":
                rnd = msg.get("round")
                print(f"\n--- Round {rnd} ---")

            elif t == "ASK_MOVE":
                # 要求玩家出拳
                choice = ask_choice(msg.get("valid", []))
                send_msg(sock, {
                    "type": "MOVE",
                    "choice": choice
                })

            elif t == "INVALID_MOVE":
                print("輸入不合法，請重新輸入。允許：", msg.get("valid"))

            elif t == "ROUND_RESULT":
                rnd = msg.get("round")
                p1 = msg.get("p1", {})
                p2 = msg.get("p2", {})
                winner = msg.get("winner")
                score = msg.get("score", {})

                print(f"\nRound {rnd} 結果：")
                print(f"  {p1.get('name')}: {p1.get('choice')}")
                print(f"  {p2.get('name')}: {p2.get('choice')}")
                if winner:
                    print(f"  => 本回合勝者：{winner}")
                else:
                    print("  => 平手")
                print("  累計分數：")
                for name, sc in score.items():
                    print(f"    - {name}: {sc}")

            elif t == "GAME_OVER":
                print("\n=== 遊戲結束 ===")
                print("最終結果：")
                results = msg.get("results", {})
                for name, sc in results.items():
                    print(f"  - {name}: {sc}")
                print("勝利者：", msg.get("winner"))
                print(f"遊戲時長：{msg.get('duration', 0)} 秒")
                break

            else:
                # 未知訊息，就印出 debug
                print("[Client] recv:", msg)

    except KeyboardInterrupt:
        print("\n[Client] aborted by user.")
    except Exception as e:
        print(f"[Client] error: {e}")
    finally:
        sock.close()


def ask_choice(valid):
    valid_set = set(valid) if valid else {"rock", "paper", "scissors"}
    while True:
        s = input("請出拳 (rock/r, paper/p, scissors/s): ").strip().lower()
        if s in ("r", "rock"):
            c = "rock"
        elif s in ("p", "paper"):
            c = "paper"
        elif s in ("s", "scissors"):
            c = "scissors"
        else:
            print("輸入錯誤，請重新輸入。")
            continue
        if c in valid_set:
            return c
        else:
            print("目前不接受這個選項，請再試一次。")


if __name__ == "__main__":
    main()
