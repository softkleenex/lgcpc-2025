n = int(input())
a = [0] * (n+1)  # 비용
b = [0] * (n+1)  # 범위

for i in range(1, n+1):
    a[i], b[i] = map(int, input().split())

adj = [[] for _ in range(n+1)]
for _ in range(n-1):
    u, v, w = map(int, input().split())
    adj[u].append((v, w))
    adj[v].append((u, w))

# dfs로 거리 계산 (트리니까)
def dfs(start, cur, dist, visited, distances):
    visited[cur] = True
    distances[cur] = dist
    for nxt, w in adj[cur]:
        if not visited[nxt]:
            dfs(start, nxt, dist + w, visited, distances)

# 각 신호기가 커버하는 정점들
covers = [set() for _ in range(n+1)]
for i in range(1, n+1):
    distances = [0] * (n+1)
    visited = [False] * (n+1)
    dfs(i, i, 0, visited, distances)
    
    for j in range(1, n+1):
        if distances[j] <= b[i]:
            covers[i].add(j)

# 작은 n은 완전탐색
if n <= 20:
    min_cost = float('inf')
    
    for mask in range(1, 1 << n):
        cost = 0
        covered = set()
        
        for i in range(n):
            if mask & (1 << i):
                sig = i + 1
                cost += a[sig]
                covered |= covers[sig]
        
        if len(covered) == n:
            min_cost = min(min_cost, cost)
    
    print(min_cost)

# 큰 n은 더 정교한 알고리즘
else:
    # DP가 불가능하므로 휴리스틱 사용
    # 1. 무료 신호기 사용
    covered = set()
    total_cost = 0
    used = [False] * (n+1)
    
    for i in range(1, n+1):
        if a[i] == 0:
            covered |= covers[i]
            used[i] = True
    
    # 2. 필수 신호기 (특정 정점을 유일하게 커버)
    changed = True
    while changed:
        changed = False
        for v in range(1, n+1):
            if v in covered:
                continue
            
            options = []
            for i in range(1, n+1):
                if not used[i] and v in covers[i]:
                    options.append(i)
            
            if len(options) == 1:
                sig = options[0]
                total_cost += a[sig]
                covered |= covers[sig]
                used[sig] = True
                changed = True
    
    # 3. 그리디 휴리스틱
    while len(covered) < n:
        best = -1
        best_ratio = 0
        
        for i in range(1, n+1):
            if used[i]:
                continue
            
            new_covered = len(covers[i] - covered)
            if new_covered > 0:
                ratio = new_covered / a[i] if a[i] > 0 else float('inf')
                if ratio > best_ratio:
                    best_ratio = ratio
                    best = i
        
        if best == -1:
            break
        
        total_cost += a[best]
        covered |= covers[best]
        used[best] = True
    
    print(total_cost)