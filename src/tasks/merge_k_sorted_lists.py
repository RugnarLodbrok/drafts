from py_tools.seq import isplit


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
        else:
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
        return not not self.len

    def __str__(self):
        return "->".join(str(x) for x in self.head or [])

    def __repr__(self):
        return str(self)


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
    key_f = lambda a: -a.head.val
    lists = sorted(lists, key=key_f)
    while lists:
        current_list = lists.pop()
        r.push_tail(current_list.pop_head())
        if current_list:
            insort(lists, current_list, key=key_f)
    return r


if __name__ == '__main__':
    print(merge([
        LinkedList.from_string("1->4->5", type=int),
        LinkedList.from_string("2->6", type=int),
        LinkedList.from_string("1->3->4", type=int),
    ]))
