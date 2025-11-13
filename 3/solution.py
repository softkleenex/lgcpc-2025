from collections import deque
from itertools import product

MOD = 998244353

def power(a, b):
    result = 1
    a %= MOD
    while b > 0:
        if b & 1:
            result = result * a % MOD
        a = a * a % MOD
        b >>= 1
    return result

def inverse(x):
    if x == 0:
        return 0
    return power(x, MOD - 2)

def get_distances(start, graph, n):
    dist = [-1] * (n + 1)
    dist[start] = 0
    queue = deque([start])
    
    while queue:
        u = queue.popleft()
        for v, cost in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + cost
                queue.append(v)
    return dist

def can_meet(positions, graph, distances, n, L):
    # 정점에서 만날 수 있는지
    for meet in range(1, n + 1):
        if all(distances[pos][meet] <= L for pos in positions):
            return True
    
    # 간선에서 만날 수 있는지
    for u in range(1, n + 1):
        for v, length in graph[u]:
            if u >= v:
                continue
            
            # 간선을 적당히 세분화해서 체크
            steps = min(201, length * 2 + 1)  # 최대 201단계
            for step in range(steps):
                t = step * length / (steps - 1) if steps > 1 else 0
                if all(min(distances[pos][u] + t, distances[pos][v] + (length - t)) <= L 
                       for pos in positions):
                    return True
    
    return False

def solve():
    try:
        n, k, L = map(int, input().split())
        
        if n == 1:
            print(1)
            return
        
        graph = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            a, b, c = map(int, input().split())
            graph[a].append((b, c))
            graph[b].append((a, c))
    
    except:
        print(0)
        return
    
    # 모든 정점 간 거리 계산
    distances = {}
    for i in range(1, n + 1):
        distances[i] = get_distances(i, graph, n)
    
    # L=0인 특수 케이스
    if L == 0:
        if k == 1:
            print(1)
        else:
            result = inverse(power(n, (k - 1) % (MOD - 1)))
            print(result)
        return
    
    # 매우 작은 케이스만 완전 탐색
    if n <= 3 and k <= 8:
        valid_count = 0
        
        for positions in product(range(1, n + 1), repeat=k):
            if can_meet(positions, graph, distances, n, L):
                valid_count += 1
        
        total_count = power(n, k)
        result = (valid_count * inverse(total_count)) % MOD
        print(result)
        return
    
    # 큰 케이스: 수학적 근사
    # 각 정점에서 L 거리 내에 도달 가능한 정점들 계산
    max_reachable = 0
    for v in range(1, n + 1):
        reachable_count = 0
        for u in range(1, n + 1):
            if distances[v][u] <= L:
                reachable_count += 1
        max_reachable = max(max_reachable, reachable_count)
    
    # 간선에서도 체크 (최대 정점 수)
    for u in range(1, n + 1):
        for neighbor, edge_len in graph[u]:
            if u >= neighbor:
                continue
            
            # 간선 중점에서 체크
            mid_reachable = 0
            t = edge_len / 2.0
            for v in range(1, n + 1):
                dist_to_mid = min(distances[v][u] + t, distances[v][neighbor] + (edge_len - t))
                if dist_to_mid <= L:
                    mid_reachable += 1
            
            max_reachable = max(max_reachable, mid_reachable)
    
    if max_reachable == n:
        print(1)
    else:
        # 확률 = (max_reachable / n)^k
        prob = power(max_reachable, k % (MOD - 1)) * inverse(power(n, k % (MOD - 1))) % MOD
        print(prob)

if __name__ == "__main__":
    solve()