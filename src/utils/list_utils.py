from typing import List
from typing import TypeVar

T = TypeVar("T")


def grouped(input_list: List[T], size: int) -> List[List[T]]:
    """
    Group list elements in chunks of size `size`.
    :param input_list: input list
    :param size: size of the chunk
    :return: list of chunks
    """
    return [input_list[i : i + size] for i in range(0, len(input_list), size)]  # noqa: E203
