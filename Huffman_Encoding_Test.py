import pytest
from Huffman_Encoding import HufCodec

# def test_single_character():
#     # Test with a single character
#     huf = HufCodec({'A': 1})
#     assert huf.to_dict() == {'A': '0'}
#     encoded = huf.encode('A' * 5)
#     assert encoded == '00000'
#     decoded = huf.decode(encoded)
#     assert decoded == 'AAAAA'


def test_two_characters():
    # Test with two characters with different frequencies
    huf = HufCodec({"A": 1, "B": 2})
    encoding = huf.to_dict()
    assert set(encoding.keys()) == {"A", "B"}
    assert len(set(encoding.values())) == 2  # Ensure different encodings for both
    encoded = huf.encode("AABBB")
    decoded = huf.decode(encoded)
    assert decoded == "AABBB"


def test_balanced_characters():
    # Test with characters having equal frequencies
    huf = HufCodec({"A": 1, "B": 1})
    encoding = huf.to_dict()
    assert set(encoding.keys()) == {"A", "B"}
    encoded = huf.encode("AABB")
    decoded = huf.decode(encoded)
    assert decoded == "AABB"


def test_multiple_characters():
    # Test with more complex character frequencies
    freq_dict = {"A": 5, "B": 9, "C": 12, "D": 13, "E": 16, "F": 45}
    huf = HufCodec(freq_dict)
    encoded = huf.encode("ABCDEF")
    decoded = huf.decode(encoded)
    assert decoded == "ABCDEF"
    assert len(huf.to_dict()) == 6  # Ensure all characters are encoded


def test_large_input():
    # Test encoding and decoding for large inputs
    freq_dict = {"A": 5, "B": 9, "C": 12, "D": 13, "E": 16, "F": 45}
    huf = HufCodec(freq_dict)
    large_input = "ABCDE" * 1000
    encoded = huf.encode(large_input)
    decoded = huf.decode(encoded)
    assert decoded == large_input  # Ensure correct roundtrip


def test_empty_input():
    # Test encoding and decoding an empty input
    huf = HufCodec({"A": 5, "B": 9})
    encoded = huf.encode("")
    decoded = huf.decode(encoded)
    assert encoded == ""  # Both encoded and decoded should be empty
    assert decoded == ""


def test_invalid_input_for_decode():
    # Test decoding with invalid characters in the bit string
    huf = HufCodec({"A": 5, "B": 9})
    encoded = huf.encode("AABBB")
    with pytest.raises(ValueError, match="Invalid bit in encoded string"):
        huf.decode("xyz")  # Invalid bits should raise an error


# def test_edge_case_single_repeated_symbol():
#     # Test repeated encoding of a single character
#     huf = HufCodec({'A': 1})
#     encoded = huf.encode('A' * 10)
#     decoded = huf.decode(encoded)
#     assert encoded == '0' * 10  # Since there's only one symbol, '0' repeated
#     assert decoded == 'A' * 10  # Should decode back to the original


def test_decoding_of_invalid_bit_string():
    # Test decoding a bit string that is not valid for the given encoding
    huf = HufCodec({"A": 3, "B": 6})
    encoded = huf.encode("AB")
    invalid_encoded = encoded + "2"  # Append an invalid character
    with pytest.raises(ValueError):
        huf.decode(invalid_encoded)


def test_to_dict_correctness():
    # Ensure that to_dict returns the correct encoding for the given input
    huf = HufCodec({"A": 5, "B": 9, "C": 12, "D": 13, "E": 16, "F": 45})
    encoding_dict = huf.to_dict()
    assert len(encoding_dict) == 6  # Six distinct characters should have encodings
    assert "A" in encoding_dict and "F" in encoding_dict  # Ensure keys are present
