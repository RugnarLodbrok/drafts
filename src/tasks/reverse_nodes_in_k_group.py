from typing import List
from py_tools.common import add_to_pythonpath

add_to_pythonpath(__file__, 2)

from src.linked_list import LinkedList, ListNode


def reverse_n(ll, n):
    old_head = ll.head
    a = ll.head
    c = None
    while a:
        if not n:
            old_head.next = a
            break
        b = c
        c = a
        a = c.next
        c.next = b
        n -= 1
    else:
        ll.tail = old_head
    ll.head = c


def reverse_n_repeat(ll: LinkedList, n):
    """
    reverse every chunk of size :n: in LinkedList except remainder
    :param ll:
    :param n: chunk size
    :return:
    [1]->[2]->[3]->[4]->[5]->[6]->[7]->[8]->
         sn
    """

    ll.reverse(ll.head.next.next.next.next.next, 3)
    # remaining_size = len(ll)
    # node = ll.head
    # while remaining_size >= n:
    #     reverse_chunk(node, n)
    #     print(ll)
    #     node = node.next
    #     remaining_size -= n


if __name__ == '__main__':
    ll = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(ll)
    reverse_n_repeat(ll, 2)
    print(ll)
