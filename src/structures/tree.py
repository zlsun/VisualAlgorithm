
from .base import *

R = 30

class TreeNode(object):

    def __init__(self, data, parent=None):
        self.parent = parent
        self.data = data

    @property
    def grandparent(self):
        return self.parent and self.parent.parent

    @property
    def children(self):
        return iter()

    def get_pen(self, tree):
        return None

    def get_brush(self, tree):
        return None

    def plot(self, tree, painter, width, layer_height, pos=None):
        if not pos:
            pos = QPoint(0, layer_height / 2)

        rect = QRect(0, 0, R, R)
        rect.moveCenter(pos)

        painter.setPen(QColor(0x000000))
        painter.setBrush(tree.get_brush(self))
        painter.drawEllipse(rect)

        painter.setPen(tree.get_pen(self))
        painter.drawText(rect, Qt.AlignCenter, str(self.data))

    def get_height(self):
        return max(node.get_height() if node else 0 for node in self.children) + 1


class BinaryTreeNode(TreeNode):

    def __init__(self, data, parent=None):
        TreeNode.__init__(self, data, parent)
        self.left = None
        self.right = None

    def get_pen(self, tree):
        return TreeNode.get_pen(self, tree) or QColor(0x000000)

    @property
    def uncle(self):
        return self.parent and self.parent.sibling

    @property
    def sibling(self):
        if not self.parent:
            return None
        return self.parent.right if self.parent.left == self else self.parent.left

    @property
    def children(self):
        yield self.left
        yield self.right

    def plot(self, tree, painter, width, layer_height, pos=None):
        if not pos:
            pos = QPoint(0, layer_height / 2)
        dx = max(width / 4, R / 2)
        if self.left:
            p1 = QPoint(pos.x() - dx, pos.y() + layer_height)
            painter.setPen(QColor(0x000000))
            painter.drawLine(pos, p1)
            self.left.plot(tree, painter, width / 2, layer_height, p1)
        if self.right:
            p2 = QPoint(pos.x() + dx, pos.y() + layer_height)
            painter.setPen(QColor(0x000000))
            painter.drawLine(pos, p2)
            self.right.plot(tree, painter, width / 2, layer_height, p2)
        TreeNode.plot(self, tree, painter, width, layer_height, pos)


class RBTreeNode(BinaryTreeNode):

    RED = 0
    BLACK = 1

    def __init__(self, data, color=RED, parent=None):
        BinaryTreeNode.__init__(self, data, parent)
        self.color = color

    def __bool__(self):
        return self != None and self != self.NIL

    def get_pen(self, tree):
        return QColor(0xffffff)

    def get_brush(self, tree):
        return QColor(0x000000 if self.color else 0xff0000)

RBTreeNode.NIL = RBTreeNode("NIL", color=RBTreeNode.BLACK)


class Tree(Base):

    def __init__(self):
        Base.__init__(self)
        self.root = None

    def get_pen(self, node):
        return Base.get_pen(self, node) or node.get_pen(self) or QColor(0x000000)

    def get_brush(self, node):
        return Base.get_brush(self, node) or node.get_brush(self) or QColor(0xffffff)

    def get_height(self):
        return self.root.get_height()

    def rotate(self, node, is_right):
        parent = node.parent

        if is_right:
            child = node.left
            grandchild = child.right
            node.left = grandchild
            child.right = node
        else:
            child = node.right
            grandchild = child.left
            node.right = grandchild
            child.left = node

        if grandchild:
            grandchild.parent = node

        node.parent = child

        child.parent = parent
        if parent:
            if parent.left == node:
                parent.left = child
            else:
                parent.right = child
        else:
            self.root = child

    def rotate_right(self, node):
        self.rotate(node, is_right=True)

    def rotate_left(self, node):
        self.rotate(node, is_right=False)

    def draw(self, visualization, painter):
        w, h = visualization.width(), visualization.height()
        if not self.root:
            return
        layer_height = h / self.get_height()
        painter.translate(w / 2, 0)
        painter.scale(1, 1)
        self.root.plot(self, painter, w, layer_height)
