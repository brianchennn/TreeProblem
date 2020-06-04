import copy
from typing import Optional, Callable, TypeVar, Generic
'''origin
from Trees.src.errors import MissingValueError, EmptyTreeError
from Trees.src.nodes.bst_node import BSTNode'''
# mine
from bst_node import BSTNode
from errors import MissingValueError, EmptyTreeError
#from bst_node import BSTNode
#from errors import MissingValueError, EmptyTreeError
T = TypeVar('T')
K = TypeVar('K')


class BST(Generic[T, K]):
    """
    T: The value stored in the node
    K: The value used in comparing nodes
    """
    
    def __init__(self, root: Optional[BSTNode[T]] = None, key: Callable[[T], K] = lambda x: x) -> None :
        """
        You must have at least one member named root

        :param root: The root node of the tree if there is one.
        If you are provided a root node don't forget to count how many nodes are in it
        :param key: The function to be applied to a node's value for comparison purposes.
        It serves the same role as the key function in the min, max, and sorted builtin
        functions
        """
        
        self.len = 1
        self.key = key
        self.root = root
        ...

    @property
    def height(self)-> int:
        """
        Compute the height of the tree. If the tree is empty its height is -1
        :return:
        """
        return self.my_height(self.root)
        ...
    def my_height(self,x: BSTNode[T])-> int:
        
        if(x==None):
            return 0
        if(x.right==None and x.left==None):
            return 1
        elif(x.right==None):
            return self.my_height(x.left)+1
        elif(x.left==None):
            return self.my_height(x.right)+1
        else:
            return max(self.my_height(x.left),self.my_height(x.right))+1 
            
    def __len__(self) -> int:
        """
        :return: the number of nodes in the tree
        """
        return len
        ...

    def add_value(self, value: T) -> None:
        """
        Add value to this BST
        Duplicate values should be placed on the right
        :param value:
        :return:
        """
        self.len+=1
        z = BSTNode(value)
        y = None
        x = self.root
        while(x!=None):
            y = x
            if(z.value < x.value):
                x = x.left
            else:
                x = x.right
        z.parent = y
        if(y == None):
            self.root = z
        elif (z.value < y.value):
            y.left = z
        else:
            y.right = z
        ...

    def get_node(self, value: K) -> BSTNode[T]:
        """
        Get the node with the specified value
        :param value:
        :raises MissingValueError if there is no node with the specified value
        :return:
        """
        
        x = self.tree_search(self.root,value)
        if(x==None):
            raise MissingValueError()
            return None
        else:
            return x
            
        ...
    def tree_search(self, x: BSTNode[T], value: K)-> T:
        
        if(x == None or value ==x.value):
            return x
        if(value < x.value):
            if(x.left==None):
                raise MissingValueError("f")
                return None
            else:
                return self.tree_search(x.left,value)
        else:
            if(x.right==None):
                raise MissingValueError("f")
                return None
            else:
                return self.tree_search(x.right,value)
    def get_max_node(self) -> BSTNode[T]:
        """
        Return the node with the largest value in the BST
        :return:
        :raises EmptyTreeError if the tree is empty
        """
       
        return self.tree_maximum(self.root)
        ...

    def get_min_node(self) -> BSTNode[T]:
        """
        Return the node with the smallest value in the BST
        :return:
        """
        return self.tree_minimum(self.root)
        
        ...
    def tree_minimum(self,x: BSTNode[T]) -> BSTNode[T]:
        
        if(x == None):
            raise EmptyTreeError("e")
            return None
        else:
            while(x.left!=None):
                x = x.left
            return x
    def tree_maximum(self,x: BSTNode[T]) -> BSTNode[T]:
        
        if(x == None):
            raise EmptyTreeError("e")
        else:
            while(x.right!=None):
                x = x.right
            return x
    def successor(self,x:BSTNode[T]) -> BSTNode[T]:
        
        if(x == None):
            raise EmptyTreeError()
            return None
        else:
           
            if(x.right!=None):
                
                return self.tree_minimum(x.right)
            y = x.parent
            while(y!=None and x==y.right):
                x = y
                y = y.parent
            return y

    def predeccessor(self,x:BSTNode[T]) -> BSTNode[T]:
        if(x == None):
            EmptyTreeError("e")
        else:
            if(x.left!=None):
                return self.tree_maximum(x.left)
            y = x.parent
            while(y!=None and x==y.left):
                x = y
                y = y.parent
            return y    
    def remove_value(self, value: K) -> None:
        """
        Remove the node with the specified value.
        When removing a node with 2 children take the successor for that node
        to be the largest value smaller than the node (the max of the
        left subtree)
        :param value:
        :return:
        :raises MissingValueError if the node does not exist
        """
        try:
            self.len-=1
            z = self.get_node(value)
            if(z==None):
                raise MissingValueError("Miss")
                return
            if(z.left == None or z.right==None):
                y = z
            else:
                y = successor(z)
            if(y.left!=None):
                x = y.left
            else:
                x = y.right
            if(x!=None):
                x.parent = y.parent
            if(y.parent == None):
                self.root = x
            elif(y == y.parent.left):
                y.parent.left = x
            else:
                y.parent.right = x
            if(y!=z):
                z.value = y.value   
        except MissingValueError:
            pass 
        ...

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        elif isinstance(other, BST):
            if len(self) == 0 and len(other) == 0:
                return True
            else:
                return len(self) == len(other) and self.root.value == other.root.value and \
                       BST(self.root.left) == BST(other.root.left) and \
                       BST(self.root.right) == BST(other.root.right)
        else:
            return False

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __deepcopy__(self, memodict) -> "BST[T,K]":
        """
        I noticed that for some tests deepcopying didn't
        work correctly until I implemented this method so here
        it is for you
        :param memodict:
        :return:
        """
        new_root = copy.deepcopy(self.root, memodict)
        new_key = copy.deepcopy(self.key, memodict)
        return BST(new_root, new_key)


node1 = BSTNode('c')
node2 = BSTNode('t')
node3 = BSTNode('a')
node4 = BSTNode('y')
tree = BST(node1,5)
tree.add_value('w')
tree.remove_value('4')
tree.add_value('q')
tree.add_value('m')
tree.add_value('s')
tree.add_value('z')
tree.add_value('o')
tree.add_value('1')
tree.add_value('2')
tree.add_value('4')
tree.add_value('3')
tree.add_value('0')
tree.remove_value('4')
tree.add_value('T')
x = tree.get_min_node()
print(x.value)
y = tree.successor(x)
print(y.value)
y = tree.successor(y)
print(y.value)
y = tree.successor(y)
print(y.value)
y = tree.successor(y)
print(y.value)
y = tree.successor(y)
print(y.value)
y = tree.successor(y)
print(y.value)
y = tree.successor(y)
print(y.value)
y = tree.successor(y)
print(y.value)
y = tree.successor(y)
print(y.value)
print("---")

print(tree.get_max_node().value)
print(tree.height)


