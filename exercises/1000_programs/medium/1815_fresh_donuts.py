from functools import lru_cache

def max_happy_groups(batch_size, groups):
    # Time Complexity: O(k^m) where k is batch_size and m is number of groups
    # Space Complexity: O(batch_size)
    
    # 1. Simplify groups by taking modulo
    remainder_counts = [0] * batch_size
    happy_groups = 0
    
    for g in groups:
        rem = g % batch_size
        if rem == 0:
            happy_groups += 1
        else:
            remainder_counts[rem] += 1
            
    # 2. Match complements (e.g., remainder 1 and batch_size-1)
    for i in range(1, batch_size // 2 + 1):
        if i == batch_size - i:
            happy_groups += remainder_counts[i] // 2
            remainder_counts[i] %= 2
        else:
            pairs = min(remainder_counts[i], remainder_counts[batch_size - i])
            happy_groups += pairs
            remainder_counts[i] -= pairs
            remainder_counts[batch_size - i] -= pairs

    # 3. DFS to optimize remaining groups
    @lru_cache(None)
    def dfs(current_rem, counts):
        max_val = 0
        total_remaining = sum(counts)
        
        if total_remaining == 0:
            return 0
            
        for i in range(1, batch_size):
            if counts[i] > 0:
                # Create a new tuple state with counts[i] decremented, avoiding list conversion
                new_counts = counts[:i] + (counts[i] - 1,) + counts[i + 1:]
                
                is_happy = 1 if current_rem == 0 else 0
                res = is_happy + dfs((current_rem + i) % batch_size, new_counts)
                max_val = max(max_val, res)
                
        return max_val

    happy_groups += dfs(0, tuple(remainder_counts))
    return happy_groups

# Driver Code
if __name__ == "__main__":
    print(f"Test 1: {max_happy_groups(3, [1, 2, 3, 4, 5, 6])}") # Expected: 4
    print(f"Test 2: {max_happy_groups(4, [1, 3, 2, 5, 2, 2, 1, 6])}") # Expected: 4