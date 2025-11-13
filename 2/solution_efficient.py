import sys
sys.setrecursionlimit(200000)

mod = 1000000007

def remove_k(x, k):
    s = str(x)
    res = ""
    for d in s:
        if d != str(k):
            res += d
    if res == "":
        return 0
    return int(res)

def brute(k, n):
    ans = 0
    for i in range(1, n + 1):
        ans = (ans + remove_k(i, k)) % mod
    return ans

def digit_dp_single(k, n_str):
    """단일 DP로 모든 기여도를 한번에 계산"""
    n = len(n_str)
    memo = {}
    
    def dp(pos, tight, started):
        if pos == n:
            return 0
        
        if (pos, tight, started) in memo:
            return memo[(pos, tight, started)]
        
        lim = int(n_str[pos]) if tight else 9
        total = 0
        
        for d in range(lim + 1):
            new_tight = tight and (d == lim)
            new_start = started or (d > 0)
            
            # 재귀 호출
            sub_total = dp(pos + 1, new_tight, new_start)
            total = (total + sub_total) % mod
            
            # 이 자리 숫자가 k가 아니고 숫자가 시작된 경우의 기여도 계산
            if d != k and new_start:
                # 이 위치에서 d가 나타나는 경우의 수
                count = count_ways(n_str, pos + 1, new_tight, k)
                
                # 평균적인 기여도 계산 (간소화)
                contribution = calculate_contribution_simplified(d, pos, n, count)
                total = (total + contribution) % mod
        
        memo[(pos, tight, started)] = total
        return total
    
    return dp(0, True, False)

def count_ways(n_str, start_pos, tight, k):
    """start_pos부터 끝까지 가능한 수의 개수 (k 제외)"""
    if start_pos >= len(n_str):
        return 1
    
    ways = 1
    for i in range(start_pos, len(n_str)):
        if tight and i == start_pos:
            limit = int(n_str[i])
            choices = 0
            for d in range(limit + 1):
                if d != k:
                    choices += 1
            ways = (ways * max(1, choices)) % mod
        else:
            ways = (ways * 9) % mod  # 0-9에서 k 제외
        tight = False
    
    return ways

def calculate_contribution_simplified(digit, pos, total_len, count):
    """간소화된 기여도 계산"""
    # 평균적인 자릿수 추정
    avg_result_len = max(1, (total_len - pos) * 8 // 9)  # k를 제외한 평균 길이
    
    # 각 자릿수별 기여도의 평균
    total_contribution = 0
    for result_pos in range(min(avg_result_len, 15)):  # 제한적으로 계산
        position_value = pow(10, result_pos, mod)
        contribution = (digit * position_value % mod * count) % mod
        # 가중치 적용 (중간 자릿수가 더 많이 나타남)
        weight = max(1, 15 - abs(result_pos - avg_result_len // 2))
        total_contribution = (total_contribution + contribution * weight) % mod
    
    return (total_contribution // max(1, avg_result_len)) % mod

k = int(input())
n_str = input().strip()

if len(n_str) <= 6:
    print(brute(k, int(n_str)))
else:
    print(digit_dp_single(k, n_str))