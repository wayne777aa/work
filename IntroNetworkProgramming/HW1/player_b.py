import socket
import json

BUFFER_SIZE = 1024
UDP_PORT_RANGE = range(18000, 18011)

def run(username):
    print(f"[INFO] Hello {username}, you are Player B (waiting for invitations)")

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_port = None

    for port in UDP_PORT_RANGE:
        try:
            udp_sock.bind(('', port))
            udp_port = port
            break
        except OSError:
            continue
    
    if udp_port is None:
        print(f"[ERROR] No available port in range {UDP_PORT_RANGE.start}–{UDP_PORT_RANGE.stop - 1}.")
        return
    
    print(f"[INFO] Listening for invitations on UDP port {udp_port}...")

    while True:
        try:
            data, addr = udp_sock.recvfrom(BUFFER_SIZE) # 卡住 直到收到udp封包
            # print(f"[DEBUG] Received UDP from {addr}: {data}")
            msg = json.loads(data.decode())

            if msg.get("action") == "scan":
                udp_sock.sendto(b"WAITING", addr)   # 告訴 A：我在線上
                continue

            if msg.get("action") == "invite":
                from_user = msg.get("from")
                print(f"\n[INVITE] Received invitation from {from_user} at {addr[0]}")

                decision = input("Do you want to accept the invitation? (y/n): ").strip().lower()
                if decision != "y":
                    # 回傳拒絕
                    reject_msg = json.dumps({"status": "REJECT"}).encode()
                    udp_sock.sendto(reject_msg, addr)
                    print("[INFO] Rejected invitation.")
                    continue

                # 回傳接受
                accept_msg = json.dumps({"status": "ACCEPT", "username": username}).encode()
                udp_sock.sendto(accept_msg, addr)
                print("[INFO] Accepted invitation. Waiting for TCP connection info...")

                # 等待對方送來 TCP 連線資訊
                tcp_data, tcp_addr = udp_sock.recvfrom(BUFFER_SIZE)
                tcp_info = json.loads(tcp_data.decode())

                target_ip = tcp_info.get("ip")
                target_port = tcp_info.get("port")
                print(f"[INFO] Connecting to TCP game server at {target_ip}:{target_port}...")

                # 建立 TCP 連線
                tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_sock.connect((target_ip, target_port))
                print("[SUCCESS] Connected to Player A. Game start!")
                try:
                    msg = json.loads(tcp_sock.recv(1024).decode())
                    if msg["action"] == "greet":
                        print(f"[SYSTEM] {msg['msg']}")
                except json.JSONDecodeError:
                    pass

                # 呼叫 game_loop，B 是後手 (is_first=False)
                from game_engine import game_loop
                game_loop(tcp_sock, username, is_first=False)

                tcp_sock.close()
                udp_sock.close()
                break  # 遊戲結束後離開迴圈

        except KeyboardInterrupt:
            print("\n[EXIT] Player B manually exited.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            continue

    udp_sock.close()