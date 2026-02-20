class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

def lowest_common_ancestor(p: 'Node', q: 'Node') -> 'Node':
    """
    Find the lowest common ancestor of two nodes in a binary tree 
    where each node has a pointer to its parent.
    """
    if not p or not q:
        return None

    a, b = p, q

    # This approach mimics finding the intersection of two linked lists.
    # By switching paths, both pointers travel the same total distance:
    # (distance p to LCA + distance q to LCA + distance LCA to root)
    while a != b:
        a = a.parent if a.parent else q
        b = b.parent if b.parent else p

    return a

if __name__ == "__main__":
    # Example Setup:
    #      3
    #     / \
    #    5   1
    #   / \
    #  6   2
    
    root = Node(3)
    node5 = Node(5)
    node1 = Node(1)
    node6 = Node(6)
    node2 = Node(2)

    root.left, root.right = node5, node1
    node5.parent, node1.parent = root, root
    
    node5.left, node5.right = node6, node2
    node6.parent, node2.parent = node5, node5

    # Test Case: LCA of 6 and 2 should be 5
    result = lowest_common_ancestor(node6, node2)
    
    print(f"Input Nodes: {node6.val}, {node2.val}")
    print(f"LCA Output: {result.val if result else 'None'}")