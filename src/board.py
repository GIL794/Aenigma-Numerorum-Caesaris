import json
import os
import random
from typing import List, Optional, Tuple

SAVE_FILE = "roman_sudoku_save.json"

class SudokuBoard:
    def __init__(self, puzzle: List[List[int]], solution: List[List[int]]):
        self.puzzle = puzzle  # 0 for empty
        self.solution = solution
        self.size = 9
        self.user = [[0 if puzzle[r][c] == 0 else puzzle[r][c] for c in range(9)] for r in range(9)]
        self.fixed = [[puzzle[r][c] != 0 for c in range(9)] for r in range(9)]
        self.symbol_perm = list(range(1, 10))  # permutation for reshuffling symbols (1..9)
        self.randomize_symbol_perm()

    def reset_user(self):
        self.user = [[self.puzzle[r][c] for c in range(9)] for r in range(9)]

    def set_cell(self, r: int, c: int, val: int):
        if self.fixed[r][c]:
            return
        self.user[r][c] = val

    def clear_cell(self, r: int, c: int):
        if self.fixed[r][c]:
            return
        self.user[r][c] = 0

    def is_complete(self) -> bool:
        for r in range(9):
            for c in range(9):
                if self.user[r][c] != self.solution[r][c]:
                    return False
        return True

    def get_conflicts(self, r: int, c: int) -> bool:
        # Returns True if user value at (r,c) conflicts with Sudoku rules
        val = self.user[r][c]
        if val == 0:
            return False
        # Row
        for cc in range(9):
            if cc != c and self.user[r][cc] == val:
                return True
        # Col
        for rr in range(9):
            if rr != r and self.user[rr][c] == val:
                return True
        # Box
        br, bc = (r // 3) * 3, (c // 3) * 3
        for rr in range(br, br + 3):
            for cc in range(bc, bc + 3):
                if (rr != r or cc != c) and self.user[rr][cc] == val:
                    return True
        # Also check against puzzle fixed duplicates (shouldn’t happen in valid puzzles)
        return False

    def randomize_symbol_perm(self):
        # Reshuffle a permutation of 1..9; this remaps display symbols only.
        perm = list(range(1, 10))
        random.shuffle(perm)
        self.symbol_perm = perm

    def permute_symbol(self, value: int) -> int:
        # Map 1..9 to permuted 1..9 for display; 0 stays 0
        if value == 0:
            return 0
        return self.symbol_perm[value - 1]

    def inverse_permute_symbol(self, display_value: int) -> int:
        # Map displayed value back to logical value
        if display_value == 0:
            return 0
        idx = self.symbol_perm.index(display_value)
        return idx + 1

    def get_hint_cell(self) -> Optional[Tuple[int, int, int]]:
        # Returns (r, c, correct_value) for one empty/incorrect cell
        for r in range(9):
            for c in range(9):
                if self.user[r][c] != self.solution[r][c]:
                    return (r, c, self.solution[r][c])
        return None

    def serialize(self) -> dict:
        return {
            "puzzle": self.puzzle,
            "solution": self.solution,
            "user": self.user,
            "fixed": self.fixed,
            "symbol_perm": self.symbol_perm,
        }

    @classmethod
    def deserialize(cls, data: dict) -> "SudokuBoard":
        obj = cls(data["puzzle"], data["solution"])
        obj.user = data["user"]
        obj.fixed = data["fixed"]
        obj.symbol_perm = data.get("symbol_perm", list(range(1, 10)))
        return obj

    def save(self):
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.serialize(), f)
        except (IOError, OSError) as e:
            print(f"Warning: Failed to save game state: {e}")

    @staticmethod
    def load_if_exists() -> Optional["SudokuBoard"]:
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return SudokuBoard.deserialize(data)
            except (IOError, OSError, json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Failed to load saved game: {e}")
                return None
        return None

def sample_puzzle() -> Tuple[List[List[int]], List[List[int]]]:
    # A valid Sudoku puzzle with a unique solution (0 = empty).
    # Puzzle and solution pair adapted from a common benchmark.
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    solution = [
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9],
    ]
    return puzzle, solution
