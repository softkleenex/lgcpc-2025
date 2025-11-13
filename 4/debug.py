# 디버깅용 코드
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
print(f"Graph edges: {dict(graph)}")

# DFS로 거리 계산 (트리이므로)
def dfs_dist(start):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    visited = [False] * (n + 1)
    
    def dfs(u, d):
        visited[u] = True
        dist[u] = d
        for v, w in graph[u]:
            if not visited[v]:
                dfs(v, d + w)
    
    dfs(start, 0)
    return dist

# 각 정점에서 다른 모든 정점까지의 거리를 계산
all_dist = {}
for i in range(1, n + 1):
    all_dist[i] = dfs_dist(i)

print("\nDistance matrix:")
for i in range(1, n + 1):
    print(f"From {i}: {all_dist[i][1:]}")

# 각 정점이 신호를 받을 수 있는 신호기들을 찾기
can_cover = [[] for _ in range(n + 1)]

for i in range(1, n + 1):  # 정점 i가
    for j in range(1, n + 1):  # 신호기 j에서
        if all_dist[j][i] <= B[j]:  # 신호를 받을 수 있다면
            can_cover[i].append(j)

print("\nCoverage:")
for i in range(1, n + 1):
    print(f"Vertex {i} can be covered by signals: {can_cover[i]}")

# Set Cover 문제를 그리디로 해결
covered = [False] * (n + 1)
total_cost = 0
selected_signals = []

while not all(covered[i] for i in range(1, n + 1)):
    best_ratio = -1
    best_signal = -1
    
    for signal in range(1, n + 1):
        if A[signal] == 0:
            continue
        
        # 이 신호기가 추가로 커버할 수 있는 정점들
        new_covered = 0
        for v in range(1, n + 1):
            if not covered[v] and signal in can_cover[v]:
                new_covered += 1
        
        if new_covered > 0:
            ratio = new_covered / A[signal]
            if ratio > best_ratio:
                best_ratio = ratio
                best_signal = signal
    
    if best_signal == -1:
        # 비용이 0인 신호기 찾기
        for signal in range(1, n + 1):
            if A[signal] == 0:
                new_covered = 0
                for v in range(1, n + 1):
                    if not covered[v] and signal in can_cover[v]:
                        new_covered += 1
                
                if new_covered > 0:
                    best_signal = signal
                    break
    
    # 선택된 신호기로 커버
    print(f"\nSelecting signal {best_signal} (cost: {A[best_signal]}, ratio: {best_ratio})")
    total_cost += A[best_signal]
    selected_signals.append(best_signal)
    
    newly_covered = []
    for v in range(1, n + 1):
        if not covered[v] and best_signal in can_cover[v]:
            covered[v] = True
            newly_covered.append(v)
    
    print(f"Newly covered vertices: {newly_covered}")
    print(f"Currently covered: {[i for i in range(1, n + 1) if covered[i]]}")

print(f"\nSelected signals: {selected_signals}")
print(f"Total cost: {total_cost}")