import sys
input = sys.stdin.readline
from heapq import heappush, heappop

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

def dist_from(s):
    d = [10**18] * (n+1)
    d[s] = 0
    q = [(0, s)]
    while q:
        cd, u = heappop(q)
        if cd > d[u]: continue
        for v, w in g[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                heappush(q, (d[v], v))
    return d

cov = [[] for _ in range(n+1)]
for i in range(1, n+1):
    d = dist_from(i)
    for j in range(1, n+1):
        if d[j] <= b[i]:
            cov[i].append(j)

if n <= 20:
    ans = 10**18
    for mask in range(1, 1<<n):
        cost = 0
        vis = [0] * (n+1)
        for i in range(n):
            if mask & (1<<i):
                cost += a[i+1]
                for v in cov[i+1]:
                    vis[v] = 1
        if sum(vis) == n:
            ans = min(ans, cost)
    print(ans)
else:
    vis = set()
    ans = 0
    use = []
    
    for i in range(1, n+1):
        if a[i] == 0:
            for v in cov[i]:
                vis.add(v)
            use.append(i)
    
    while len(vis) < n:
        best = -1
        best_val = 0
        
        for i in range(1, n+1):
            if i in use: continue
            
            cnt = 0
            for v in cov[i]:
                if v not in vis:
                    cnt += 1
            
            if cnt > 0:
                val = cnt / max(a[i], 1)
                if val > best_val:
                    best_val = val
                    best = i
        
        if best == -1: break
        
        ans += a[best]
        for v in cov[best]:
            vis.add(v)
        use.append(best)
    
    print(ans)