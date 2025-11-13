from collections import defaultdict
from itertools import combinations
import sys

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

covers = [set() for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if all_dist[i][j] <= B[i]:
            covers[i].add(j)

# 비용 0인 신호기는 반드시 사용
free_signals = [i for i in range(1, n + 1) if A[i] == 0]
mandatory_covered = set()
mandatory_cost = 0

for sig in free_signals:
    mandatory_covered.update(covers[sig])
    mandatory_cost += A[sig]

remaining = set(range(1, n + 1)) - mandatory_covered
paid_signals = [i for i in range(1, n + 1) if A[i] > 0]

print(f"Must use free signals: {free_signals}")
print(f"They cover: {mandatory_covered}")  
print(f"Remaining to cover: {remaining}")
print(f"Available paid signals: {paid_signals}")

min_cost = float('inf')
best_solution = None

# 작은 조합부터 시도
found = False
for r in range(len(remaining)):  # 최소한 남은 정점 수만큼은 필요할 수 있음
    if found:
        break
    for combo in combinations(paid_signals, r + 1):
        combo_covers = set()
        for sig in combo:
            combo_covers.update(covers[sig])
        
        if remaining.issubset(combo_covers):
            cost = mandatory_cost + sum(A[sig] for sig in combo)
            if cost < min_cost:
                min_cost = cost
                best_solution = (free_signals, combo)
                print(f"Solution found: free {free_signals} + paid {combo} = cost {cost}")
                if cost == 350:  # 목표값에 도달하면 탐색 중단
                    found = True
                    break

if best_solution:
    print(f"\nBest solution: free signals {best_solution[0]} + paid signals {best_solution[1]}")
    print(f"Total cost: {min_cost}")
else:
    print("No solution found!")

# 특별히 350을 만들 수 있는 조합 찾기
print(f"\n=== Looking for cost 350 combinations ===")
target = 350

# 11번(무료) + 나머지 신호기들로 350 만들기
for r in range(1, len(paid_signals) + 1):
    for combo in combinations(paid_signals, r):
        combo_covers = set()
        for sig in combo:
            combo_covers.update(covers[sig])
        
        if remaining.issubset(combo_covers):
            cost = sum(A[sig] for sig in combo)
            if cost == target:
                print(f"TARGET FOUND: signals 11 + {combo} = cost {cost}")
                
                # 검증
                total_covered = mandatory_covered.copy()
                for sig in combo:
                    total_covered.update(covers[sig])
                print(f"Covers all vertices: {len(total_covered) == n}")
                print(f"Coverage: {sorted(total_covered)}")