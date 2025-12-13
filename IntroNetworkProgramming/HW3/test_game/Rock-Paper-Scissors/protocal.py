import struct, json

MAX_LEN = 65536

def send_msg(sock, obj):
    data = json.dumps(obj).encode('utf-8')
    length = len(data)
    if length > MAX_LEN:
        raise ValueError("Message too large")
    sock.sendall(struct.pack('!I', length) + data) # 4 bytes 長度欄位 + 訊息本體

def recvall(sock, n):
    buf = b''
    while len(buf) < n:
        part = sock.recv(n - len(buf))
        if not part:
            return None
        buf += part
    return buf

def recv_msg(sock):
    # 先讀 4 bytes 長度欄位
    raw_len = recvall(sock, 4)
    if not raw_len:
        return None
    msg_len = struct.unpack('!I', raw_len)[0]
    if msg_len <= 0 or msg_len > MAX_LEN:
        raise ValueError("Invalid length")
    # 再讀完整訊息本體
    data = recvall(sock, msg_len)
    return json.loads(data.decode('utf-8'))