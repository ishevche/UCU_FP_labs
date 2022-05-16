"""
File: linked bst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log


class LinkedBST(AbstractCollection):
    """A link-based binary search tree implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            ans = ""
            if node is not None:
                ans += recurse(node.right, level + 1)
                ans += "| " * level
                ans += str(node.data) + "\n"
                ans += recurse(node.left, level + 1)
            return ans

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lst)

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        post-condition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree.""")

        def lift_max_in_left_subtree_to_top(top):
            """
            Replace top's datum with the maximum datum in the left subtree
            Pre:  top has a left child
            Post: the maximum node in top's left subtree
                  has been removed
            Post: top. data = maximum value in top's left subtree
            """
            max_parent = top
            max_node = top.left
            while max_node.right is not None:
                max_parent = max_node
                max_node = max_node.right
            top.data = max_node.data
            if max_parent == top:
                top.left = max_node.left
            else:
                max_parent.right = max_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while current_node is not None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximum node in the left subtree
        if current_node.left is not None \
                and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed any harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise.
        """
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        """

        def is_leaf(node: BSTNode):
            """
            Determines whether the node is a leaf
            """
            return node.left is None and node.right is None

        def recurse(top: BSTNode):
            """
            Helper function
            """
            if top is None or is_leaf(top):
                return 0
            else:
                return 1 + max(recurse(top.left), recurse(top.right))

        return recurse(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        """
        return self.height() < (2 * log(self._size + 1, 2)) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        """

        def recurse(node):
            ans = []
            if node is None:
                return ans
            if node.data > low:
                ans += recurse(node.left)
            if low <= node.data <= high:
                ans += [node.data]
            if node.data < high:
                ans += recurse(node.right)
            return ans

        return recurse(self._root)

    def rebalance(self):
        """
        Balances the tree.
        """

        def recurse(elements: list):
            if elements:
                idx = len(elements) // 2
                self.add(elements[idx])
                recurse(elements[:idx])
                recurse(elements[idx + 1:])

        nodes = self.inorder()
        nodes = sorted(nodes)
        self.clear()
        recurse(nodes)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        """
        cur_node = self._root
        ans = None
        while cur_node is not None:
            if cur_node.data <= item:
                cur_node = cur_node.right
            else:
                ans = cur_node.data
                cur_node = cur_node.left
        return ans

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        """
        cur_node = self._root
        ans = None
        while cur_node is not None:
            if cur_node.data < item:
                ans = cur_node.data
                cur_node = cur_node.right
            else:
                cur_node = cur_node.left
        return ans

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        """
