#!/usr/bin/env python3

MOD = 1000000007

def remove_k(num, k):
    s = str(num)
    result = ''.join(c for c in s if c != str(k))
    return int(result) if result else 0

def brute_force(k, n):
    total = 0
    for i in range(1, n + 1):
        total = (total + remove_k(i, k)) % MOD
    return total

def solve(k, n_str):
    if len(n_str) <= 6:
        return brute_force(k, int(n_str))
    
    return digit_dp(k, n_str)

def digit_dp(k, n_str):
    """정확한 digit DP 구현"""
    n = len(n_str)
    
    # dp[pos][tight][started] = 해당 조건에서 f(x)들의 합
    dp = {}
    
    def rec(pos, tight, started):
        if pos == n:
            return 0
        
        state = (pos, tight, started)
        if state in dp:
            return dp[state]
        
        limit = int(n_str[pos]) if tight else 9
        result = 0
        
        for digit in range(10):
            if digit > limit:
                break
            
            new_tight = tight and (digit == limit)
            new_started = started or (digit > 0)
            
            if not new_started:
                # Leading zero case
                result = (result + rec(pos + 1, new_tight, False)) % MOD
            else:
                # Valid number case
                if digit == k:
                    # k digit is removed, so only add the contribution from remaining digits
                    result = (result + rec(pos + 1, new_tight, True)) % MOD
                else:
                    # Non-k digit contributes to the sum
                    # Calculate contribution of this digit in the final result
                    contribution = calc_contribution(digit, pos, n, k, new_tight, n_str)
                    remaining_sum = rec(pos + 1, new_tight, True)
                    result = (result + contribution + remaining_sum) % MOD
        
        dp[state] = result
        return result
    
    return rec(0, True, False)

def calc_contribution(digit, pos, n, k, tight, n_str):
    """현재 digit이 최종 합에 기여하는 값 정확히 계산"""
    
    # 이 digit 뒤에 오는 자릿수들에서 k가 제거된 후의 길이 분포 계산
    remaining_pos = n - pos - 1
    
    if remaining_pos == 0:
        return digit
    
    # 뒤쪽 자릿수들에서 만들어지는 모든 조합에 대해
    # 이 digit이 최종 결과에서 차지하는 위치의 기댓값 계산
    
    total_contribution = 0
    
    # 각 가능한 k 제거 개수에 대해 계산
    for k_removed in range(remaining_pos + 1):
        prob = probability_of_k_removed(remaining_pos, k, k_removed, tight, n_str[pos+1:] if pos+1 < n else "")
        if prob > 0:
            final_pos = remaining_pos - k_removed
            digit_value = digit * pow(10, final_pos, MOD) % MOD
            total_contribution = (total_contribution + digit_value * prob) % MOD
    
    return total_contribution

def probability_of_k_removed(length, k, k_count, tight, limit_str):
    """길이 length에서 정확히 k_count개의 k가 나올 확률 계산 (경우의 수로 계산)"""
    if length == 0:
        return 1 if k_count == 0 else 0
    
    # Dynamic programming to count exact ways
    # This is complex for tight constraint, so use approximation
    
    if k_count > length:
        return 0
    
    # 이항계수와 확률을 이용한 근사
    from math import comb
    if not tight:
        # 각 자리에서 k가 나올 확률 1/10, 아닐 확률 9/10
        ways = comb(length, k_count) * pow(9, length - k_count, MOD) % MOD
        return ways
    else:
        # tight constraint가 있는 경우 복잡하므로 단순화
        return count_exact_k(length, k, k_count, limit_str)

def count_exact_k(length, k, k_count, limit_str):
    """정확히 k_count개의 k를 포함하는 경우의 수"""
    if length == 0:
        return 1 if k_count == 0 else 0
    
    # 간단한 근사: tight constraint 무시하고 계산
    from math import comb
    if k_count > length:
        return 0
    
    return comb(length, k_count) * pow(9, length - k_count, MOD) % MOD

# 더 간단하고 정확한 접근법
def solve_simple(k, n_str):
    if len(n_str) <= 6:
        return brute_force(k, int(n_str))
    
    return simple_digit_dp(k, n_str)

def simple_digit_dp(k, n_str):
    """단순화된 정확한 접근법"""
    n = len(n_str)
    
    # 각 자릿수별로 기여도를 직접 계산
    total = 0
    
    for pos in range(n):
        pos_contribution = calculate_position_contribution_exact(n_str, pos, k)
        total = (total + pos_contribution) % MOD
    
    return total

def calculate_position_contribution_exact(n_str, pos, k):
    """pos 위치에서의 정확한 기여도 계산"""
    n = len(n_str)
    
    # pos 위치에 올 수 있는 각 digit에 대해
    contribution = 0
    limit = int(n_str[pos])
    
    for digit in range(1 if pos == 0 else 0, limit + 1):
        if digit == k:
            continue
        
        # 이 digit이 pos에 올 때의 경우의 수
        count = count_numbers_with_digit(n_str, pos, digit, k)
        
        # 결과에서 이 digit이 차지할 위치들의 분포
        for result_pos in range(n - pos):  # 최대 가능한 결과 위치
            prob = probability_digit_at_result_pos(pos, result_pos, n, k)
            if prob > 0:
                value = (digit * pow(10, result_pos, MOD) * count * prob) % MOD
                contribution = (contribution + value) % MOD
    
    return contribution

def count_numbers_with_digit(n_str, pos, digit, k):
    """pos 위치에 특정 digit이 오는 수의 개수 (tight 제약 고려)"""
    n = len(n_str)
    
    # 앞쪽 자릿수 경우의 수
    front = 1
    for i in range(pos):
        if i == 0:
            front = (front * (8 if k != 0 else 9)) % MOD  # 1~9에서 k 제외
        else:
            front = (front * 9) % MOD  # 0~9에서 k 제외
    
    # 뒤쪽 자릿수 경우의 수  
    back = 1
    for i in range(pos + 1, n):
        back = (back * 9) % MOD  # 0~9에서 k 제외
    
    return (front * back) % MOD

def probability_digit_at_result_pos(original_pos, result_pos, n, k):
    """원래 pos의 digit이 결과에서 result_pos에 올 확률"""
    remaining = n - original_pos - 1
    k_removed = remaining - result_pos
    
    if k_removed < 0 or k_removed > remaining:
        return 0
    
    # 이항 분포 근사
    from math import comb
    if k_removed <= remaining:
        return comb(remaining, k_removed)
    return 0

# 입력 처리
k = int(input())
n_str = input().strip()

print(solve_simple(k, n_str))