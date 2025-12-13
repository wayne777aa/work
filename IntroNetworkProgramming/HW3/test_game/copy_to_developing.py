#!/usr/bin/env python3
import os
import sys
import shutil

def main():
    if len(sys.argv) != 3:
        print("用法: python copy_to_developing.py <developer_name> <game_name>")
        sys.exit(1)

    developer_name = sys.argv[1]
    game_name = sys.argv[2]

    # 当前腳本所在的 test_game/ 資料夾
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 來源：test_game/<game_name>/
    src_dir = os.path.join(script_dir, game_name)

    # 目標：developer/developing/<developer_name>/<game_name>/
    # repo_root = 上一層
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    dst_base = os.path.join(repo_root, "developer", "developing", developer_name)
    dst_dir = os.path.join(dst_base, game_name)

    # 檢查來源是否存在
    if not os.path.isdir(src_dir):
        print(f"[錯誤] 找不到來源資料夾: {src_dir}")
        sys.exit(1)

    # 建立目標 developer/developing/<developer_name>/ 如果沒有的話
    os.makedirs(dst_base, exist_ok=True)

    # 如果目標已經有同名遊戲，避免直接覆蓋
    if os.path.exists(dst_dir):
        print(f"[錯誤] 目標已經存在: {dst_dir}")
        print("請先刪除或移走原本的遊戲資料夾，再重新執行。")
        sys.exit(1)

    print(f"複製遊戲資料夾：")
    print(f"  從 {src_dir}")
    print(f"  到 {dst_dir}")

    shutil.copytree(src_dir, dst_dir)

    print("[完成] 複製成功。")

if __name__ == "__main__":
    main()
