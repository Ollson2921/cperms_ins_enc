from insertion_encoding import VatterVerticalSearcher, VatterHorizontalSearcher


def test_vatter_vertical():
    basis = "12, 21"
    spec = VatterVerticalSearcher(basis).auto_search(max_expansion_time=600)

    n = 10
    counts = [spec.count_objects_of_size(i) for i in range(n)]
    assert counts == [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]


def test_vatter_horizontal():
    basis = "12_11"
    spec = VatterHorizontalSearcher(basis).auto_search(max_expansion_time=6000)
    n = 10
    counts = [spec.count_objects_of_size(i) for i in range(n)]
    assert counts == [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
