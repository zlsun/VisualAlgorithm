
from random import shuffle
from time import sleep

from structures import Tree, BinaryTreeNode


def tree_insert(tree, data):
    node = BinaryTreeNode(data)
    tree_insert_node(tree, node)

def tree_insert_node(tree, z):
    x = tree.root
    y = None
    while x:
        y = x
        if z.data < x.data:
            x = x.left
        else:
            x = x.right
    z.parent = y
    if not y:
        tree.root = z
    elif z.data < y.data:
        y.left = z
    else:
        y.right = z

def tree_build(tree, lst):
    shuffle(lst)
    for i in lst:
        tree_insert(tree, i)

def tree_search(tree, data):
    x = tree.root
    while x and x.data != data:
        if x.data > data:
            x = x.left
        else:
            x = x.right
    return x


tree = Tree()
tree.add_mark('x', 0x00ff00)
tree.add_mark('z', 0xff0000)
lst = [1, 16, 21, 11, 8, 7, 10, 3, 4, 20, 17, 13, 2, 12, 10, 19, 5, 13, 3, 4, 20, 18]
tree_build(tree, lst)

sleep(1)

for i in lst:
    tree_search(tree, i)
