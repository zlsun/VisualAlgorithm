
from random import shuffle, randrange
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
tree.bind('x', 0x00ff00)
tree.bind('z', 0xff0000)

N = 50
lst = [randrange(N) for _ in range(N)]
tree_build(tree, lst)

sleep(1)

for i in lst:
    tree_search(tree, i)

