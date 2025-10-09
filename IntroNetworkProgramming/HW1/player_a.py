import socket
import json
import threading

UDP_PORT_RANGE = range(17999, 18011)  # 可以掃描的 port 範圍
SERVER_LIST = [
    "127.0.0.1",
    "140.113.235.151",  # linux1.cs.nycu.edu.tw
    "140.113.235.152",  # linux2.cs.nycu.edu.tw
    "140.113.235.153",  # linux3.cs.nycu.edu.tw
    "140.113.235.154"   # linux4.cs.nycu.edu.tw
]

BUFFER_SIZE = 1024

def run(username):
    print(f"[INFO] Player A ({username}) is scanning for available Player B...")

    found_targets = []

    # 掃描所有 server + port，看哪裡有 player B
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.settimeout(0.3)  # 每個封包等待 0.3s

    scan_msg = json.dumps({"action": "scan"}).encode()

    for host in SERVER_LIST:
        for port in UDP_PORT_RANGE:
            # print(f"[DEBUG] Sending scan to {host}:{port}")
            try:
                udp_sock.sendto(scan_msg, (host, port))
                data, addr = udp_sock.recvfrom(BUFFER_SIZE)
                if b"WAITING" in data:
                    print(f"[FOUND] Player B at {host}:{port}")
                    found_targets.append((host, port))
            except socket.timeout:
                continue

    if not found_targets:
        print("[INFO] No available Player B found.")
        return

    #  選一個目標來傳送邀請
    print("\nAvailable Players:")
    for i, (ip, port) in enumerate(found_targets):
        print(f"{i+1}. {ip}:{port}")
    
    try:
        idx = int(input("Select a player to invite (1~N): ")) - 1
        target_ip, target_port = found_targets[idx]
    except (ValueError, IndexError):
        print("[ERROR] Invalid selection.")
        return

    invite_msg = json.dumps({
        "action": "invite",
        "from": username
    }).encode()
    udp_sock.sendto(invite_msg, (target_ip, target_port))
    print(f"[INFO] Sent invitation to {target_ip}:{target_port}, waiting for response...")

    udp_sock.settimeout(10.0)

    try:
        data, addr = udp_sock.recvfrom(BUFFER_SIZE)
        reply = json.loads(data.decode())
        if reply.get("status") != "ACCEPT":
            print("[INFO] Invitation was rejected.")
            return
    except socket.timeout:
        print("[ERROR] No response from player.")
        return

    print("[SUCCESS] Invitation accepted.")

    # 啟動 TCP server 等待對方連進來
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind(('', 0))  # 自動分配一個空的 port
    tcp_sock.listen(1)
    tcp_ip = socket.gethostbyname(socket.gethostname())
    tcp_port = tcp_sock.getsockname()[1]
    print(f"[INFO] TCP server listening on {tcp_ip}:{tcp_port}")

    # 傳送 TCP server 資訊給 Player B
    tcp_info = {
        "ip": tcp_ip,
        "port": tcp_port
    }
    udp_sock.sendto(json.dumps(tcp_info).encode(), (target_ip, target_port))
    print(f"[INFO] Sent TCP info to {target_ip}:{target_port}, waiting for connection...")

    # 等待對方連進來
    conn, addr = tcp_sock.accept()
    print(f"[SUCCESS] Player B connected from {addr[0]}:{addr[1]}")
    conn.sendall(json.dumps({"action": "greet", "msg": "Welcome to Tic-Tac-Toe game!"}).encode())

    # 呼叫 game_loop，A 是先手 (is_first=True)
    from game_engine import game_loop
    game_loop(conn, username, is_first=True)

    conn.close()
    tcp_sock.close()
    udp_sock.close()