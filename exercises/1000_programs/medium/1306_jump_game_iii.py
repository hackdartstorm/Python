def can_reach(arr: list[int], start: int) -> bool:
    # 1. Initialize the queue with our starting position
    queue = [start]
    # 2. Keep track of visited indices so we don't get stuck in a loop
    visited = set()
    
    while queue:
        # Get the current position
        curr = queue.pop(0)
        
        # SUCCESS: We found a zero!
        if arr[curr] == 0:
            return True
            
        # Mark current as visited
        visited.add(curr)
        
        # Calculate possible jumps
        for next_pos in [curr + arr[curr], curr - arr[curr]]:
            # Check if the jump is within the array bounds and not visited
            if 0 <= next_pos < len(arr) and next_pos not in visited:
                queue.append(next_pos)
                
    # If the queue is empty and we never hit 0, it's impossible
    return False

# --- Test Cases ---
if __name__ == "__main__":
    # Test 1: Should be True (can reach index 5 or 6)
    print(f"Test 1: {can_reach([4, 2, 3, 0, 3, 1, 2], 5)}")
    
    # Test 2: Should be True (start is already 0)
    print(f"Test 2: {can_reach([4, 2, 3, 0, 3, 1, 2], 0)}")
    
    # Test 3: Should be False (cannot reach 0)
    print(f"Test 3: {can_reach([3, 0, 2, 1, 2], 2)}")