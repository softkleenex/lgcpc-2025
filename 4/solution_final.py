import sys
input = sys.stdin.readline
from collections import deque

n = int(input())
a = [0] * (n+1)
b = [0] * (n+1)

for i in range(1, n+1):
    a[i], b[i] = map(int, input().split())

g = [[] for _ in range(n+1)]
for _ in range(n-1):
    u, v, w = map(int, input().split())
    g[u].append((v, w))
    g[v].append((u, w))

def bfs(s):
    d = [-1] * (n+1)
    d[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v, w in g[u]:
            if d[v] == -1:
                d[v] = d[u] + w
                q.append(v)
    return d

cov = [0] * (n+1)
for i in range(1, n+1):
    d = bfs(i)
    for j in range(1, n+1):
        if d[j] <= b[i]:
            cov[i] |= (1 << (j-1))

if n <= 20:
    dp = [10**18] * (1 << n)
    dp[0] = 0
    
    for m in range(1 << n):
        if dp[m] == 10**18:
            continue
        for i in range(1, n+1):
            nm = m | cov[i]
            dp[nm] = min(dp[nm], dp[m] + a[i])
    
    print(dp[(1 << n) - 1])
else:
    cur = 0
    res = 0
    use = [0] * (n+1)
    
    for i in range(1, n+1):
        if a[i] == 0:
            cur |= cov[i]
            use[i] = 1
    
    while cur != (1 << n) - 1:
        best = -1
        best_val = 0
        
        for i in range(1, n+1):
            if use[i]:
                continue
            
            cnt = 0
            for j in range(n):
                if not (cur & (1 << j)) and (cov[i] & (1 << j)):
                    cnt += 1
            
            if cnt > 0:
                val = cnt / max(a[i], 1)
                if val > best_val:
                    best_val = val
                    best = i
        
        if best == -1:
            break
        
        res += a[best]
        cur |= cov[best]
        use[best] = 1
    
    print(res)