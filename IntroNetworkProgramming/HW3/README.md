# Network Programming Final - 遊戲商城系統

## 1. 專案簡介

這個專案實作一個「遊戲商城 + 大廳」系統，整合：

- **開發者平台**：開發者可以上傳 / 更新 / 上下架自己的遊戲。
- **玩家大廳與商城**：玩家可以註冊登入、瀏覽遊戲列表與詳細資訊、下載最新版本、建立房間與其他玩家一起玩。
- **遊戲示範**：提供一款雙人對戰的 **Tetris GUI 遊戲**，透過 game_server 同步雙方的遊戲狀態，遊戲結束後回報 Lobby，並讓玩家當場評分。

專案同一個 repo 內同時包含 Server 端與 Client 端程式。  
Demo 時預期是：

- Server 端佈署在系計 Linux 主機上執行。
- 助教在自己電腦上 `git clone` 此 repo，依 README 啟動：
  - `developer_client.py`（開發者）
  - `player_client.py`（玩家）

---
## 2. 遊玩指南
1. 在自己電腦上 `git clone` 此 repo，依照需求啟動：
    - `developer/developer_client.py`（開發者）
    - `player/player_client.py`（玩家）
    - 可能需要修改連線設定

2. 如果要測試 `developer_client.py`，可以先執行：

    ```bash
    python3 test_game/copy_to_developing.py <developer_name> <game_name>
    ```

    - `<developer_name>`：建議填之後要用來登入 Developer Client 的帳號名稱。
    - `<game_name>`：必須是 `test_game/` 下面現有的資料夾名稱，目前提供：
        - `tetris`
        - `Rock-Paper-Scissors`

3. `developer` 和 `player` 各自有獨立帳號系統：
    - Developer Client：開發者需在 Developer Server 上註冊 / 登入。
    - Player Client：玩家需在 Lobby Server 上註冊 / 登入。
    - 註冊完登入後依照 CLI 提示即可進行上架 / 遊玩流程。

---
## 3. 系統架構與元件

### 3.1 元件列表

Server 端（系計機器）：

- `database.py`：定義 SQLite schema 與 DB 操作邏輯（User / Developer / Game / GameVersion / Review）。

- `db_server.py`：  
  - 監聽 `DB_HOST:DB_PORT`，接受 JSON request，呼叫 `database.handle_request()` 存取 SQLite 檔 `game.db`。

- `developer_server.py`：Developer Server / Store 後端。  
  - 處理開發者註冊、登入、上傳新遊戲、上傳新版本、上下架遊戲。
  - 接收 zip 檔並解壓縮到 `server_games/<game_name>/`。

- `lobby_server.py`：Lobby Server / 大廳與商城。  
  - 管理玩家帳號、房間、遊戲列表 / 詳細資訊 / 下載、遊戲啟動與 GAME_OVER 回報、評分。
  - 當房主按下「開始遊戲」時：
    - 找一個 12000–13000 的空 port。
    - 以 `subprocess` 啟動對應遊戲的 `game_server.py`。
    - 廣播 `game_start` 給房間內所有玩家。
  - 接收遊戲結束的 GAME_OVER 回報，紀錄勝負 / 遊戲紀錄。
  - 處理玩家對「剛玩完遊戲」的評分與評論。

- `server_games/<game_name>/game_server.py` + `game_logic.py`：示範遊戲 Server（雙人 Tetris）。
  - 固定 tick（0.5 秒）更新遊戲，維護每個玩家的 board / score / alive 狀態。
  - 兩位玩家都結束或時間到 → 廣播 GAME_OVER，並通知 Lobby Server。

Client 端：

- `developer/developer_client.py`：Developer Client（Menu-based CLI）。
  - 管理自己的遊戲資料夾並打包成 zip 上傳。
  - 支援「上傳新遊戲 / 上傳新版本 / 下架 / 上架」。
  - 從 `developing/<developer_name>/<game_name>/` 讀取檔案與 `config.json`，打包後送給 `developer_server.py`。

- `player/player_client.py`：Player / Lobby Client（Menu-based CLI）。
  - 玩家註冊登入 / 登出
  - 瀏覽遊戲詳細資訊（版本列表、平均評分、評論）、下載 / 更新遊戲。
  - 建立 / 加入 / 離開房間，房內選擇遊戲、開始遊戲。
  - 遊戲結束後可針對 **上一局剛玩完的遊戲** 給 1–5 分並寫評論。

- `server_games/<game_name>/game_client.py`：示範遊戲 GUI Client（Tetris，使用 pygame）。
  - 由 Player Client 在收到 `game_start` 廣播後自動 `subprocess` 啟動。

共用：

- `protocal.py`：簡單的長度前綴 JSON protocol（`send_msg` / `recv_msg`）。

---

## 4. 目錄結構

實際執行時會動態產生一些資料夾。建議的檔案與資料夾如下：

```text
.
├── protocal.py
├── developer_server.py
├── lobby_server.py
├── db_server.py
├── database.py
├── game.db                # SQLite DB 檔（初次執行時建立）
│
├── server_games/          # Server 端儲存的遊戲
│   └── <game_name>/
│       ├── game_logic.py
│       ├── game_server.py
│       ├── protocal.py
│       ├── config.json
│       └── ...
│
├── player
│   ├── protocal.py
│   ├── player_client.py
│   └── downloads/        # 玩家下載的遊戲
│       └── <username>/
│           ├── _versions.json # 記錄此玩家已下載過的 gameId → version
│           └── <game_name>/
│               ├── game_client.py
│               ├── protocal.py
│               └── ...
│
├── developer
│   ├── protocal.py
│   ├── developer_client.py
│   └── developing/        # 正在開發的遊戲
│       └── <developer_name>/
│           └── <game_name>/
│               ├── game_client.py
│               ├── game_logic.py
│               ├── game_server.py
│               ├── protocal.py
│               └── config.json # 需由developer自行填寫:"version", "description"
│
├── test_game.py # 測試用的小遊戲或測試腳本
|   ├── test_game.py
│   └── <game_name>/
│
└── README.md
```
---
## 5. 執行環境需求
### 5.1 共通（Developer / Player Client）
- 作業系統：
    - Linux
- Python：
    - Python 3.10 以上。
- Python 套件：
    - pygame >= 2.0（只有遊戲 GUI client 需要，即 game_client.py）
    - 可通過 `pip install pygame` 下載
---
## 6. 可修改連線資訊（IP / Port）
如果要改連線設定，只需要編輯以下檔案中的常數：
- Server 端（系計機器）：
    - `db_server.py`：
        - `PORT`
    - `developer_server.py`：
        - `DB_PORT`, `DEV_HOST`, `DEV_PORT`
    - `lobby_server.py`：
        - `DB_PORT`, `LOBBY_HOST`, `LOBBY_PORT`
    - `game_server.py`：
        - `LOBBY_PORT`（用於 GAME_OVER 回報）
- Client 端（助教本地機器）：
    - `developer_client.py`：
        - `DEV_HOST, DEV_PORT`
    - `player_client.py`：
        - `LOBBY_HOST`, `LOBBY_PORT`