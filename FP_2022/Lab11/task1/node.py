"""
File: node.py

Node classes for one-way linked structures and two-way
linked structures.
"""


class Node:

    def __init__(self, data, next=None):
        """Instantiates a Node with default next_node of None"""
        self.item = data
        self.next = next
