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

        def __repr__(self):
            if self.next:
                if self.next.next:
                    return f"[{self.val}]->[{self.next.val}]->..."
                else:
                    return f"[{self.val}]->[{self.next.val}]"
            else:
                return f"[{self.val}]"


class LinkedList:
    def __init__(self, node=None):
        """
        if head/tail or nodes altered directly or bypassing LinkedList methods head/tail state
        could become inconsistent. Therefore behaviour is undefined
        :param node: vanilla list or ListNode
        """
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

    def reverse(self, node_before=None, n=None):
        """
        reverse linked list in one pass;
        :param node_before: a node before the chunk to be reversed. Has role of a pointer to the chunk
               When node_before is None; list reversed from the head;
        :param n: number of nodes to be reversed
        :return:
        """
        if node_before or (n is not None):
            return self._reverse_chunk(node_before, n)
        self.tail = self.head
        a = self.head
        c = None
        while a:
            b = c
            c = a
            a = c.next
            c.next = b
        self.head = c

    def _reverse_chunk(self, node_before, n):
        """
        :param node_before: a node before the chunk to be reversed. Has role of a pointer to the chunk
        :param n: number of nodes to be reversed
        :return:
        """
        if n is None:
            n = len(self)
        if node_before:
            first_node = node_before.next
        else:
            first_node = self.head
        a = first_node
        c = None
        while a:
            if not n:  # chunk ended
                first_node.next = a
                break
            b = c
            c = a
            a = c.next
            c.next = b
            n -= 1
        else:  # list ended
            self.tail = first_node
        if node_before:
            node_before.next = c
        else:
            self.head = c

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
