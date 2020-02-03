from typing import List
from py_tools.common import add_to_pythonpath

add_to_pythonpath(__file__, 2)

from src.linked_list import LinkedList, ListNode

if __name__ == '__main__':
    print(LinkedList)
