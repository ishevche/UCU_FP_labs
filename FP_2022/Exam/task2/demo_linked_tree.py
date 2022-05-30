"""
demonstration of linked trees
"""

from linked_binary_tree import LinkedBinaryTree


def main():
    """
    Demonstrates trees abilities
    """
    tree = LinkedBinaryTree()
    one = tree.set_root(1)
    two = tree.add_left(one, 2)
    tree.add_left(two, 4)
    tree.add_right(two, 5)
    three = tree.add_right(one, 3)
    eight = tree.add_right(three, 8)
    tree.add_left(eight, 6)
    tree.add_right(eight, 7)
    print('Leaf paths:')
    tree.leaf_paths()
    print('Inorder:', '-'.join(map(lambda x: str(x.element()), tree.inorder())))


if __name__ == '__main__':
    main()
