#!/usr/bin/env python3

def f(x, k):
    s = str(x)
    r = ''.join(c for c in s if c != str(k))
    return int(r) if r else 0

# k=5, N=10 검증
print("k=5, N=10:")
total = 0
for i in range(1, 11):
    val = f(i, 5)
    total += val
    print(f"  f({i}) = {val}, 누적={total}")
print(f"답: {total}\n")

# k=9, N=10 검증  
print("k=9, N=10:")
total = 0
for i in range(1, 11):
    val = f(i, 9)
    total += val
    print(f"  f({i}) = {val}, 누적={total}")
print(f"답: {total}")