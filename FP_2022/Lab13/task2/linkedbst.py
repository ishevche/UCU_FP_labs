"""
File: linked bst.py
Author: Ken Lambert
"""
import copy
import random
import time

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

        ans = ""
        if self.isEmpty():
            return ans
        current = self._root.right
        stack = LinkedStack([(self._root, 0)])
        cur_level = 0
        while not stack.isEmpty() or current is not None:
            if current is not None:
                cur_level += 1
                stack.push((current, cur_level))
                current = current.right
            else:
                parent, cur_level = stack.pop()
                ans += "| " * cur_level
                ans += str(parent.data) + "\n"
                current = parent.left

        return ans

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

        if self.isEmpty():
            return lst

        current: BSTNode = self._root
        stack = LinkedStack([current])
        current = current.left
        while not stack.isEmpty() or current is not None:
            if current is not None:
                stack.push(current)
                current = current.left
            else:
                parent = stack.pop()
                lst += [parent.data]
                current = parent.right

        return iter(lst)

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        current = self._root
        while current is not None:
            if item == current.data:
                return current.data
            elif item < current.data:
                current = current.left
            else:
                current = current.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            current = self._root

            while current is not None:
                if item < current.data:
                    if current.left is None:
                        current.left = BSTNode(item)
                        break
                    else:
                        current = current.left

                elif current.right is None:
                    current.right = BSTNode(item)
                    break
                else:
                    current = current.right
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

        if self.isEmpty():
            return 0
        queue = [self._root]
        height = -1
        while True:
            node_count = len(queue)
            if node_count == 0:
                return height
            height += 1
            while node_count > 0:
                node = queue.pop(0)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
                node_count -= 1

    def is_balanced(self):
        """
        Return True if tree is balanced
        """
        return self.height() < (2 * log(self._size + 1, 2)) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        """

        ans = []
        if self.isEmpty():
            return ans

        current = self._root
        stack = LinkedStack([current])
        current = current.left

        while not stack.isEmpty() or current is not None:
            if current is not None:
                if current.data > low:
                    stack.push(current)
                    current = current.left
                else:
                    if current.data == low:
                        ans += [current.data]
                    current = current.right
            else:
                parent = stack.pop()
                if low <= parent.data <= high:
                    ans += [parent.data]
                if parent.data < high:
                    current = parent.right
                else:
                    current = None

        return ans

    def rebalance(self):
        """
        Balances the tree.
        """

        nodes = list(self.inorder())
        self.clear()
        queue = [nodes]
        while queue:
            current = queue.pop(0)
            if not current:
                continue
            idx = len(current) // 2
            self.add(current[idx])
            queue.append(current[:idx])
            queue.append(current[idx + 1:])

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

    @staticmethod
    def demo_bst(path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        """

        def read_dict() -> list:
            ans = []
            with open(path, 'r') as dictionary:
                for word in dictionary:
                    ans.append(word.replace('\n', ''))
            return ans

        words_list = read_dict()
        bst_random = LinkedBST(random.shuffle(words_list.copy()))
        bst_balanced = copy.deepcopy(bst_random)
        bst_balanced.rebalance()
        words_to_find = random.sample(words_list, 10_000)

        time_start = time.perf_counter()
        for word_to_find in words_to_find:
            word_to_find in words_list
        time_list = time.perf_counter() - time_start

        time_start = time.perf_counter()
        for word_to_find in words_to_find:
            word_to_find in bst_random
        time_random = time.perf_counter() - time_start

        time_start = time.perf_counter()
        for word_to_find in words_to_find:
            word_to_find in bst_balanced
        time_balanced = time.perf_counter() - time_start

        print(f'┏━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓')
        print(f'┃ Amount ┃ Sorted list ┃ Random tree ┃ Balanced tree ┃')
        print(f'┣━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫')
        print(f'┃  10000 ┃ {time_list.__round__(9)} ┃ '
              f'{time_random.__round__(9)} ┃ {time_balanced.__round__(11)} ┃')
        print(f'┗━━━━━━━━┻━━━━━━━━━━━━━┻━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┛')

        return time_list, time_random, time_balanced


if __name__ == '__main__':
    LinkedBST.demo_bst('words.txt')
