#!/usr/bin/env python3

MOD = 1000000007

def remove_k(num, k):
    s = str(num)
    result = ''.join(c for c in s if c != str(k))
    return int(result) if result else 0

def brute_force(k, n):
    total = 0
    for i in range(1, n + 1):
        val = remove_k(i, k)
        print(f"f({i}) = {val}")
        total = (total + val) % MOD
    return total

# 작은 케이스 테스트
print("k=3, n=5:")
result = brute_force(3, 5)
print(f"Total: {result}")

print("\nk=3, n=20:")
result = brute_force(3, 20)
print(f"Total: {result}")