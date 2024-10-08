import pytest
from Huffman_Encoding import HufCodec


def test_huffman_encoding_decoding():
    freq_dict = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
    codec = HufCodec(freq_dict)
    encoded = codec.encode("abcdef")
    assert isinstance(encoded, str)
    decoded = codec.decode(encoded)
    assert decoded == "abcdef"


def test_single_symbol():
    freq_dict = {"a": 100}
    codec = HufCodec(freq_dict)
    encoded = codec.encode("aaaa")
    assert encoded == "0000"
    decoded = codec.decode(encoded)
    assert decoded == "aaaa"


def test_edge_case_decoding_invalid_bit():
    freq_dict = {"a": 5, "b": 9}
    codec = HufCodec(freq_dict)
    encoded = codec.encode("ab")
    decoded = codec.decode(encoded)
    assert decoded == "ab"


def test_empty_string():
    freq_dict = {"a": 5, "b": 9}
    codec = HufCodec(freq_dict)
    encoded = codec.encode("")
    decoded = codec.decode(encoded)
    assert encoded == ""
    assert decoded == ""


def test_long_sequence():
    freq_dict = {"a": 5, "b": 9, "c": 12, "d": 13}
    codec = HufCodec(freq_dict)
    long_sequence = "abcd" * 1000
    encoded = codec.encode(long_sequence)
    decoded = codec.decode(encoded)
    assert decoded == long_sequence


def test_equal_frequencies():
    freq_dict = {"a": 10, "b": 10, "c": 10, "d": 10}
    codec = HufCodec(freq_dict)
    encoded = codec.encode("abcd")
    decoded = codec.decode(encoded)
    assert decoded == "abcd"
