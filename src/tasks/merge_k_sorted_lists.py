from typing import List
from py_tools.common import add_to_pythonpath

add_to_pythonpath(__file__, 2)

from src.linked_list import LinkedList, ListNode


def insort(a: list, x, key=None):
    i = 0
    j = len(a)
    if key:
        while i < j:
            mid = (i + j) // 2
            if key(x) <= key(a[mid]):
                j = mid
            else:
                i = mid + 1
    else:
        while i < j:
            mid = (i + j) // 2
            if x <= a[mid]:
                j = mid
            else:
                i = mid + 1
    a.insert(i, x)
    return i


def merge(lists):
    r = LinkedList()
    key_f = lambda a: -a.head.val
    lists = [l for l in lists if l.head]
    lists = sorted(lists, key=key_f)
    while lists:
        current_list = lists.pop()
        r.push_tail(current_list.pop_head())
        if current_list:
            insort(lists, current_list, key=key_f)
    return r


class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        return merge([LinkedList(x) for x in lists]).head


if __name__ == '__main__':
    print(LinkedList(Solution().mergeKLists([l.head for l in [
        LinkedList.from_string("1->4->5", type=int),
        LinkedList.from_string("2->6", type=int),
        LinkedList.from_string("1->3->4", type=int),
    ]])))

    print(LinkedList(Solution().mergeKLists([l.head for l in [
        LinkedList()
    ]])))
