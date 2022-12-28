# username - complete info
# id1      - 207829805
# name1    - Yael Tzur
# id2      - 209513910
# name2    - Noa Malka


"""A class represnting a node in an AVL tree"""
import random


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0
        self.size = 1
        self.BF = 0  # Balance factor

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node
        node.parent = self
        self.size = self.right.size + self.left.size + 1
        self.height = max(self.right.height, self.left.height) + 1
        self.BF = self.left.height - self.right.height

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node
        node.parent = self
        self.size = self.right.size + self.left.size + 1
        self.height = max(self.right.height, self.left.height) + 1
        self.BF = self.left.height - self.right.height

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        return self.height != -1 or self is None


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):
        self.size = 0
        self.root = None
        self.min = None
        self.max = None

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.size == 0

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i):
        if self.empty() or i >= self.size or i < 0:
            return None
        wanted_node = self.select(i + 1)
        return wanted_node.value

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        if not 0 <= i <= self.size:
            return None
        # creating a node
        new_node = AVLNode(val)
        self.virtual_sons(new_node)

        if self.empty():
            self.root = new_node
            new_node.parent = None
            self.min = self.max = new_node

        elif i == self.size:
            max_node = self.max
            max_node.setRight(new_node)
            self.max = new_node

        else:
            if i == 0:
                self.min = new_node

            cur_node = self.select(i + 1)
            if not cur_node.left.isRealNode():
                cur_node.setLeft(new_node)
            else:
                pre = self.predecessor(cur_node)
                pre.setRight(new_node)

        self.size += 1
        cnt = self.rebalance(new_node.parent)
        self.update_tree(new_node)
        return cnt

    """deletes the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        if self.empty() or i < 0 or i >= self.size:
            return -1
        if self.size == 1 and i == 0:
            self.root = None
            self.size = 0
            self.min = None
            self.max = None
            return 0
        else:
            prev = self.size
            wanted_node = self.select(i + 1)
            cnt = self.delete_node(wanted_node)

            if i == 0:
                self.min = self.select(1)
            if i == prev - 1:
                self.max = self.select(self.size)
            return cnt

    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        if self.min is not None:
            return self.min.value
        return None

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        if self.max is not None:
            return self.max.value
        return None

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        if self.empty():
            return []
        help_stack = []
        result = []
        cur_node = self.root
        while cur_node.isRealNode() or help_stack != []:
            while cur_node.isRealNode():
                help_stack.append(cur_node)
                cur_node = cur_node.left
            cur_node = help_stack.pop()
            result.append(cur_node.value)
            cur_node = cur_node.right
        return result

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.size

    """sort the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are sorted by the info of the original list.
    """

    def sort(self):
        lst = self.listToArray()
        sorted_lst = self.merge_sort(lst)
        new_tree = AVLTreeList()
        for i in range(len(sorted_lst)):
            new_node = AVLNode(sorted_lst[i])
            new_tree.insert(i, new_node.value)
        return new_tree

    """permute the info values of the list

    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    """

    def permutation(self):
        order_lst = self.listToArray()
        new_tree = AVLTreeList()
        for i in range(self.size):
            index = random.randint(0, len(order_lst) - 1)
            cur = order_lst.pop(index)
            new_node = AVLNode(cur)
            new_tree.insert(i, new_node.value)
        return new_tree

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        if self.empty():
            if lst.empty():
                return 0
            else:
                self.root = lst.root
                self.min = lst.min
                self.max = lst.max
                self.size += lst.size
                return lst.root.height
        else:
            if lst.empty():
                return self.root.height

        self_height = self.root.height
        lst_height = lst.root.height
        result = abs(self_height - lst_height)
        if self.size == 1:
            self.root.setRight(lst.root)
            self.max = lst.max
            self.update_node(self.root)
            self.rebalance_delete(self.root)
            return result

        x = self.max
        self.delete(self.size - 1)
        x.parent = None

        # after deleting x
        new_self_height = self.root.height
        self.size += lst.size + 1

        # if self is the smaller tree
        if new_self_height < lst_height:
            cur_in_lst = lst.min
            while cur_in_lst.height < self_height:
                cur_in_lst = cur_in_lst.parent

            # height of cur_in_lst == self_height
            if cur_in_lst.parent is not None:
                cur_in_lst.parent.setLeft(x)
            else:
                lst.root = x

            x.setLeft(self.root)
            x.setRight(cur_in_lst)
            self.root = lst.root
            self.max = lst.max
            self.rebalance_delete(x)

        elif new_self_height == lst_height:
            x.setLeft(self.root)
            x.setRight(lst.root)
            self.root = x
            self.max = lst.max
            self.update_node(x)

        elif new_self_height > lst_height:
            cur_in_self = self.max
            while cur_in_self.height < lst_height:
                cur_in_self = cur_in_self.parent

            if cur_in_self.parent is not None:
                cur_in_self.parent.setRight(x)
            else:
                self.root = x

            x.setLeft(cur_in_self)
            x.setRight(lst.root)
            self.max = lst.max
            self.update_node(x)
            self.rebalance_delete(x)
        return result

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        lst = self.listToArray()
        for i in range(len(lst)):
            if lst[i] == val:
                return i
        return -1

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return self.root

    # aid functions

    """returns the node with rank i in the AVLtree

    @type i int
    @rtype: AVLNode

    """

    def select(self, i):
        root = self.getRoot()
        return self.select_rec(root, i)

    def select_rec(self, node, i):
        cur_node = node
        if cur_node.right is None or not cur_node.right.isRealNode():
            rank_cur = cur_node.size
        else:
            rank_cur = cur_node.size - cur_node.right.size
        if rank_cur == i:
            return cur_node
        elif rank_cur < i:
            return self.select_rec(cur_node.right, i - rank_cur)
        elif rank_cur > i:
            return self.select_rec(cur_node.left, i)

    """returns the node with the maximum rank in the given node's subTree 

    @:type node: AVLNode
    @rtype: AVLNode
    """

    def find_max(self, node):
        cur_node = node
        while cur_node.right.isRealNode():
            cur_node = cur_node.right
        return cur_node

    """returns the previous node of the given node

    @:type node: AVLNode
    @rtype: AVLNode
    """

    def predecessor(self, node):
        if node.left.isRealNode():
            return self.find_max(node.left)
        else:
            parent = node.parent
            if node == parent.right:
                return parent
            while parent is not None and node == parent.left:
                node = parent
                parent = node.parent
            return parent

    """updates the height, size and BF of the given node  

    @:type node: AVLNode
    """

    def update_node(self, node):
        size = 0
        if node is not None:
            if node.right.isRealNode():
                size += node.right.size
            if node.left.isRealNode():
                size += node.left.size
            node.size = size + 1
            node.height = max(node.right.height, node.left.height) + 1
            node.BF = node.left.height - node.right.height

    """updates the height, size and BF of all nodes in the tree  

    @:type node: AVLNode
    """

    def update_tree(self, node):
        while node is not None:
            size = 0
            if node.right.isRealNode():
                size += node.right.size
            if node.left.isRealNode():
                size += node.left.size
            node.size = size + 1
            node.height = max(node.right.height, node.left.height) + 1
            node.BF = node.left.height - node.right.height
            node = node.parent
        return None

    """returns the number of rotation needed to balance the AVLTree

    @:type node: AVLNode
    @rtype: int
    """

    # only for insert
    def rebalance(self, node):
        count = 0
        if self.size > 2:
            self.update_node(node)
            while node is not None and node.BF != 0:
                parent = node.parent
                self.update_node(parent)
                if node.BF == 2:
                    if node.left.BF == 1:
                        self.rotate_right(node)
                        count += 1
                        return count

                    elif node.left.BF == -1:  # rotate_left_then_right
                        self.rotate_left(node.left)
                        self.rotate_right(node)
                        count += 2
                        return count

                elif node.BF == -2:
                    if node.right.BF == 1:  # rotate_right_then_left
                        self.rotate_right(node.right)
                        self.rotate_left(node)
                        count += 2
                        return count

                    elif node.right.BF == -1:
                        self.rotate_left(node)
                        count += 1
                        return count
                node = parent
        return count

    """makes a right rotation

    @:type node: AVLNode
    """

    def rotate_right(self, node):
        son = node.left
        if node.parent is None:
            son.parent = None
            self.root = son

        else:
            if node == node.parent.right:
                node.parent.setRight(son)
            else:
                node.parent.setLeft(son)
        right = son.right
        son.setRight(node)
        node.setLeft(right)

        """makes a left rotation

        @:type node: AVLNode
        """

    def rotate_left(self, node):
        son = node.right
        if node.parent is None:
            son.parent = None
            self.root = son
        else:
            if node == node.parent.right:
                node.parent.setRight(son)
            else:
                node.parent.setLeft(son)
        left = son.left
        son.setLeft(node)
        node.setRight(left)

        """deletes the given node

        @:type node: AVLNode
        @returns: the number of rebalancing operation due to AVL rebalancing
        """

    def delete_node(self, node):
        parent = node.parent
        self.size -= 1
        if not node.left.isRealNode() and not node.right.isRealNode():  # if node is leaf we just remove it
            if node == parent.left:
                parent.setLeft(node.left)
            elif node == parent.right:
                parent.setRight(node.right)
            return self.rebalance_delete(parent)

        elif not node.left.isRealNode():  # only right son
            if node.parent is None:
                self.root = node.right
                node.right.parent = None
                self.update_node(node.right)
                return self.rebalance_delete(node.right)

            elif node == parent.left:
                parent.setLeft(node.right)
            elif node == parent.right:
                parent.setRight(node.right)
            return self.rebalance_delete(parent)

        elif not node.right.isRealNode(): # only left son
            if node.parent is None:
                self.root = node.left
                node.left.parent = None
                self.update_node(node.left)
                return self.rebalance_delete(node.left)

            elif node == parent.left:
                parent.setLeft(node.left)
            elif node == parent.right:
                parent.setRight(node.left)
            return self.rebalance_delete(parent)
        else:                                          # two sons
            successor = self.find_min(node.right)
            successor_parent = successor.parent
            successor.setLeft(node.left)
            if successor.parent != node:
                successor.parent.setLeft(successor.right)
                successor.setRight(node.right)
            if node.parent is None:
                successor.parent = None
                self.root = successor
                if successor_parent != node:
                    self.update_node(successor_parent)
                    return self.rebalance_delete(successor_parent)
                else:
                    self.update_node(successor)
                    return self.rebalance_delete(successor)

            if node == node.parent.left:
                node.parent.setLeft(successor)
            if node == node.parent.right:
                node.parent.setRight(successor)
            if successor_parent != node:
                self.update_node(successor_parent)
                return self.rebalance_delete(successor_parent)
            else:
                self.update_node(successor)
                return self.rebalance_delete(successor)

    """returns the node with the minimum rank in the given node's subTree 

    @:type node: AVLNode
    @rtype: AVLNode
    """

    def find_min(self, node):
        cur_node = node
        while cur_node.left.isRealNode():
            cur_node = cur_node.left
        return cur_node

    """returns the number of rotation needed to balance the AVLTree after delete

    @:type node: AVLNode
    @rtype: int
    """

    def rebalance_delete(self, node):
        count = 0
        if self.size > 2:
            while node is not None:
                self.update_node(node)
                if node.BF == 2:
                    self.update_node(node.left)
                    if node.left.BF == 1 or node.left.BF == 0:
                        self.rotate_right(node)
                        count += 1
                    elif node.left.BF == -1:  # rotate_left_then_right
                        self.rotate_left(node.left)
                        self.rotate_right(node)
                        count += 2

                elif node.BF == -2:
                    self.update_node(node.right)
                    if node.right.BF == 1:  # rotate_right_then_left
                        self.rotate_right(node.right)
                        self.rotate_left(node)
                        count += 2

                    elif node.right.BF == -1 or node.right.BF == 0:
                        self.rotate_left(node)
                        count += 1
                node = node.parent
        return count

    """sort the lists by value using recursive calls
    
    @type: list
    @rtype: list
    @returns:sorted list.
    """
    def merge_sort(self, lst):
        len_lst = len(lst)
        if len_lst <= 1:
            return lst
        else:
            lst1 = self.merge_sort(lst[:(len_lst // 2)])
            lst2 = self.merge_sort(lst[(len_lst // 2):])
        return self.merge(lst1, lst2)

    """merge two sorted lists into one sorted list

    @type: list
    @rtype: list
    @returns: sorted list
    """

    def merge(self, A, B):
        len_A = len(A)
        len_B = len(B)
        result = [None for i in range(len_A + len_B)]
        a = b = c = 0
        while a < len_A and b < len_B:
            if A[a] < B[b]:
                result[c] = A[a]
                a += 1
            else:
                result[c] = B[b]
                b += 1
            c += 1
        if a == len_A:
            while b < len_B:
                result[c] = B[b]
                b += 1
                c += 1
        else:
            while a < len_A:
                result[c] = A[a]
                a += 1
                c += 1
        return result

    """creates two virtual sons for the node received
        @type node: AVLNode 
        """
    def virtual_sons(self, node):
        #left virtual son
        v1 = AVLNode(None)
        v1.setHeight(-1)
        v1.size = 0
        # right virtual son
        v2 = AVLNode(None)
        v2.setHeight(-1)
        v2.size = 0
        node.right = v2
        node.left = v1
        v1.setParent(node)
        v2.setParent(node)

