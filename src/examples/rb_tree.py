
from random import shuffle
from time import sleep

from structures import Tree, RBTreeNode

BLACK = RBTreeNode.BLACK
RED = RBTreeNode.RED
NIL = RBTreeNode.NIL

def tree_insert(tree, data):
    node = RBTreeNode(data)
    node.left = node.right = NIL
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
    insert_case(tree, z)

def insert_case(tree, z):
    # Initally, z.color is RED
    # 
    # Case 1: z is root
    if not z.parent:
        # change z.color to BLACK
        z.color = BLACK
        return
    # Case 2: z.parent.color is BLACK, OK
    if z.parent.color == BLACK:
        return 
    # 
    # Now, z.parent.color is RED, so z must have a grandparent.
    # The colors of z and z.parent are both RED which is not allowed, we should deal with it.
    # 
    # Case 3: z.uncle.color is RED
    if z.uncle and z.uncle.color == RED:
        # invert the colors of z.parent, z.uncle and z.grandparent
        z.parent.color = BLACK
        z.uncle.color = BLACK
        z.grandparent.color = RED
        # process z.grandparent
        insert_case(tree, z.grandparent)
        return
    #
    # Now, z has no uncle or z.uncle.color is BLACK
    # 
    # Case 4:
    if z == z.parent.right and z.parent == z.grandparent.left:
        # exchange the role of z and z.parent
        tree.rotate_left(z.parent)
        z = z.left
        # now, z == z.parent.left and z.parent == z.grandparent.left
        # turn to Case 5.1
    elif z == z.parent.left and z.parent == z.grandparent.right:
        # exchange the role of z and z.parent
        tree.rotate_right(z.parent)
        z = z.right
        # now, z == z.parent.right and z.parent == z.grandparent.right
        # turn to Case 5.2
    # Case 5:
    # First, invert the colors of z.parent and z.grandparent
    z.parent.color = BLACK
    z.grandparent.color = RED
    # Case 5.1:
    if z == z.parent.left and z.parent == z.grandparent.left:
        tree.rotate_right(z.grandparent)
    # Case 5.2
    else:
        tree.rotate_left(z.grandparent)

def get_smallest_child(node):
    x = node
    while x.left:
        x = x.left
    return x

def tree_delete(tree, data):
    z = tree_search(tree, data)
    if z:
        if z.right:
            s = get_smallest_child(z.right)
            z.data, s.data = s.data, z.data
            z = s
        tree_delete_one_child_node(tree, z)
        return True
    else:
        return False
    
def tree_delete_one_child_node(tree, z):
    child = z.left if z.left else z.right
    
    if not z.parent and not child:
        tree.root = None
        return

    if not z.parent:
        child.parent = None
        child.color = BLACK
        tree.root = child
        return
    
    if z.parent.left == z:
        z.parent.left = child
    else:
        z.parent.right = child
    child.parent = z.parent

    if z.color == BLACK:
        if child.color == RED:
            child.color = BLACK
        else:
            delete_case(tree, child)

def delete_case(tree, x):
    # 
    # Initally, x.color is BLACK
    # 
    # Case 1: x is root
    if not x.parent:
        return
    # Case 2: x.sibling.color is RED
    if x.sibling.color == RED:
        # invert colors of x.parent and x.sibing
        x.parent.color = RED
        x.sibling.color = BLACK
        # rotate
        if x == x.parent.left:
            tree.rotate_left(x.parent)
        else:
            tree.rotate_right(x.parent)
        # turn to Case 4, 5, 6
    s = x.sibling
    # Case 3: x.parent, x.sibling and its childs are both BLACK
    if x.parent.color == s.color == s.left.color == s.right.color == BLACK:
        s.color = RED
        delete_case(tree, x.parent)
        return
    # Case 4:
    if x.parent.color == RED and s.color == s.left.color == s.right.color == BLACK:
        s.color = RED
        x.parent.color = BLACK
        return
    # Case 5:
    if s.color == BLACK:
        if x == x.parent.left and s.right.color == BLACK and s.left.color == RED:
            s.color = RED
            s.left.color = BLACK
            tree.rotate_right(s)
        elif x == x.parent.right and s.left.color == BLACK and s.right.color == RED:
            s.color = RED
            s.right.color = BLACK
            tree.rotate_left(s)
    # Case 6:
    s = x.sibling
    s.color = x.parent.color
    x.parent.color = BLACK
    if x == x.parent.left:
        s.right.color = BLACK
        tree.rotate_left(s.parent)
    else:
        s.left.color = BLACK
        tree.rotate_right(s.parent)

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
tree.bind('z', 0x0000ff)
lst = [1, 16, 21, 11, 8, 7, 10, 3, 4, 20, 17, 13, 2, 12, 10, 19, 5, 13, 3, 4, 20, 18] * 3
tree_build(tree, lst)

sleep(1)

for i in lst:
    tree_delete(tree, i)
