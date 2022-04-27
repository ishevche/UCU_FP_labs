"""
multiset.py
"""
from node import Node


class Multiset:
    """
    A class implementing Multiset as a linked list.
    """

    def __init__(self):
        """
        Produces a newly constructed empty Multiset.
        __init__: -> Multiset
        Field: _head points to the first node in the linked list
        """
        self._head: Node | None = None

    def empty(self):
        """
        Checks emptiness of Multiset.
        empty: Multiset -> Bool
        :return: True if Multiset is empty and False otherwise.
        """
        return self._head is None

    def __contains__(self, value):
        """
        Checks existence of value in the Multiset.
        __contains__: Multiset Any -> Bool
        :param value: the value to be check.
        :return: True if Multiset is in the Multiset and False otherwise.
        """
        current = self._head
        while current is not None:
            if current.item == value:
                return True
            else:
                current = current.next
        return False

    def add(self, value):
        """
        Adds the value to multiset.

        :param value: the value to be added.
        """
        if self._head is None:
            self._head = Node(value)
        else:
            rest = self._head
            self._head = Node(value)
            self._head.next = rest

    def delete(self, value):
        """

        :param value: value first occurrence of which should be deleted.
        """
        current = self._head
        previous = None
        while current is not None and current.item != value:
            previous = current
            current = current.next
        if current is not None:
            if previous is None:
                self._head = self._head.next
            else:
                previous.next = current.next

    def remove_all(self):
        """
        Clears all multiset, returns elements
        """
        current = self._head
        elements = []
        while current is not None:
            elements += [current.item]
            current = current.next
        self._head = None
        return elements

    def split_half(self):
        """
        Splits a multiset in two
        """
        length = len(self)
        second_part = Multiset()
        if length < 2:
            return None
        first_length = (length + 1) // 2
        cur = self._head
        for _ in range(first_length - 1):
            cur = cur.next
        first_node = cur.next
        cur.next = None
        second_part._head = first_node
        return self, second_part

    def extend(self, other):
        """
        Extends a multiset
        """
        prev_head = self._head
        self._head = other._head
        cur = self._head
        while cur.next is not None:
            cur = cur.next
        cur.next = prev_head
        return self

    def __len__(self):
        amount = 0
        cur = self._head
        while cur is not None:
            amount += 1
            cur = cur.next
        return amount
