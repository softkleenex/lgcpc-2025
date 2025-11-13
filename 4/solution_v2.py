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

# 각 신호기가 커버할 수 있는 정점들
cov = [[] for _ in range(n+1)]
for i in range(1, n+1):
    d = bfs(i)
    for j in range(1, n+1):
        if d[j] <= b[i]:
            cov[i].append(j)

if n <= 20:
    # 비트마스크 DP
    dp = [10**18] * (1 << n)
    dp[0] = 0
    
    for m in range(1 << n):
        if dp[m] == 10**18:
            continue
        for i in range(1, n+1):
            nm = m
            for v in cov[i]:
                nm |= (1 << (v-1))
            dp[nm] = min(dp[nm], dp[m] + a[i])
    
    print(dp[(1 << n) - 1])
else:
    # 큰 N에 대해서는 set 사용
    covered = set()
    res = 0
    used = set()
    
    # 비용 0인 신호기 먼저
    for i in range(1, n+1):
        if a[i] == 0:
            for v in cov[i]:
                covered.add(v)
            used.add(i)
    
    # 필수 신호기 찾기
    while True:
        essential = []
        for v in range(1, n+1):
            if v in covered:
                continue
            
            options = []
            for i in range(1, n+1):
                if i not in used and v in cov[i]:
                    options.append(i)
            
            if len(options) == 1:
                essential.append(options[0])
        
        if not essential:
            break
        
        for sig in essential:
            if sig not in used:
                res += a[sig]
                for v in cov[sig]:
                    covered.add(v)
                used.add(sig)
    
    # 그리디로 나머지 처리
    while len(covered) < n:
        best = -1
        best_val = 0
        
        for i in range(1, n+1):
            if i in used:
                continue
            
            cnt = 0
            for v in cov[i]:
                if v not in covered:
                    cnt += 1
            
            if cnt > 0:
                val = cnt / max(a[i], 1)
                if val > best_val:
                    best_val = val
                    best = i
        
        if best == -1:
            break
        
        res += a[best]
        for v in cov[best]:
            covered.add(v)
        used.add(best)
    
    print(res)