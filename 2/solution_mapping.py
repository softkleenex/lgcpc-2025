MOD = 1000000007

def f(x, k):
    s = str(x)
    result = ""
    for digit in s:
        if digit != str(k):
            result += digit
    return int(result) if result else 0

def solve_small(k, n):
    total = 0
    for i in range(1, n + 1):
        total = (total + f(i, k)) % MOD
    return total

def solve_large(k, n_str):
    n = len(n_str)
    total = 0
    
    for orig_pos in range(n):
        for result_pos in range(n):
            contribution = calculate_mapping_contribution(n_str, orig_pos, result_pos, k)
            total = (total + contribution) % MOD
    
    return total

def calculate_mapping_contribution(n_str, orig_pos, result_pos, k):
    n = len(n_str)
    memo = {}
    
    def dp(pos, tight, started, non_k_before_orig, non_k_after_orig):
        if pos == n:
            if started:
                if non_k_after_orig == result_pos:
                    return 1
            return 0
        
        key = (pos, tight, started, non_k_before_orig, non_k_after_orig)
        if key in memo:
            return memo[key]
        
        limit = int(n_str[pos]) if tight else 9
        result = 0
        
        for digit in range(0, limit + 1):
            new_tight = tight and (digit == limit)
            new_started = started or (digit > 0)
            
            if pos == orig_pos:
                if digit != k and new_started:
                    count = dp(pos + 1, new_tight, new_started, non_k_before_orig, 0)
                    position_value = pow(10, result_pos, MOD)
                    contribution = (digit * position_value % MOD * count) % MOD
                    result = (result + contribution) % MOD
                elif digit == k and new_started:
                    count = dp(pos + 1, new_tight, new_started, non_k_before_orig, 0)
                else:
                    count = dp(pos + 1, new_tight, new_started, non_k_before_orig, 0)
            elif pos < orig_pos:
                if digit != k and new_started:
                    new_before = non_k_before_orig + 1
                else:
                    new_before = non_k_before_orig
                result = (result + dp(pos + 1, new_tight, new_started, new_before, non_k_after_orig)) % MOD
            else:
                if digit != k:
                    new_after = non_k_after_orig + 1
                else:
                    new_after = non_k_after_orig
                result = (result + dp(pos + 1, new_tight, new_started, non_k_before_orig, new_after)) % MOD
        
        memo[key] = result
        return result
    
    return dp(0, True, False, 0, 0)

def solve():
    k = int(input())
    n_str = input().strip()
    
    if len(n_str) <= 4:
        n = int(n_str)
        print(solve_small(k, n))
        return
    
    result = solve_large(k, n_str)
    print(result)

if __name__ == "__main__":
    solve()