try:
    from py_tools.seq import isplit
except ImportError:
    def isplit(s, delimeter=None):
        return s.split(delimeter)

if 'ListNode' in globals():
    def _iter_f(self):
        curr = self
        while curr:
            yield curr.val
            curr = curr.next


    globals()['ListNode'].__iter__ = _iter_f
else:
    class ListNode:
        def __init__(self, x):
            self.val = x
            self.next = None

        def __iter__(self):
            curr = self
            while curr:
                yield curr.val
                curr = curr.next


class LinkedList:
    def __init__(self, node=None):
        self.head = None
        self.tail = None
        self.len = 0
        if hasattr(node, 'next'):
            while node:
                tmp = node.next
                self.push_tail(node)
                node = tmp
        elif isinstance(node, list):
            for x in node:
                self.push_tail(x)

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
