MOD = 998244353

def get_valid_scores(n, scores, dependencies):
    score_count = {} 

    prereq = [[] for _ in range(n + 1)]
    for x, y in dependencies:
        prereq[y].append(x)
    
    def dfs(idx, selected, current_score):
        if idx > n:
            score_count[current_score] = score_count.get(current_score, 0) + 1
            return
        
        dfs(idx + 1, selected, current_score)
        
        can_select = True
        for req in prereq[idx]:
            if req not in selected:
                can_select = False
                break
        
        if can_select:
            selected.add(idx)
            dfs(idx + 1, selected, current_score + scores[idx - 1])
            selected.remove(idx)
    
    dfs(1, set(), 0)
    return score_count

def solve():
    P = int(input())
    
    all_problem_scores = []
    
    for _ in range(P):
        N, M = map(int, input().split())
        scores = list(map(int, input().split()))
        
        dependencies = []
        for _ in range(M):
            x, y = map(int, input().split())
            dependencies.append((x, y))
        
        problem_score_count = get_valid_scores(N, scores, dependencies)
        all_problem_scores.append(problem_score_count)
    
    max_score = 100 * P
    dp = [0] * (max_score + 1)
    dp[0] = 1
    
    for problem_score_count in all_problem_scores:
        new_dp = [0] * (max_score + 1)
        for i in range(max_score + 1):
            if dp[i] > 0:
                for score, count in problem_score_count.items():
                    if i + score <= max_score:
                        new_dp[i + score] = (new_dp[i + score] + dp[i] * count) % MOD
        dp = new_dp
    
    result = 0
    for t in range(max_score + 1):
        result = (result + dp[t] * t) % MOD
    
    print(result)

if __name__ == "__main__":
    solve()