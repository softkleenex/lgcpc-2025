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

print(f"A: {A[1:]}")
print(f"B: {B[1:]}")

# DFS로 거리 계산
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

all_dist = {}
for i in range(1, n + 1):
    all_dist[i] = dfs_dist(i)

print("Distance matrix:")
for i in range(1, n + 1):
    print(f"From {i}: {all_dist[i][1:]}")

# 각 신호기가 커버할 수 있는 정점들
covers = [[] for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if all_dist[i][j] <= B[i]:
            covers[i].append(j)

print("\nSignal coverage:")
for i in range(1, n + 1):
    print(f"Signal {i} (cost {A[i]}, range {B[i]}) covers: {covers[i]}")

# 완전 탐색으로 최적해 찾기
from itertools import combinations

min_cost = float('inf')
best_solution = None

# 모든 신호기 조합 시도
for r in range(1, n + 1):
    for combo in combinations(range(1, n + 1), r):
        # 이 조합이 모든 정점을 커버하는지 확인
        covered = set()
        for signal in combo:
            covered.update(covers[signal])
        
        if len(covered) == n:  # 모든 정점 커버
            cost = sum(A[signal] for signal in combo)
            if cost < min_cost:
                min_cost = cost
                best_solution = combo
                print(f"New best: signals {combo}, cost {cost}")

print(f"\nOptimal solution: signals {best_solution}, cost {min_cost}")