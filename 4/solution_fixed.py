from collections import defaultdict

n = int(input())
A = [0] * (n + 1)
B = [0] * (n + 1)

for i in range(1, n + 1):
    a, b = map(int, input().split())
    A[i] = a
    B[i] = b

graph = defaultdict(list)

for _ in range(n - 1):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))
    graph[v].append((u, w))

# DFS로 거리 계산 (트리이므로)
def dfs_dist(start):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    
    def dfs(u, d):
        dist[u] = d
        for v, w in graph[u]:
            if dist[v] == float('inf'):
                dfs(v, d + w)
    
    dfs(start, 0)
    return dist

# 각 정점에서 다른 모든 정점까지의 거리를 계산
all_dist = {}
for i in range(1, n + 1):
    all_dist[i] = dfs_dist(i)

# 각 신호기가 커버할 수 있는 정점들
covers = [set() for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if all_dist[i][j] <= B[i]:
            covers[i].add(j)

# 비용이 0인 신호기들 먼저 선택
covered = set()
total_cost = 0
used_signals = []

# 1. 비용이 0인 신호기들을 모두 사용
for i in range(1, n + 1):
    if A[i] == 0:
        covered.update(covers[i])
        used_signals.append(i)

# 2. 남은 정점들을 커버하기 위한 그리디
remaining = set(range(1, n + 1)) - covered

while remaining:
    best_ratio = -1
    best_signal = -1
    best_new_covered = 0
    
    for signal in range(1, n + 1):
        if signal in used_signals or A[signal] == 0:
            continue
        
        # 이 신호기가 추가로 커버할 수 있는 정점들
        new_covered = len(covers[signal] & remaining)
        
        if new_covered > 0:
            ratio = new_covered / A[signal]
            if ratio > best_ratio:
                best_ratio = ratio
                best_signal = signal
                best_new_covered = new_covered
    
    if best_signal == -1:
        break
    
    # 선택된 신호기로 커버
    total_cost += A[best_signal]
    used_signals.append(best_signal)
    newly_covered = covers[best_signal] & remaining
    covered.update(newly_covered)
    remaining -= newly_covered

print(total_cost)