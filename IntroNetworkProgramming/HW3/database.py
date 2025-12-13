import sqlite3
from datetime import datetime

DB_FILE = "game.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS User(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        passwordHash TEXT,
        online INTEGER DEFAULT 0
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Developer(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        passwordHash TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Room(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        hostUserId INTEGER,
        status TEXT,
        createdAt TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Game(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        developer TEXT,
        description TEXT,
        latestVersion TEXT,
        status TEXT DEFAULT 'active'
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS GameVersion(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gameId INTEGER,
        version TEXT,
        zipPath TEXT,
        createdAt TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Review(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gameId INTEGER,
        user TEXT,
        rating INTEGER,
        comment TEXT,
        createdAt TEXT
    )""")

    conn.commit()
    conn.close()

# ============================================================
#  統一格式的 DB 回應工具
# ============================================================
def ok(action_name, payload=None):
    return {
        "action": action_name,
        "data": payload or {}
    }

def error(msg):
    return {
        "action": "error",
        "data": {"msg": msg}
    }

# ============================================================
#  Main DB Handler
# ============================================================
def handle_request(req: dict) -> dict:
    coll = req.get("collection") # which table(User/Room/Game/...)
    act = req.get("action")      # what action(create/read/update/...)
    data = req.get("data", {})

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    try:
        # =====================================================
        # User
        # =====================================================
        if coll == "User" and act == "create": # 建立新使用者 return_data:null
            cur.execute("""
                INSERT INTO User(name, passwordHash, online)
                VALUES(?,?,?)""",(
                data["name"],
                data["passwordHash"],
                0
                )
            )
            conn.commit()
            return ok("user_created")

        elif coll == "User" and act == "read": # 讀單一使用者資料 return_data:row
            cur.execute("SELECT * FROM User WHERE name=?", (data["name"],))
            row = cur.fetchone()
            return ok("user_read", {"row": row})
        
        elif coll == "User" and act == "set_online": # 設定使用者線上狀態 return_data:null
            cur.execute(
                "UPDATE User SET online=? WHERE name=?",
                (data["online"], data["name"])
            )
            conn.commit()
            return ok("user_online_set")
        
        elif coll == "User" and act == "delete": # 刪除使用者 return_data:null
            cur.execute("DELETE FROM User WHERE name=?", (data["name"],))
            conn.commit()
            return ok("user_deleted")
        
        # =====================================================
        # Developer
        # =====================================================
        elif coll == "Developer" and act == "create":  # 註冊開發者
            cur.execute("""
                INSERT INTO Developer(name, passwordHash)
                VALUES(?,?)
            """, (
                data["name"],
                data["passwordHash"]
            ))
            conn.commit()
            return ok("developer_created")

        elif coll == "Developer" and act == "read":  # 讀單一開發者資料
            cur.execute("SELECT * FROM Developer WHERE name=?", (data["name"],))
            row = cur.fetchone()
            return ok("developer_read", {"row": row})

        elif coll == "Developer" and act == "delete":  # 刪除開發者
            cur.execute("DELETE FROM Developer WHERE name=?", (data["name"],))
            conn.commit()
            return ok("developer_deleted")

        # =====================================================
        # Room
        # =====================================================
        elif coll == "Room" and act == "create": # 建立新房間 return_data:room_id
            cur.execute("""
                INSERT INTO Room(name, hostUserId, status, createdAt)
                VALUES(?,?,?,?)""", (
                data["name"], 
                data["hostUserId"],
                data.get("status", "idle"), # default to idle
                datetime.now().isoformat()
                )
            )
            conn.commit()
            return ok("room_created", {"room_id": cur.lastrowid}) # 拿到 SQLite 自動產生的 id
        
        elif coll == "Room" and act == "read": # 讀單一房間資料 return_data:row
            cur.execute("SELECT * FROM Room WHERE id=?", (data["id"],))
            row = cur.fetchone()
            return ok("room_read", {"row": row})
        
        elif coll == "Room" and act == "query": # 讀全部房間列表 return_data:rows
            cur.execute("SELECT * FROM Room ")
            rows = cur.fetchall()
            return ok("room_query", {"rows": rows})
        
        elif coll == "Room" and act == "update": # 更新房間資料 return_data:null
            fields = []
            values = []

            for key in ["status", "hostUserId", "name"]:
                if key in data:
                    fields.append(f"{key}=?")
                    values.append(data[key])

            if not fields:
                return error("no room fields to update")
            
            values.append(data["id"])

            query = f"UPDATE Room SET {', '.join(fields)} WHERE id=?"
            cur.execute(query, tuple(values))
            conn.commit()
            return ok("room_updated")

        elif coll == "Room" and act == "delete": # 刪除房間 return_data:null
            cur.execute("DELETE FROM Room WHERE id=?", (data["id"],))
            conn.commit()
            return ok("room_deleted")
        
        # =====================================================
        # Game
        # =====================================================
        elif coll == "Game" and act == "create": # 建立新遊戲 return_data:game_id
            cur.execute("""
                INSERT INTO Game(name, developer, description, latestVersion, status)
                VALUES(?,?,?,?,?)
            """, (
                data["name"],
                data["developer"],
                data["description"],
                data["latestVersion"],
                data.get("status", "active")  # 預設 active
            ))
            conn.commit()
            return ok("game_created", {"game_id": cur.lastrowid})
        
        elif coll == "Game" and act == "read": # 讀單一遊戲資料 return_data:row
            if "id" in data:
                cur.execute("SELECT * FROM Game WHERE id=?", (data["id"],))
            elif "name" in data:
                cur.execute("SELECT * FROM Game WHERE name=?", (data["name"],))
            else:
                return error("id or name required")
            
            row = cur.fetchone()
            if not row:
                return error("game_not_found")

            result = {
                "id": row[0],
                "name": row[1],
                "developer": row[2],
                "description": row[3],
                "latestVersion": row[4],
                "status": row[5]
            }
            return ok("game_read", result)

        elif coll == "Game" and act == "query": # 讀全部遊戲列表 return_data:rows
            cur.execute("SELECT * FROM Game WHERE status='active'")
            rows = cur.fetchall()
            return ok("game_query", {"rows": rows})

        elif coll == "Game" and act == "update": # 更新遊戲資料 return_data:null
            # latestVersion 必填
            if "latestVersion" not in data:
                return error("latestVersion is required")

            fields = ["latestVersion=?"]       # 必填欄位先塞進來
            values = [data["latestVersion"]]   # 必填值也先放

            # description 可選填
            if "description" in data:
                fields.append("description=?")
                values.append(data["description"])

            # id 作為 WHERE 條件
            values.append(data["id"])

            query = f"UPDATE Game SET {', '.join(fields)} WHERE id=?"
            cur.execute(query, tuple(values))
            conn.commit()

            return ok("game_updated")
        
        elif coll == "Game" and act == "set_status":
            cur.execute("UPDATE Game SET status=? WHERE id=?", (
                data["status"],
                data["id"]
            ))
            conn.commit()
            return ok("game_status_updated")
        # =====================================================
        # GameVersion
        # =====================================================
        elif coll == "GameVersion" and act == "create": # 建立新遊戲版本 return_data:version_id
            cur.execute("""
                INSERT INTO GameVersion(gameId, version, zipPath, createdAt)
                VALUES(?,?,?,?)
            """, (
                data["gameId"],
                data["version"],
                data["zipPath"],
                datetime.now().isoformat()
            ))
            conn.commit()
            return ok("gameversion_created", {"version_id": cur.lastrowid})

        elif coll == "GameVersion" and act == "read": # 讀單一遊戲版本資料 return_data:row
            cur.execute("""
                SELECT * FROM GameVersion 
                WHERE gameId=? AND version=?
            """, (data["gameId"], data["version"]))
            row = cur.fetchone()
            return ok("gameversion_read", {"row": row})

        elif coll == "GameVersion" and act == "query": # 讀單一遊戲全部版本列表 return_data:rows
            cur.execute("SELECT * FROM GameVersion WHERE gameId=?",
                        (data["gameId"],))
            rows = cur.fetchall()
            return ok("gameversion_query", {"rows": rows})
        
        # =====================================================
        # Review
        # =====================================================
        elif coll == "Review" and act == "create": # 建立新評論 return_data:null
            cur.execute("""
                INSERT INTO Review(gameId, user, rating, comment, createdAt)
                VALUES(?,?,?,?,?)
            """, (
                data["gameId"],
                data["user"],
                data["rating"],
                data["comment"],
                datetime.now().isoformat()
            ))
            conn.commit()
            return ok("review_created")

        elif coll == "Review" and act == "query": # 讀單一遊戲全部評論列表 return_data:rows
            cur.execute("SELECT * FROM Review WHERE gameId=?",
                        (data["gameId"],))
            rows = cur.fetchall()
            return ok("review_query", {"rows": rows})

        elif coll == "Review" and act == "avg": # 讀單一遊戲評論平均分數 return_data:avg
            cur.execute("SELECT AVG(rating) FROM Review WHERE gameId=?",
                        (data["gameId"],))
            avg = cur.fetchone()[0]
            return ok("review_avg", {"avg": avg})
        
        # =====================================================
        # Unsupported
        # =====================================================
        else:
            return error(f"unsupported operation: {coll}.{act}")

    except Exception as e:
        return error(str(e))
    finally:
        conn.close()
