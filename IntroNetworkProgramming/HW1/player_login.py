import socket
import json

LOBBY_HOST = '127.0.0.1'  # TODO: change the Lobby IP
LOBBY_PORT = 12000

def send_request(action, username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((LOBBY_HOST, LOBBY_PORT))

        request = {
            "action": action,
            "username": username,
            "password": password
        }

        s.sendall(json.dumps(request).encode())
        response = s.recv(1024).decode()

        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {"status": "ERROR", "reason": "Invalid response"}
        
def logout(username):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((LOBBY_HOST, LOBBY_PORT))
        request = {
            "action": "logout",
            "username": username,
            "password": ""  # 不需要密碼
        }
        s.sendall(json.dumps(request).encode())
        response = s.recv(1024).decode()
        try:
            result = json.loads(response)
            if result.get("status") == "LOGOUT_SUCCESS":
                print("[SUCCESS] Logout successful. See you next time!")
            else:
                print(f"[WARN] Logout failed: {result}")
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid logout response: {response}")
        
def enter_game_mode(username):
    print(f"\n[WELCOME] Hello {username}, please select your role:")
    print("1. Player A (Invite other players)")
    print("2. Player B (Wait for invitations)")
    print("3. Logout")
    choice = input("Enter 1 , 2 or 3: ").strip()

    if choice == "1":
        import player_a
        player_a.run(username)
        return True
    elif choice == "2":
        import player_b
        player_b.run(username)
        return True
    elif choice == "3":
        return False
    else:
        print("[ERROR] Invalid choice. Try again.")
        return True

def handle_login_or_register():
    while True:
        action = input("Do you want to login or register? (login/register): ").strip().lower()
        if action in ["login", "register"]:
            break
        print("Invalid action. try again")

    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        result = send_request(action, username, password)

        if result["status"] == "LOGIN_SUCCESS":
            print("[SUCCESS] Login successful.")
            win = result.get("win", 0)
            draw = result.get("draw", 0)
            lose = result.get("lose", 0)
            print(f"[STATS] Wins: {win}, Draws: {draw}, Losses: {lose}")
            return username
        elif result["status"] == "REGISTER_SUCCESS":
            print("[SUCCESS] Registration successful. Please login again.")
            return None
        else:
            print(f"[FAIL] {result['status']} - {result.get('reason', 'Unknown reason')}. try again")
            continue


def main():
    print("Welcome to the Game Lobby!")

    while True:
        username = handle_login_or_register()
        if not username:
            continue

        try:
            while True:
                keep_playing = enter_game_mode(username)
                if not keep_playing:
                    break
        except KeyboardInterrupt:
            print("\n[EXIT] Manually interrupted.")
        finally:
            logout(username)
            break

if __name__ == "__main__":
    main()
