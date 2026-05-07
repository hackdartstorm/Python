def hasPathSum(root, targetSum):
    """
    Determine if tree has root-to-leaf path with target sum.
    This logic is fundamental for Decision Trees in Machine Learning.
    """
    # Base Case: Agar tree khali hai
    if not root:
        return False
    
    # Check if we are at a leaf node (node with no children)
    if not root.left and not root.right:
        # Check if the remaining sum matches the current node's value
        return root.val == targetSum
    
    # Recursive step: Subtract current node's value from targetSum
    # and search in children subtrees
    remaining_sum = targetSum - root.val
    
    return hasPathSum(root.left, remaining_sum) or hasPathSum(root.right, remaining_sum)