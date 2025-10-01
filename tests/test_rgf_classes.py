from cperms_ins_enc import (
    RGFVerticalSearcher,
    RGFHorizontalSearcher,
    MatchingHorizontalSearcher,
)


def test_vertical_rgfs():
    basis = "231,312,2121"
    spec = RGFVerticalSearcher(basis).auto_search(max_expansion_time=600)
    assert [spec.count_objects_of_size(i) for i in range(10)] == [
        1,
        1,
        2,
        5,
        14,
        40,
        114,
        324,
        920,
        2612,
    ]


def test_horizontal_rgfs():
    basis = "100,120,210"
    spec = RGFHorizontalSearcher(basis).auto_search(max_expansion_time=600)
    assert [spec.count_objects_of_size(i) for i in range(10)] == [
        1,
        1,
        2,
        5,
        13,
        34,
        89,
        233,
        610,
        1597,
    ]


def test_horizontal_rgfs():
    basis = "1201,1320"
    spec = MatchingHorizontalSearcher(basis).auto_search(max_expansion_time=600)
    assert [spec.count_objects_of_size(i) for i in range(11)] == [
        1,
        0,
        1,
        0,
        3,
        0,
        12,
        0,
        45,
        0,
        165,
    ]
