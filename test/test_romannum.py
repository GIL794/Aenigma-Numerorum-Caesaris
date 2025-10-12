from src.romannum import int_to_roman, roman_to_int

def test_roundtrip():
    for i in range(1, 10):
        r = int_to_roman(i)
        assert roman_to_int(r) == i
