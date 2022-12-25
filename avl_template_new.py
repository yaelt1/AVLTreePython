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
        if self.left.height == -1:
            return None
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        if self.right.height == -1:
            return None
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
        self.size = self.right.size + self.left.size +1
        self.height = max(self.right.height, self.left.height)+1
        self.BF =  self.left.height- self.right.height







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
        return self.height != -1




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
        self. max = None


    # add your fields here

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
        if self.empty() or i > self.size or i < 0:
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
        if not 0<= i <= self.size:
            return None
        #creating a node
        new_node = AVLNode(val)
        virtual = AVLNode("None")
        virtual.setHeight(-1)
        virtual.size = 0
        new_node.left = (virtual)
        new_node.right = (virtual)

        if self.empty():
            self.root = new_node
            new_node.parent = None
            self.min = self.max = new_node

        elif i == self.size:
            # max_node = self.max
            max_node = self.find_max(self.getRoot())
            max_node.setRight(new_node)
            self.max = new_node

        else:
            if i==0:
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
            wanted_node = self.select(i + 1)
            cnt = self.delete_node(wanted_node)
            if i==0:
                self.min = self.select(1)
            if i==self.size-1:
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
        # if self.empty():
        #     return None
        # cur_node = self.getRoot()
        # while cur_node.left.isRealNode():
        #     cur_node = cur_node.left
        # return cur_node.value

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        if self.max is not None:
            return self.max.value
        return None
        # if self.empty():
        #     return None
        # cur_node = self.getRoot()
        # while cur_node.right.isRealNode():
        #     cur_node = cur_node.right
        # return cur_node.value

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
                return lst.root.height
        else:
            if lst.empty():
                return self.root.height
        self_height = self.root.height
        lst_height = lst.root.height
        result = abs(self_height - lst_height)
        if self.size == 1:
            self.root.setRight(lst.root)
            self.update_tree(self.root)
            self.rebalance_delete(self.root)
            return result
        x = self.select(self.size)
        self.delete(self.size - 1)
        x.parent = None
        new_self_height = self.root.height
        self.size += lst.size
        if new_self_height < lst_height:
            cur_in_lst = lst.select(1)
            while cur_in_lst.height < self_height - 1:
                cur_in_lst = cur_in_lst.parent
            cur_in_lst.parent.setLeft(x)
            x.setLeft(self.root)
            x.setRight(cur_in_lst)
            self.root = lst.root
            self.update_tree(x)
            self.rebalance_delete(x)
        elif new_self_height == lst_height:
            x.setLeft(self.root)
            x.setRight(lst.root)
            self.root = x
            self.update_tree(x)
        elif new_self_height > lst_height:
            cur_in_self = self.select(1)
            while cur_in_self.height < lst_height - 1:
                cur_in_self = cur_in_self.parent
            cur_in_self.parent.setLeft(x)
            x.setLeft(cur_in_self)
            x.setRight(lst.root)
            self.update_tree(x)
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
    def get_first(self):
        return self.min.value

    def get_last(self):
        return self.max.value

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

    """updates the height and size of all nodes in the tree  

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
    #only for insert
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
                        # self.update_node(node)
                        count += 1
                        return count

                    elif node.left.BF == -1:  # rotate_left_then_right
                        self.rotate_left(node.left)
                        self.rotate_right(node)
                        # self.update_node(node)
                        count += 2
                        return count

                elif node.BF == -2:
                    if node.right.BF == 1:  # rotate_right_then_left
                        self.rotate_right(node.right)
                        self.rotate_left(node)
                        # self.update_node(node)
                        count += 2
                        return count

                    elif node.right.BF == -1:
                        self.rotate_left(node)
                        count += 1
                        return count
                node = parent
        return count

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
        node.setLeft(son.right)
        son.setRight(node)
        # self.update_node(node)

    def rotate_left(self, node):
        son = node.right
        if node.parent is None:
            son.parent = None
        else:
            if node == node.parent.right:
                node.parent.setRight(son)
            else:
                node.parent.setLeft(son)
        node.setRight(son.left)
        son.setLeft(node)
        if son.parent is None:
            self.root = son
        # self.update_node(node)

    def delete_node(self, node):
        parent = node.parent
        self.size -= 1
        if not node.left.isRealNode() and not node.right.isRealNode(): #if node is leaf we just remove it
            if node == parent.left:
                parent.setLeft(node.left)
            elif node == parent.right:
                parent.setRight(node.right)
            #self.update_tree(parent)
            return self.rebalance_delete(parent)

        elif not node.left.isRealNode(): #has a right son
            if node.parent is None:
                self.root = node.right
                node.right.parent = None
                self.update_node(node.right)
                return self.rebalance_delete(node.right)

            elif node == parent.left:
                parent.setLeft(node.right)
            elif node == parent.right:
                parent.setRight(node.right)
            #self.update_node(parent)
            return self.rebalance_delete(parent)

        elif not node.right.isRealNode():
            if node.parent is None:
                self.root = node.left
                node.left.parent = None
                self.update_node(node.left)
                return self.rebalance_delete(node.left)

            elif node == parent.left:
                parent.setLeft(node.left)
            elif node == parent.right:
                parent.setRight(node.left)
            # self.update_node(parent)
            return self.rebalance_delete(parent)
        else:
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

                    # self.update_node(node.parent)

                elif node.BF == -2:
                    self.update_node(node.right)
                    if node.right.BF == 1:  # rotate_right_then_left
                        self.rotate_right(node.right)
                        self.rotate_left(node)
                        count += 2

                    elif node.right.BF == -1 or node.right.BF == 0:
                        self.rotate_left(node)
                        count += 1
                    # self.update_tree(node.parent)
                node = node.parent
        return count

    def merge_sort(self, lst):
        len_lst = len(lst)
        if len_lst <= 1:
            return lst
        else:
            lst1 = self.merge_sort(lst[:(len_lst // 2)])
            lst2 = self.merge_sort(lst[(len_lst // 2):])
        return self.merge(lst1, lst2)

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

    def append(self, val):
        self.insert(self.length(), val)

    def getTreeHeight(self):
        return self.root.height




def test_delete():
    print("delete")
    new_tree = AVLTreeList()
    lst1 = []
    for j in range(50):
        index = random.randint(0, new_tree.size)
        new_tree.insert(index, str(j))
        lst1.insert(index, str(j))
    new_tree.delete(10)
    lst1.pop(10)
    new_tree.delete(0)
    lst1.pop(0)
    new_tree.delete(-2)
    new_tree.delete(15)
    lst1.pop(15)
    new_tree.delete(70)
    new_tree.delete(4)
    lst1.pop(4)
    for i in range(46):
        index = random.randint(0, new_tree.size-1)
        new_tree.delete(index)
        lst1.pop(index)
        if lst1 != new_tree.listToArray():
            print ("problem")
# print( test_delete())

def test_insert():
    print("insert")
    new_tree = AVLTreeList()
    for j in range(10):
        index = random.randint(0, new_tree.size)
        new_tree.insert(index, str(j))
    new_tree.insert(0, "A")
    new_tree.insert(5, "B")
    new_tree.insert(20, "C")
    print(new_tree.listToArray())
    print(new_tree.sort().listToArray())
    print(new_tree.permutation().listToArray())
# print( test_insert())

def list_bf(tree):
    if tree.empty():
        return []
    help_stack = []
    result = []
    cur_node = tree.root
    while cur_node.isRealNode() or help_stack != []:
        while cur_node.isRealNode():
            help_stack.append(cur_node)
            cur_node = cur_node.left
        cur_node = help_stack.pop()
        result.append(cur_node.BF)
        cur_node = cur_node.right
    return result

def chek_bf(tree):
    bf_list = list_bf(tree)
    for i in range(len(bf_list)):
        if bf_list[i]==2 or bf_list[i]==-2:
            return ("problem with node om index ",i )
    return "done"


def test2():
    new_tree = AVLTreeList()
    print(new_tree.last())
    print(new_tree.first())
    a = new_tree.insert(0, "2")
    b = new_tree.insert(1, "4")
    c = new_tree.insert(2, "8")
    d = new_tree.insert(3, "9")
    e = new_tree.insert(4, "11")
    f = new_tree.insert(5, "12")
    g = new_tree.insert(6, "13")
    h = new_tree.insert(7, "15")
    i = new_tree.insert(8, "18")
    j = new_tree.insert(9, "20")
    k = new_tree.insert(10, "22")
    l = new_tree.insert(11, "24")
    print(new_tree.last())
    print(new_tree.first())
    tree1 = new_tree.permutation()
    tree2 = new_tree.sort()
    m = new_tree.delete(11)
    n = new_tree.delete(9)
    o = new_tree.delete(3)
    p = new_tree.delete(7)
    d = new_tree.delete(5)
    print(new_tree.last())
    print(new_tree.first())
    total = 0
    n= new_tree.size
    for j in range(n):
        index = random.randint(0, new_tree.size - 1)
        # print("in" , index)
        # print("val", new_tree.retrieve(index))
        total += new_tree.delete(index)
    new_tree.delete(3)
    new_tree.delete(0)
    new_tree.delete(9)
    new_tree.delete(2)
    new_tree.delete(7)

    self = AVLTreeList()
    q = self.insert(0, "A")
    r = self.insert(1, "B")
    s = self.insert(2, "C")
    print(self.concat(new_tree))
    print(self.listToArray())
    print(self.size)
    print(self.search("13"))



def exp1(i):
    new_tree = AVLTreeList()
    total_insert = 0
    total_both = 0
    lst1 = []
    n = i
    for j in range(n//2):
        index = random.randint(0, new_tree.size)
        new_tree.insert(index, str(j))
    print(chek_bf(new_tree))
    for j in range(n//4):
        if j%2 ==0:
            index = random.randint(0, new_tree.size - 1)
            total_both += new_tree.delete(index)
        else:
            index = random.randint(0, new_tree.size)
            new_tree.insert(index, str(j))
    chek_bf(new_tree)

print(exp1(100))

