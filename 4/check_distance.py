# 거리 계산이 맞는지 확인

from collections import deque

# 간단한 예제로 테스트
test = """4
10 2
20 3
30 1
40 5
1 2 2
2 3 3
3 4 1"""

with open("test_dist.txt", "w") as f:
    f.write(test)

n = 4
graph = [[] for _ in range(n + 1)]
edges = [(1,2,2), (2,3,3), (3,4,1)]
for u, v, w in edges:
    graph[u].append((v, w))
    graph[v].append((u, w))

# 잘못된 BFS
def bad_bfs(start):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    q = deque([start])
    
    while q:
        u = q.popleft()
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                q.append(v)
    
    return dist

# 올바른 거리 계산 (Dijkstra)
import heapq

def dijkstra(start):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    return dist

print("=== 거리 계산 비교 ===")
for i in range(1, n+1):
    bad = bad_bfs(i)
    good = dijkstra(i)
    print(f"From {i}:")
    print(f"  BFS: {bad[1:]}")
    print(f"  Dijkstra: {good[1:]}")
    if bad != good:
        print("  >>> 차이 발견!")