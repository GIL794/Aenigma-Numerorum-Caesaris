# Roman numeral utilities tailored to Sudoku 1–9.
ROMAN_TO_INT_MAP = {
    "I": 1, "II": 2, "III": 3, "IV": 4,
    "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9
}
INT_TO_ROMAN_MAP = {v: k for k, v in ROMAN_TO_INT_MAP.items()}

VALID_ROMAN_TOKENS = set(ROMAN_TO_INT_MAP.keys())

def int_to_roman(n: int) -> str:
    if n not in INT_TO_ROMAN_MAP:
        raise ValueError("Only supports 1..9")
    return INT_TO_ROMAN_MAP[n]

def roman_to_int(s: str) -> int:
    s = s.strip().upper()
    if s not in ROMAN_TO_INT_MAP:
        raise ValueError("Invalid Roman numeral for 1..9")
    return ROMAN_TO_INT_MAP[s]

def normalize_roman_input(buffer: str) -> str:
    # Accepts partial input typed by user (I,V,X) and returns a commit-ready Roman if valid 1..9, else empty or partial.
    s = buffer.strip().upper()
    if s in VALID_ROMAN_TOKENS:
        # Check if this could be a prefix of a longer valid Roman numeral
        # Don't auto-commit if adding I, V, or X could form a valid longer numeral
        for next_char in ["I", "V", "X"]:
            potential = s + next_char
            if potential in VALID_ROMAN_TOKENS:
                return ""  # Don't commit yet, could be longer
        return s  # Safe to commit, cannot be extended
    # If invalid or too long, return empty (caller may decide to clear)
    return ""
