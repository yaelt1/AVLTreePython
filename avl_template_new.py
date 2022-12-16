# username -
# id1      - 207829805
# name1    - Yael Tzur
# id2      - 209513910
# name2    - Noa Malka



"""A class represnting a node in an AVL tree"""


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
		self.size = 1
		self.height = 0 # Balance factor*


	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	"""
	def getLeft(self):
		if self.left.height == -1 :
			return None
		return self.left


	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	"""
	def getRight(self):
		if self.right.height == -1 :
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
		if node.size != -1:
			self.size+=1
			self.height+=1


	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.right = node
		node.parent = self
		if node.size != -1:
			self.size += 1
			self.height -= 1

	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		parent = node
		if node is not None:
			self.parent = parent
			if self.value > node.value:
				parent.setRight(self)
			else:
				parent.setLeft(self)


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
		return self.size != -1



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
		# add your fields here


	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return (self.size ==0)


	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		wanted_node = self.select( i+1)
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
		new_node = AVLNode(val)
		virtual = AVLNode("None")
		virtual.size = -1
		new_node.setLeft(virtual)
		new_node.setRight(virtual)
		if self.empty():
			self.root = new_node
		if i == self.size:
			max_1 = self.find_max_node(self.getRoot())
			max_1.setRight(new_node)
		else:
			curr = self.select(i+1)
			if not curr.left.isRealNode():
				curr.setLeft(new_node)
			else:
				pre = self.predecessor(curr)
				pre.setRight(new_node)
		self.size += 1
		if self.size>2:
			self.update_size(new_node.parent.parent)
			self.update_height(new_node.parent.parent)
		return self.rebalance(new_node.parent)


	"""" returns number of rotations until balanced tree
				@type node : AVLNode
				@rtype : int
				"""
	def rebalance(self,node):
		if self.size >2:
			cnt = 0
			while node.height != 0:
				if abs(node.height) == 1:
					node = node.parent
				if node.height == 2:
					son = node.left
					if son.height ==1:
						self.right_rotation(node)
						cnt +=1
					elif son.height ==-1:
						self.left_rotation(node.left)
						self.right_rotation(node)
						cnt += 2
				elif node.height == -2:
					son = node.right
					if son.height == 1:
						self.right_rotation(node.right)
						self.left_rotation(node)
						cnt += 2
					elif son.height == -1:
						self.left_rotation(node)
						cnt += 1
			return cnt

	def right_rotation(self , node):
		son = node.left
		son.setParent(node.parenrt)
		son.setRight(node)

	def left_rotation(self , node):
		son = node.right
		son.setParent(node.parenrt)
		son.setLeft(node)

	"""updates the heights of nodes after inserting/deleting
		@type node: AVLNode
		"""
	def update_tree(self, node):
		size = 0
		while node is not None:
			if node.right.isRealNode():
				node.height -= node.right.height
				size += node.right.size
			if node.left.isRealNode():
				node.height += node.left.height
				size += node.left.size
			node = node.parent

	"""updates the sizes of nodes after inserting/deleting
			@type node: AVLNode
			"""



	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		node = self.select(i+1)

		return -1


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		if self.empty():
			return None
		curr = self.getRoot()
		while curr.left is not None:
			curr = curr.left
		curr = curr.parent
		return curr.value


	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		if self.empty():
			return None
		curr = self.getRoot()
		while curr.right is not None:
			curr = curr.right
		curr = curr.parent
		return

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		return None

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
		return None

	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		return None

	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		return None

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		return None



	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		return self.root


	"""" returns the node with rank i in the tree
		@type i: int
		@rtype: AVLNode
		"""
	def select(self, i):
		node = self.getRoot()
		return self.select_rec(node, i)

	def select_rec(self, node, i):

		curr = node
		if curr.right.size == -1:
			rank_curr = curr.size
		else:
			rank_curr = curr.size - curr.right.size

		if rank_curr < i:
			curr = curr.right
			i = i - rank_curr
			return self.select_rec(curr, i)
		elif rank_curr > i:
			curr = curr.left
			return self.select_rec(curr, i)
		elif rank_curr == i:
			return(curr)

	"""" returns the node with max value in the giving node's subtree 
			@type node : AVLNode
			@rtype : AVLNode
			"""
	def find_max_node(self, node):
		curr = node
		while curr.right is not None:
			curr = curr.right
		if curr == node:
			return curr
		return curr.parent

	"""" returns the previous node of the giving node
				@type node : AVLNode
				@rtype : AVLNode
				"""

	def predecessor(self, node):
		if node.left is not None:
			return self.find_max_node(node.left)
		parent = node.parent
		if node == parent.right:
			return parent
		while parent is not None and node == parent.left:
			node = parent
			parent = node.parent
		return parent





