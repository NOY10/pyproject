class treenode:
    def __init__(self,key):
        self.key=key
        self.right=None
        self.left=None
def parse_tuple(data):
    if isinstance(data,tuple) and len(data)==3:
        node=treenode(data[1])
        node.left=parse_tuple(data[0])
        node.right=parse_tuple(data[2])
    elif data is None:
        node=None
    else:
        node=treenode(data)
    return node
def display(node,space='\t',level=0):
    if node is None:
        print(space*level+'*')
        return
    if node.left is None and node.right is None:
        print(space*level+str(node.key))
        return
    display(node.right,space,level+1)
    print(level*space+str(node.key))
    display(node.left,space,level+1)
tree2 = parse_tuple(((1,3,None), 2, ((None, 3, 4), 5, (6, 7, 8))))
def traverse_in_order(node):
    if node == None:
        return []
    return (traverse_in_order(node.left)+[node.key]+traverse_in_order(node.right))
def traverse_pre_order(node):
    if node==None:
        return []
    return ([node.key]+traverse_pre_order(node.left)+traverse_pre_order(node.right))


def post_order(node):
    if node==None:
        return []
    return(post_order(node.left)+post_order(node.right)+[node.key])


display(tree2,' ')






        

    
