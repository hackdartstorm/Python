import math

def minSpeedOnTime(dist, hour):
    # If it's impossible to cover all trains even at infinite speed
    # (need at least 1 hour per train except the last one)
    if len(dist) - 1 >= hour:
        return -1
    left, right = 1, 10**7
    ans = -1
    while left <= right:
        mid = (left + right) // 2
        # Calculate time taken at speed 'mid'
        time = 0
        for i in range(len(dist) - 1):
            time += (dist[i] + mid - 1) // mid
        # Last train doesn't need to wait for integer hour
        time += dist[-1] / mid
        if time <= hour + 1e-9:
            ans = mid
            right = mid - 1
        else:
            left = mid + 1
    return ans
# Driver code to test locally
if __name__ == "__main__":
    print(minSpeedOnTime([1,3,2], 6))    # Expected: 1
    print(minSpeedOnTime([1,3,2], 2.7))  # Expected: 3
    print(minSpeedOnTime([1,3,2], 1.9))  # Expected: -1