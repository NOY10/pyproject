import math

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
# node0 = TreeNode(3)
# node1 = TreeNode(4)
# node2 = TreeNode(5)
# node0.left = node1
# node0.right = node2
def parse_tuple(data):
    if isinstance(data, tuple) and len(data) == 3:
        node = TreeNode(data[1])
        node.left = parse_tuple(data[0])
        node.right = parse_tuple(data[2])
    elif data is None:
        node = None
    else:
        node = TreeNode(data)
    return node
tree2 = parse_tuple(((1,3,None), 2, ((None, 3, 4), 5, (6, 7, 8))))
print(tree2.key)
print(tree2.left.key, tree2.right.key)
print(tree2.left.left.key, tree2.left.right, tree2.right.left.key, tree2.right.right.key)
print(tree2.right.left.right.key, tree2.right.right.left.key, tree2.right.right.right.key)
def display_keys(node, space='\t', level=0):
    # print(node.key if node else None, level)
    
    # If the node is empty
    if node is None:
        print(space*level + '∅')
        return   
    
    # If the node is a leaf 
    if node.left is None and node.right is None:
        print(space*level + str(node.key))
        return
    
    # If the node has children
    display_keys(node.right, space, level+1)
    print(space*level + str(node.key))
    display_keys(node.left,space, level+1)    
display_keys(tree2, '  ')

def traverse_in_order(node):
    if node==None:
        return []
    return(traverse_in_order(node.left)+[node.key]+ traverse_in_order(node.right))
tree = parse_tuple(((1,3,None), 2, ((None, 3, 4), 5, (6, 7, 8))))
print(traverse_in_order(tree))

def traverse_pre_order(node):
    if node==None:
        return []
    return ([node.key]+traverse_pre_order(node.left)+traverse_pre_order(node.right))
print(traverse_pre_order(tree))

def post_order(node):
    if node==None:
        return []
    return(post_order(node.left)+post_order(node.right)+[node.key])
print(post_order(tree))

def tree_height(node):
    if node ==None:
        return 0
    return 1+max(tree_height(node.left),tree_height(node.right))
print(tree_height(tree))

def tree_size(node):
    if node==None:
        return 0
    return 1+tree_size(node.left)+tree_size(node.right)
print(tree_size(tree))

def min_depth(node):
    if node==None:
        return 0
    if node.left==None and node.right==None:
        return 1
    leftdepth=min_depth(node.left) if node.left!=None else math.inf
    rightdepth=min_depth(node.right) if node.right != None else math.inf

    return 1+min(leftdepth,rightdepth)
print(min_depth(tree))

def diameterofbinarytree(node):
    res=[0]
    def dfs(node):
        if node==None:
            return -1
        left=dfs(node.left)
        right=dfs(node.right)
        res[0]=max(res[0],2+left,right)
        return 1+ max(left,right)
    dfs(node)
    return res[0]

print(diameterofbinarytree(tree))
def remove_none(nums):
    return [x for x in nums if x is not None]

def is_bst(node):
    if node is None:
        return True, None, None
    
    is_bst_l, min_l, max_l = is_bst(node.left)
    is_bst_r, min_r, max_r = is_bst(node.right)
    
    is_bst_node = (is_bst_l and is_bst_r and 
              (max_l is None or node.key > max_l) and 
              (min_r is None or node.key < min_r))
    
    min_key = min(remove_none([min_l, node.key, min_r]))
    max_key = max(remove_none([max_l, node.key, max_r]))
    
    # print(node.key, min_key, max_key, is_bst_node)
        
    return is_bst_node, min_key, max_key     

