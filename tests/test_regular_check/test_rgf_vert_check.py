from cperms_ins_enc import rgf_regular_vertical_insertion_encoding
from cperms_ins_enc.check_regular.rgf_vert_regular_check import (
    greedy_grid_left,
    grid_inc_con,
    grid_inc_dec,
)


def test_the_checks():
    assert greedy_grid_left([0, 1, 2, 3, 4, 2, 5, 1, 6], 0)  # dec_inc passes
    assert greedy_grid_left([0, 1, 2, 4, 0, 5, 1, 6, 2], 1)  # inc_inc passes
    assert not greedy_grid_left([0, 1, 2, 3, 0, 2, 3, 1], 1)  # inc_inc fails

    assert grid_inc_con([0, 1, 2, 3, 4, 0, 1, 5, 2, 5, 5, 3, 4])  # inc_con passes
    assert grid_inc_con([0, 1, 2, 3, 4, 0, 1, 4, 2, 3])  # inc_con passes
    assert not grid_inc_con([0, 1, 2, 3, 2, 0, 2, 1, 2, 2])  # inc_con fails
    assert grid_inc_dec([1, 2, 0])  # should be true


def test_bases():
    basis = "120, 100, 000"
    assert rgf_regular_vertical_insertion_encoding(basis)
    basis = "120, 110, 000"
    assert rgf_regular_vertical_insertion_encoding(basis)
