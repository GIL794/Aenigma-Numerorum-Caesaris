from src.romannum import int_to_roman, roman_to_int, normalize_roman_input

def test_roundtrip():
    for i in range(1, 10):
        r = int_to_roman(i)
        assert roman_to_int(r) == i

def test_normalize_roman_input():
    """Test that normalize_roman_input only commits when Roman numeral cannot be extended."""
    # These can be extended, so should return empty string (don't commit yet)
    assert normalize_roman_input("I") == "", "I can extend to II, III, IV, IX"
    assert normalize_roman_input("II") == "", "II can extend to III"
    assert normalize_roman_input("V") == "", "V can extend to VI, VII"
    assert normalize_roman_input("VI") == "", "VI can extend to VII"
    assert normalize_roman_input("VII") == "", "VII can extend to VIII"
    
    # These cannot be extended further, so should return the value (commit)
    assert normalize_roman_input("III") == "III", "III cannot be extended"
    assert normalize_roman_input("IV") == "IV", "IV cannot be extended"
    assert normalize_roman_input("VIII") == "VIII", "VIII cannot be extended"
    assert normalize_roman_input("IX") == "IX", "IX cannot be extended"
    
    # Invalid input should return empty string
    assert normalize_roman_input("IIII") == "", "IIII is invalid"
    assert normalize_roman_input("VV") == "", "VV is invalid"
    assert normalize_roman_input("IIX") == "", "IIX is invalid"
