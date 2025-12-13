import socket
import os
import json
import zipfile
from io import BytesIO
from protocal import send_msg, recv_msg

DEV_HOST = "127.0.0.1"
# DEV_HOST = "140.113.17.12"  # change for remote
DEV_PORT = 10070

# 所有開發者的遊戲都放這裡：developing/<developer_name>/<game_name>/
DEVELOP_ROOT = "developing"

class DeveloperClient:
    def __init__(self, host=DEV_HOST, port=DEV_PORT):
        self.sock = socket.create_connection((host, port))
        self.name = None   # 開發者名稱（登入後才有）
        self.base_dir = None 

    # ============================================================
    # 基本工具：發一個 JSON，等一個 JSON 回應
    # ============================================================
    def send_and_wait(self, obj: dict) -> dict:
        try:
            send_msg(self.sock, obj)
            res = recv_msg(self.sock)
            if not res:
                return {"action": "error", "data": {"msg": "disconnected"}}
            return res
        except Exception as e:
            return {"action": "error", "data": {"msg": str(e)}}

    # ============================================================
    # Auth API：register / login / logout
    # ============================================================
    def register(self, name: str, password: str):
        return self.send_and_wait({
            "action": "register",
            "data": {
                "name": name,
                "passwordHash": password
            }
        })

    def login(self, name: str, password: str):
        res = self.send_and_wait({
            "action": "login",
            "data": {
                "name": name,
                "passwordHash": password
            }
        })
        if res.get("action") == "login_success":
            self.name = name
            # login 成功就建 base dir: developing/<developer_name>/
            self.base_dir = os.path.join(DEVELOP_ROOT, self.name)
            os.makedirs(self.base_dir, exist_ok=True)
            print(f"[Info] 開發者根目錄: {self.base_dir}")
        return res

    def logout(self):
        return self.send_and_wait({"action": "logout"})

    # ============================================================
    # ZIP 工具：把整個資料夾打包成 zip（存在記憶體）
    # ============================================================
    def _zip_dir(self, dir_path: str) -> bytes:
        """
        把 dir_path 下面的所有檔案壓成 zip，回傳 bytes。
        zip 裡的路徑使用「相對 dir_path」。
        """
        buf = BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(dir_path):
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, dir_path)
                    z.write(full, arcname=rel)
        return buf.getvalue()

    def _load_config(self, game_dir: str):
        """
        從 game_dir/config.json 讀出 version / description。
        回傳 (version, description)；缺 version 則回傳 (None, None)。
        """
        cfg_path = os.path.join(game_dir, "config.json")
        if not os.path.exists(cfg_path):
            print(f"[Error] config.json not found in {game_dir}")
            return None, None

        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception as e:
            print(f"[Error] Failed to parse config.json: {e}")
            return None, None

        version = cfg.get("version")
        description = cfg.get("description", "")

        if not version:
            print("[Error] config.json 必須包含 'version' 欄位")
            return None, None

        return version, description

    # ============================================================
    # 上傳新遊戲（第一次上架）
    # ============================================================
    def upload_new_game(self, game_name: str):
        """
        對應 developer_server 的 handle_dev_upload_new():
        action = "dev_upload"
        data: {
            "game_name": str,
            "version": str,
            "description": str,
            "size": int
        }
        之後 server 會回 dev_upload_ready，client 再傳 zip binary。
        """
        if not self.base_dir:
            print("[Error] 尚未登入")
            return

        game_dir = os.path.join(self.base_dir, game_name)
        if not os.path.isdir(game_dir):
            print(f"[Error] 資料夾不存在: {game_dir}")
            return

        version, description = self._load_config(game_dir)
        if not version:
            return

        # 打包 zip
        binary = self._zip_dir(game_dir)
        size = len(binary)

        print(f"[Info] 準備上傳新遊戲：{game_name} v{version} ({size} bytes)")

        # 1) 先送 JSON header
        header = {
            "action": "dev_upload",
            "data": {
                "game_name": game_name,
                "version": version,
                "description": description,
                "size": size
            }
        }
        send_msg(self.sock, header)
        res = recv_msg(self.sock)
        print("[Header response]", res)

        if not res or res.get("action") != "dev_upload_ready":
            print("[Error] server 不接受上傳 (dev_upload_ready 失敗)")
            return

        # 2) 傳 zip binary
        try:
            self.sock.sendall(binary)
        except Exception as e:
            print("[Error] 傳送 zip 失敗:", e)
            return

        # 3) 等最後結果
        res = recv_msg(self.sock)
        print("[Final response]", res)

    # ============================================================
    # 既有遊戲新增版本
    # ============================================================
    def upload_new_version(self, game_name: str):
        """
        對應 developer_server 的 handle_dev_upload_version():
        action = "dev_upload_version"
        """
        if not self.base_dir:
            print("[Error] 尚未登入")
            return

        game_dir = os.path.join(self.base_dir, game_name)
        if not os.path.isdir(game_dir):
            print(f"[Error] 找不到遊戲資料夾: {game_dir}")
            return

        version, description = self._load_config(game_dir)
        if not version:
            return

        binary = self._zip_dir(game_dir)
        size = len(binary)

        print(f"[Info] 準備上傳新版本：{game_name} v{version} ({size} bytes)")

        # 1) 先送 JSON header
        header = {
            "action": "dev_upload_version",
            "data": {
                "game_name": game_name,
                "version": version,
                "description": description,
                "size": size
            }
        }
        send_msg(self.sock, header)
        res = recv_msg(self.sock)
        print("[Header resp]", res)

        if not res or res.get("action") != "dev_upload_ready":
            print("[Error] server 不接受上傳 (dev_upload_ready 失敗)")
            return

        # 2) 傳 zip binary
        try:
            self.sock.sendall(binary)
        except Exception as e:
            print("[Error] 傳送 zip 失敗:", e)
            return

        # 3) 等最後結果
        res = recv_msg(self.sock)
        print("[Final resp]", res)

    # ============================================================
    # 下/上架遊戲
    # ============================================================
    def offline_game(self, game_name: str):
        if not self.base_dir:
            print("[Error] 尚未登入")
            return

        res = self.send_and_wait({
            "action": "dev_offline",
            "data": {"game_name": game_name}
        })
        print(res)
    
    def online_game(self, game_name: str):
        if not self.base_dir:
            print("[Error] 尚未登入")
            return
        
        res = self.send_and_wait({
            "action": "dev_online",
            "data": {"game_name": game_name}
        })
        print(res)

    # ============================================================
    # 關閉連線
    # ============================================================
    def close(self):
        try:
            self.sock.close()
        except:
            pass


# ============================================================
# Developer Menu
# ============================================================
def main():
    print("=== Developer Client ===")

    client = DeveloperClient(DEV_HOST, DEV_PORT)

    try:
        # -------------------------------
        # Login / Register
        # -------------------------------
        while True:
            print("\n1) Login")
            print("2) Register")
            op = input("> ").strip()

            if op == "2":
                name = input("Developer name: ").strip()
                pw = input("Password: ").strip()

                if not name or not pw:
                    print("[Error] 不可為空")
                    continue

                res = client.register(name, pw)
                print(res)
                continue

            if op == "1":
                name = input("Developer name: ").strip()
                pw = input("Password: ").strip()

                if not name or not pw:
                    print("[Error] 不可為空")
                    continue
                res = client.login(name, pw)
                print(res)
                if res.get("action") == "login_success":
                    break
                continue

            print("[Error] 無效選項")

        print(f"\n登入成功，開發者：{client.name}")
        print(f"遊戲請放在：{client.base_dir}/<game_name>/")

        # -------------------------------
        # 主選單：上傳 / 更新
        # -------------------------------
        while True:
            print("\n=== Developer Menu ===")
            print("1. 上傳新遊戲 (第一次上架)")
            print("2. 上傳新版本 (既有遊戲)")
            print("3. 下架遊戲")
            print("4. 上架遊戲")
            print("0. 登出並離開")
            op = input("> ").strip()

            if op == "0":
                res = client.logout()
                print(res)
                break

            game_name = input("遊戲名稱 (資料夾名稱): ").strip()
            if not game_name:
                print("[Error] 遊戲名稱不可為空")
                continue

            if op == "1":
                client.upload_new_game(game_name)
            elif op == "2":
                client.upload_new_version(game_name)
            elif op == "3":
                client.offline_game(game_name)
            elif op == "4":
                client.online_game(game_name)
            else:
                print("[Error] 無效選項")

    finally:
        client.close()


if __name__ == "__main__":
    main()