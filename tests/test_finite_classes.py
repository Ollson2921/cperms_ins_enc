from insertion_encoding import HorizontalSearcher, VerticalSearcher


def test_horizontal_searcher():
    """
    Test the HorizontalSearcher with a finite class of Cayley permutations.
    """
    basis = "210, 012, 100"

    assert HorizontalSearcher(basis).auto_search(max_expansion_time=60000)


def test_vertical_searcher():
    """
    Test the VerticalSearcher with a finite class of Cayley permutations.
    """
    basis = "210, 012, 100"

    assert VerticalSearcher(basis).auto_search(max_expansion_time=60000)
