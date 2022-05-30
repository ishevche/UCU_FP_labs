# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class LinkedBinaryTree:
    """Linked representation of a binary tree structure."""

    # -------------------------- nested _Node class --------------------------
    class Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = 'element', '_parent', 'left', 'right'

        def __init__(self, element, left=None, right=None):
            self.element = element
            self.left = left
            self.right = right

    class Position:
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self.container = container
            self.node = node

        def element(self):
            """Return the element stored at this Position."""
            return self.node.element

        def __eq__(self, other):
            """
            Return True if other is a Position representing the same location.
            """
            return type(other) is type(self) and other.node is self.node

        def __hash__(self):
            return hash(self.node)

    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p.container is not self:
            raise ValueError('p does not belong to this container')
        return p.node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def get_root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)

    def get_left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node.left)

    def get_right(self, p):
        """
        Return the Position of p's right child (or None if no right child).
        """
        node = self._validate(p)
        return self._make_position(node.right)

    def set_root(self, e):
        """Place element e at the root of an empty tree and return new Position.

        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self.Node(e)
        return self._make_position(self._root)

    def add_left(self, p, e):
        """Create a new left child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node.left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        node.left = self.Node(e)
        return self._make_position(node.left)

    def add_right(self, p, e):
        """Create a new right child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already
            has a right child.
        """
        node = self._validate(p)
        if node.right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        node.right = self.Node(e)
        return self._make_position(node.right)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node.left is not None:  # left child exists
            count += 1
        if node.right is not None:  # right child exists
            count += 1
        return count

    def leaf_paths(self):
        """
        Prints paths from root to leafs
        """
        leafs = list()
        parents = {}
        dfs_stack = [self._make_position(self._root)]
        while dfs_stack:
            cur_vertex: LinkedBinaryTree.Position = dfs_stack.pop()
            if self.is_leaf(cur_vertex):
                leafs.append(cur_vertex)
            else:
                right = self.get_right(cur_vertex)
                left = self.get_left(cur_vertex)
                if right is not None:
                    parents[right] = cur_vertex
                    dfs_stack.append(right)
                if left is not None:
                    parents[left] = cur_vertex
                    dfs_stack.append(left)
        for leaf in leafs:
            print(leaf.element(), end='')
            while leaf in parents:
                leaf = parents[leaf]
                print(f'-{leaf.element()}', end='')
            print()

    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if len(self) != 0:
            for p in self._subtree_inorder(self.get_root()):
                yield p

    def _subtree_inorder(self, p):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if self.get_left(p) is not None:
            for other in self._subtree_inorder(self.get_left(p)):
                yield other
        yield p  # visit p between its subtrees
        if self.get_right(p) is not None:
            for other in self._subtree_inorder(self.get_right(p)):
                yield other

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0
