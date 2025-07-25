from cperms_ins_enc.check_regular import regular_horizontal_insertion_encoding
from cperms_ins_enc.check_regular.check_regular_hori import dec_left


def test_hori_regular_check_fail():
    """Test that this class should fail as they are not permutations"""
    assert regular_horizontal_insertion_encoding("132, 212") is False
    assert dec_left([1, 0, 1], 1) is False


def test_hori_regular_check_pass():
    """Test that this class should pass."""
    assert regular_horizontal_insertion_encoding("132, 213")
    assert dec_left([1, 0, 2], 1)
