class Node:

    def __init__(self, data):
        self.data = data
        self.left = self.right = None


class BTree:

    def __init__(self):
        self.root = None

    def __find(self, node, parent, value):
        if node is None:
            return None, parent, False
        if value == node.data:
            return node, parent, True
        if value < node.data:
            if node.left is not None:
                return self.__find(node.left, node, value)
        if value > node.data:
            if node.right is not None:
                return self.__find(node.right, node, value)
        return node, parent, False

    def append(self, data):
        obj = Node(data)
        if self.root is None:
            self.root = obj
            return obj

        s, p, fl_find = self.__find(self.root, None, obj.data) # fl_find - флаг, True если вершина со значением уже существует

        if not fl_find and s:
            if obj.data < s.data:
                s.left = obj
            else:
                s.right = obj
        return obj

    def __del_leaf(self, s, p):
        if p.left == s:
            p.left = None
        elif p.right == s:
            p.right = None
        return None

    def __del_one_child(self, s, p):
        if p.left == s:
            if s.left is None:
                p.left = s.right
            elif s.right is None:
                p.left = s.left
        elif p.right == s:
            if s.left is None:
                p.right = s.right
            elif s.right is None:
                p.right = s.left
        return None

    def __find_min(self, node, parent):
        if node.left:
            return self.__find_min(node.left, node)
        return node, parent

    def delete(self, value):
        s, p, fl_find = self.__find(self.root, None, value)
        if s is None:
            return None

        if not fl_find:
            return None

        if s.left is None and s.right is None:
            self.__del_leaf(s, p)
            return None

        if s.left is None or s.right is None:
            self.__del_one_child(s, p)
            return None

        sr, pr = self.__find_min(s.right, s)
        s.data = sr.data
        self.__del_one_child(sr, pr)


    def show_tree(self):
        v = [self.root]
        while v:
            vn = []
            for x in v:
                print(x.data, end=' ')
                if x.left:
                    vn += [x.left]
                if x.right:
                    vn += [x.right]
            v = vn
            print()
        return None

    def __deep(self, node):
        if node is None:
            return None

        self.__deep(node.left)
        print(node.data)
        self.__deep(node.right)

    def deep_search(self):
        self.__deep(self.root)

v = [10, 5, 7, 16, 13, 2, 20, 22, 1, 6, 8, 19]

tr = BTree()
for x in v:
    tr.append(x)
tr.show_tree()
print()
tr.delete(16)
tr.show_tree()
tr.deep_search()