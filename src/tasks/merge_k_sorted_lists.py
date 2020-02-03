from py_tools.seq import isplit
import bisect


def insort(a: list, x, key=None):
    if not key:
        key = lambda x: x
    i = 0
    j = len(a)
    while True:
        mid = (i + j) // 2
        if key(x) >= key(a[mid]):
            if i == mid:
                break
            i = mid
        else:
            j = mid
    a.insert(i, x)
    return i


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.len = 0

    def push_tail(self, v):
        if not isinstance(v, ListNode):
            v = ListNode(v)
        else:
            v.next = None
        if not self.tail:
            self.head = v
            self.tail = v
        self.tail.next = v
        self.tail = v
        self.len += 1

    def push_head(self, v):
        if not isinstance(v, ListNode):
            v = ListNode(v)
        else:
            v.next = None
        v.next = self.head
        self.head = v
        if not self.tail:
            self.tail = self.head
        self.len += 1

    def pop_head(self):
        if not self.len:
            return None
        r = self.head
        self.head = r.next
        if not self.head:
            self.tail = None
        self.len -= 1
        return r

    @classmethod
    def from_string(cls, s, type=None):
        """
        :param s: `1->1->2->3->4->4->5->6`
        """
        r = LinkedList()
        for v in isplit(s, '->'):
            if type is not None:
                v = type(v)
            r.push_tail(v)
        return r

    def __len__(self):
        return self.len

    def __bool__(self):
        return self.len

    def __str__(self):
        return "->".join(str(x) for x in self.head)


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __iter__(self):
        curr = self
        while curr:
            yield curr.val
            curr = curr.next


def merge(lists):
    r = LinkedList()
    lists = sorted(lists, key=lambda a: a.head.val)
    while lists:
        r.push_tail(lists[0].pop_head())
        if not lists[0]:
            lists.pop(0)
        else:
            bisect.insort()


if __name__ == '__main__':
    # merge([
    #     LinkedList.from_string("1->4->5"),
    #     LinkedList.from_string("2->6"),
    #     LinkedList.from_string("1->3->4"),
    # ])
    a = [1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 7]
    i = insort(a, 5)
    print(a[:i], a[i], a[i + 1:])
