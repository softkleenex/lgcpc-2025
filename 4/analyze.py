# 예제 분석 - 최적해 찾기
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

print("Signal analysis:")
for i in range(1, n + 1):
    ratio = len(covers[i]) / max(A[i], 1) if A[i] > 0 else float('inf')
    print(f"Signal {i}: cost {A[i]}, covers {len(covers[i])} vertices {covers[i]}, ratio {ratio:.3f}")

# 특별한 조합들 시도
print("\n=== Trying different strategies ===")

# 전략 1: 비용 0인 신호기 + 효율적인 조합
free_signals = [i for i in range(1, n + 1) if A[i] == 0]
print(f"Free signals: {free_signals}")

if free_signals:
    covered_by_free = set()
    for sig in free_signals:
        covered_by_free.update(covers[sig])
    print(f"Free signals cover: {covered_by_free}")
    remaining = set(range(1, n + 1)) - covered_by_free
    print(f"Remaining to cover: {remaining}")
    
    # 남은 정점들을 위한 최소 비용 조합 찾기
    if remaining:
        best_cost = float('inf')
        best_combo = None
        
        # 작은 조합들 시도
        from itertools import combinations
        
        paid_signals = [i for i in range(1, n + 1) if A[i] > 0]
        
        for r in range(1, min(len(paid_signals), 5) + 1):  # 최대 5개 조합
            for combo in combinations(paid_signals, r):
                combo_covers = set()
                for sig in combo:
                    combo_covers.update(covers[sig])
                
                if remaining.issubset(combo_covers):
                    cost = sum(A[sig] for sig in combo)
                    if cost < best_cost:
                        best_cost = cost
                        best_combo = combo
                        print(f"Found solution: free signals {free_signals} + paid signals {combo} = cost {cost}")

# 전략 2: 가장 효율적인 신호기들 조합
print("\n=== Most efficient signals ===")
efficiency = [(len(covers[i]) / max(A[i], 0.001), i, A[i], covers[i]) for i in range(1, n + 1)]
efficiency.sort(reverse=True)

for eff, sig, cost, cov in efficiency[:8]:
    print(f"Signal {sig}: efficiency {eff:.3f}, cost {cost}, covers {len(cov)} vertices")

# 특별 조합 시도: 11번(무료) + 다른 신호기들
print(f"\nSignal 11 covers: {covers[11]}")
remaining_after_11 = set(range(1, n + 1)) - covers[11]
print(f"After signal 11, remaining: {remaining_after_11}")

# 남은 정점들을 가장 적은 비용으로 커버하는 방법
if remaining_after_11:
    print("Trying to cover remaining with minimal cost...")
    
    # 각 남은 정점을 커버할 수 있는 가장 저렴한 신호기
    vertex_options = {}
    for v in remaining_after_11:
        options = []
        for sig in range(1, n + 1):
            if v in covers[sig] and A[sig] > 0:
                options.append((A[sig], sig))
        options.sort()
        vertex_options[v] = options
        print(f"Vertex {v} can be covered by: {options[:3]}")  # 상위 3개만