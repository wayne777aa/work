import random

# === 七種方塊 ===
TETROMINOES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1],
          [1, 1]],
    "T": [[0, 1, 0],
          [1, 1, 1]],
    "S": [[0, 1, 1],
          [1, 1, 0]],
    "Z": [[1, 1, 0],
          [0, 1, 1]],
    "J": [[1, 0, 0],
          [1, 1, 1]],
    "L": [[0, 0, 1],
          [1, 1, 1]],
}

def rotate_matrix(matrix):
    """順時針旋轉 90 度"""
    return [list(row) for row in zip(*matrix[::-1])]

class GameLogic:
    """處理單一玩家的遊戲規則"""
    def __init__(self, seed=None):
        random.seed(seed)
        self.board = [[0] * 10 for _ in range(20)]
        self.score = 0
        self.alive = True
        self.next_queue = self._gen_7bag()
        self.active = self._spawn_piece()

    # === 方塊生成 ===
    def _gen_7bag(self):
        bag = list("IJLOSTZ")
        random.shuffle(bag)
        return bag

    def _spawn_piece(self):
        if not self.next_queue:
            self.next_queue = self._gen_7bag()
        shape = self.next_queue.pop(0)
        piece = {
            "shape": shape,
            "matrix": [row[:] for row in TETROMINOES[shape]],
            "x": 3,
            "y": 0,
            "rot": 0,
        }
        if self._check_collision(piece["matrix"], piece["x"], piece["y"]):
            self.alive = False
        return piece

    # === 移動與掉落 ===
    def move_left(self):
        if not self.alive: return
        new_x = self.active["x"] - 1
        if not self._check_collision(self.active["matrix"], new_x, self.active["y"]):
            self.active["x"] = new_x

    def move_right(self):
        if not self.alive: return
        new_x = self.active["x"] + 1
        if not self._check_collision(self.active["matrix"], new_x, self.active["y"]):
            self.active["x"] = new_x

    def soft_drop(self):
        if not self.alive: return
        self.active["y"] += 1
        if self._check_collision(self.active["matrix"], self.active["x"], self.active["y"]):
            self.active["y"] -= 1
            self._lock_piece()

    def hard_drop(self):
        if not self.alive: return
        while not self._check_collision(self.active["matrix"], self.active["x"], self.active["y"] + 1):
            self.active["y"] += 1
        self._lock_piece()

    def rotate_cw(self):
        if not self.alive: return
        rotated = rotate_matrix(self.active["matrix"])
        if not self._check_collision(rotated, self.active["x"], self.active["y"]):
            self.active["matrix"] = rotated
            self.active["rot"] = (self.active["rot"] + 1) % 4

    def rotate_ccw(self):
        if not self.alive: return
        rotated = rotate_matrix(rotate_matrix(rotate_matrix(self.active["matrix"])))
        if not self._check_collision(rotated, self.active["x"], self.active["y"]):
            self.active["matrix"] = rotated
            self.active["rot"] = (self.active["rot"] - 1) % 4

    # === 碰撞檢查 ===
    def _check_collision(self, matrix, x, y):
        for dy, row in enumerate(matrix):
            for dx, val in enumerate(row):
                if not val:
                    continue
                bx, by = x + dx, y + dy
                # 超出邊界
                if bx < 0 or bx >= 10 or by >= 20:
                    return True
                # 與固定方塊重疊
                if by >= 0 and self.board[by][bx]:
                    return True
        return False

    # === 固定方塊、消行、得分 ===
    def _lock_piece(self):
        for dy, row in enumerate(self.active["matrix"]):
            for dx, val in enumerate(row):
                if val:
                    bx, by = self.active["x"] + dx, self.active["y"] + dy
                    if 0 <= by < 20:
                        self.board[by][bx] = 1
        self._clear_lines()
        self.active = self._spawn_piece()

    def _clear_lines(self):
        full_rows = [i for i, row in enumerate(self.board) if all(row)]
        for i in full_rows:
            del self.board[i]
            self.board.insert(0, [0] * 10)
        if full_rows:
            self.score += len(full_rows) * 100


    def get_combined_board(self):
        """回傳包含當前活動方塊的棋盤，用於顯示動畫"""
        b = [row[:] for row in self.board]  # 深拷貝固定方塊
        active = self.active
        if not active or not self.alive:
            return b
        for dy, row in enumerate(active["matrix"]):
            for dx, val in enumerate(row):
                if not val:
                    continue
                x = active["x"] + dx
                y = active["y"] + dy
                if 0 <= x < 10 and 0 <= y < 20:
                    b[y][x] = 2  # 使用 2 表示活動方塊
        return b
