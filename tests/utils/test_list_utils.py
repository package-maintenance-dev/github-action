from src.utils.list_utils import grouped


def test_grouped():
    input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    size = 4
    result = grouped(input_list, size)
    assert result == [[1, 2, 3, 4], [5, 6, 7, 8], [9]]
