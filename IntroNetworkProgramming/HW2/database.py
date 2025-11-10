import sqlite3
from datetime import datetime

DB_FILE = "game.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS User(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        email TEXT,
        passwordHash TEXT,
        createdAt TEXT,
        lastLoginAt TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Room(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        hostUserId INTEGER,
        visibility TEXT,
        status TEXT,
        createdAt TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS GameLog(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roomId INTEGER,
        users TEXT,
        startAt TEXT,
        endAt TEXT,
        result TEXT
    )""")

    conn.commit()
    conn.close()

def handle_request(req: dict) -> dict:
    coll = req.get("collection") # which table(User/Room/GameLog)
    act = req.get("action")      # what action(create/read/update/...)
    data = req.get("data", {})
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    try:
        # ========== User =============
        if coll == "User" and act == "create":
            cur.execute("""
                INSERT INTO User(name,email,passwordHash,createdAt,lastLoginAt)
                VALUES(?,?,?,?,?)""",(
                data["name"], data["email"], data["passwordHash"],
                datetime.now().isoformat(), 
                datetime.now().isoformat()
                )
            )
            conn.commit()
            return {"ok": True, "msg": "User created"}

        elif coll == "User" and act == "read":
            cur.execute("SELECT * FROM User WHERE name=?", (data["name"],))
            row = cur.fetchone()
            return {"ok": bool(row), "data": row}
        
        elif coll == "User" and act == "update":
            cur.execute(
                "UPDATE User SET lastLoginAt=? WHERE name=?",
                (datetime.now().isoformat(), data["name"])
            )
            conn.commit()
            return {"ok": True, "msg": "User updated"}
        
        elif coll == "User" and act == "delete":
            cur.execute("DELETE FROM User WHERE name=?", (data["name"],))
            conn.commit()
            return {"ok": True, "msg": "User deleted"}
        
        # ========== Room =============
        elif coll == "Room" and act == "create":
            cur.execute("""
                INSERT INTO Room(name,hostUserId,visibility,status,createdAt)
                VALUES(?,?,?,?,?)""", (
                data["name"], data["hostUserId"],
                data.get("visibility", "public"), # default to public
                data.get("status", "idle"), # default to idle
                data.get("createdAt", datetime.now().isoformat())
                )
            )
            conn.commit()
            room_id = cur.lastrowid  # 拿到 SQLite 自動產生的 id
            return {"ok": True, "room_id": room_id, "msg": f"Room {room_id} created"}
        
        elif coll == "Room" and act == "query":
            cur.execute("SELECT * FROM Room ")
            rows = cur.fetchall()
            return {"ok": True, "data": rows}
        
        elif coll == "Room" and act == "update":
            fields = []
            values = []

            if "status" in data:
                fields.append("status=?")
                values.append(data["status"])
            if "visibility" in data:
                fields.append("visibility=?")
                values.append(data["visibility"])
            if "hostUserId" in data:
                fields.append("hostUserId=?")
                values.append(data["hostUserId"])
            if "name" in data:
                fields.append("name=?")
                values.append(data["name"])

            if not fields:
                return {"ok": False, "msg": "No fields to update"}
            
            values.append(data["id"])

            query = f"UPDATE Room SET {', '.join(fields)} WHERE id=?"
            cur.execute(query, tuple(values))
            conn.commit()
            return {"ok": True, "msg": "Room updated"}

        elif coll == "Room" and act == "delete":
            cur.execute("DELETE FROM Room WHERE id=?", (data["id"],))
            conn.commit()
            return {"ok": True, "msg": "Room deleted"}

        # ========== GameLog ==========
        elif coll == "GameLog" and act == "create":
            cur.execute("""
                INSERT INTO GameLog(roomId,users,startAt,endAt,result)
                VALUES(?,?,?,?,?)
            """, (
                data["roomId"], 
                str(data["users"]), # 不支援 list 直接存，改存成 str
                data["startAt"], 
                data["endAt"], 
                str(data["result"])
                )
            )
            conn.commit()
            return {"ok": True, "msg": "GameLog created"}
        
        elif coll == "GameLog" and act == "query":
            cur.execute("SELECT * FROM GameLog")
            rows = cur.fetchall()
            return {"ok": True, "data": rows}

        else:
            return {"ok": False, "msg": "Unsupported operation"}

    except Exception as e:
        return {"ok": False, "msg": str(e)}
    finally:
        conn.close()
