from lobby_client import LobbyClient
from game_gui import GameGUI
import time
import ast

LOBBY_HOST = "127.0.0.1" # change for local
# LOBBY_HOST = "140.113.17.12"  # change for remote
LOBBY_PORT = 10090

def connect_to_game(host, port, user, room_id, retry=3):
    time.sleep(1)  # 等待 Game Server 啟動
    for attempt in range(retry):
        try:
            game = GameGUI(host, port, user, room_id)
            game.start()
            return
        
        except ConnectionRefusedError:
            print(f"[GameClient] Connection refused. Retrying in 1s...")
            time.sleep(1)
        except Exception as e:
            print(f"[GameClient] Failed to connect: {e}")
            break
    print("[GameClient] All connection attempts failed.")

def main():
    # === 連線 Lobby ===
    lobby = LobbyClient(LOBBY_HOST, LOBBY_PORT)


    # === 遊戲開始 callback ===
    def on_start(msg):
        connect_to_game(msg["host"], msg["port"], name, msg["room_id"])
    lobby.on_game_start = on_start

    # === 登入 / 註冊 ===
    while True:
        choice = input("Login [L] or Register [R]? ").strip().lower()
        name = input("Username: ")
        pw = input("Password: ")

        if choice == "r":
            email = input("Email: ")
            res = lobby.register(name, email, pw)
            if res.get("ok"):
                print(f"✅ 註冊成功：{res.get('msg', '')}")
            else:
                print(f"❌ 註冊失敗：{res.get('msg', '')}")
                continue

        res = lobby.login(name, pw)
        if res.get("ok"):
            print(f"✅ 登入成功：{res.get('msg', '')}")
            break
        else:
            print(f"❌ 登入失敗：{res.get('msg', '')}")
            print("請再試一次。")

    # === 房間操作 ===
    while True:
        print("== Room Menu ==")
        print("1. list user")
        print("2. List rooms")
        print("3. Create room")
        print("4. Join room")
        print("5. invite user")
        print("6. accept invite")
        print("7. Game start (host only)")
        print("8. Leave room")
        print("9. Show GameLog")
        print("10. Exit")
        choice = input("> ").strip()

        if choice == "1":
            res = lobby.list_users()
            if res.get("ok"):
                users = res.get("users", [])
                if not users:
                    print("目前沒有上線使用者。")
                else:
                    print("=== Online Users ===")
                    for u in users:
                        name = u.get("name", "N/A")
                        status = u.get("status", "N/A")
                        room = u.get("room", None)
                        room_str = str(room) if room else "無"
                        print(f"使用者：{name}")
                        print(f"狀態　：{status}")
                        print(f"房間　：{room_str}")
                        print("------------------------")
                time.sleep(1.5)
            else:
                print("Failed to get users:", res.get("msg"))

        elif choice == "2":
            res = lobby.list_rooms()
            if res.get("ok"):
                rooms = res.get("rooms", [])
                if not rooms:
                    print("目前沒有可用的房間。")
                else:
                    print("=== 房間列表 (Rooms) ===")
                    for r in rooms:
                        room_id = r.get("id", "N/A")
                        name = r.get("name", "N/A")
                        host = r.get("host", "N/A")
                        members = ", ".join(r.get("member_list", [])) or "(empty)"
                        visibility = r.get("visibility", "N/A")
                        status = r.get("status", "N/A")

                        print(f"房間ID　：{room_id}")
                        print(f"房間名稱：{name}")
                        print(f"房主　　：{host}")
                        print(f"成員　　：{members}")
                        print(f"公開狀態：{visibility}")
                        print(f"狀態　　：{status}")
                        print("-" * 40)
                time.sleep(1.5)
            else:
                print("Failed to get rooms:", res.get("msg"))
            
        elif choice == "3":
            room_name = input("Room name: ")
            vis = input("public/private: ").strip() or "public"
            res = lobby.create_room(room_name, vis)
            if res.get("ok"):
                room_id = res.get("room_id", "N/A")
                print("✅ 房間建立成功！")
                print(f"房間 ID ：{room_id}")
                print(f"房間名稱：{room_name}")
                print(f"公開狀態：{vis}")
                print(f"房主　　：{name}")
                print(f"狀態　　：idle")
                print("-" * 40)
            else:
                print("❌ 房間建立失敗:", res.get("msg", "Unknown error"))
            time.sleep(1.5)

        elif choice == "4":
            try:
                room_id = int(input("Room ID to join: "))
            except ValueError:
                print("❌ 請輸入正確的房間編號！")
                continue
            res = lobby.join_room(room_id)
            if res.get("ok"):
                print("✅ 已成功加入房間！")
                print(f"房間 ID ：{room_id}")
                print(f"加入者　：{name}")
                print(f"狀態　　：in_room")
                print("-" * 40)
            else:
                print("❌ 加入房間失敗:", res.get("msg", "Unknown error"))
            time.sleep(1.5)

        elif choice == "5":
            invitee = input("Username to invite: ")
            res = lobby.invite_user(invitee)
            if res.get("ok"):
                msg = res.get("msg", "")
                # 嘗試從訊息中提取房號，例如 "q invited to room 7"
                import re
                match = re.search(r"room (\d+)", msg)
                room_id = match.group(1) if match else "N/A"

                print("✅ 已送出邀請！")
                print(f"邀請對象：{invitee}")
                print(f"房間 ID　：{room_id}")
                print("-" * 40)
            else:
                print("❌ 邀請失敗:", res.get("msg", "Unknown error"))
            time.sleep(1.5)

        elif choice == "6":
            list_res = lobby.list_invites()
            if list_res.get("ok"):
                invites = list_res.get("invites", [])
                if not invites:
                    print("目前沒有邀請。")
                else:
                    print("邀請列表：")
                    for inv in invites:
                        print(f"來自：{inv['from']} | 房名：{inv['name']} | 房間 ID：{inv['room_id']}")
                    print("-" * 40)

                    rid = input("請輸入要接受的房間 ID：").strip()
                    res = lobby.accept_invite(rid)
                    if res.get("ok"):
                        print("成功加入房間！")
                        print(f"邀請者　：{inv['from']}")
                        print(f"房間 ID ：{rid}")
                        print(f"房間狀態：等待開始")
                        print("-" * 40)
                    else:
                        print(f"❌ 加入失敗：{res.get('msg', 'Unknown error')}")
            else:
                print("❌ 取得邀請清單失敗。")
            
            time.sleep(1.5)

        elif choice == "7":
            if input("是否開始遊戲? [Y/N] ").strip().lower() == "y":
                lobby.start_game()

        elif choice == "8":
            res = lobby.leave_room()
            if res.get("ok"):
                print(f"✅ 離開房間成功：{res.get('msg', '')}")
            else:
                print(f"❌ 離開房間失敗：{res.get('msg', '')}")
            print("-" * 40)
            time.sleep(1.5)

        elif choice == "9":
            res = lobby.list_gamelog()
            if res.get("ok"):
                print("=== Game Logs ===")
                for i, log in enumerate(res["logs"], start=1):
                    users_raw = log.get("users", [])
                    if isinstance(users_raw, str):
                        try:
                            users_list = ast.literal_eval(users_raw)
                        except Exception:
                            users_list = [users_raw]
                    else:
                        users_list = users_raw

                    users = ", ".join(users_list)

                    result_raw = log.get("result", {})
                    if isinstance(result_raw, str):
                        try:
                            result = ast.literal_eval(result_raw)
                        except Exception:
                            result = {"raw": result_raw}
                    else:
                        result = result_raw

                    result_str = " | ".join(f"{u}: {s}" for u, s in result.items())
                    start_time = log.get("startAt", "N/A")
                    end_time = log.get("endAt", "N/A")

                    print(f"[{i}] 玩家: {users}")
                    print(f"     分數: {result_str}")
                    print(f"     開始時間: {start_time}")
                    print(f"     結束時間: {end_time}")
                    print("-" * 40)
            else:
                print("Failed to get logs:", res.get("msg"))

            time.sleep(1.5)

        elif choice == "10":
            print("Exiting.")
            lobby.exit()
            return

if __name__ == "__main__":
    main()
