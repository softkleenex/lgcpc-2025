#!/usr/bin/env python3

MOD = 1000000007

def solve(k, n_str):
    n = len(n_str)
    
    # 작은 경우는 brute force
    if n <= 6:
        return brute_force(k, int(n_str))
    
    # k=1인 경우 특별 처리
    if k == 1:
        return solve_k1(n_str)
    
    # 일반적인 경우 digit DP
    return digit_dp(k, n_str)

def brute_force(k, n):
    total = 0
    for i in range(1, n + 1):
        s = str(i)
        filtered = ''.join(c for c in s if c != str(k))
        if filtered:
            total = (total + int(filtered)) % MOD
    return total

def solve_k1(n_str):
    """k=1인 경우의 특별 처리"""
    n = len(n_str)
    
    # dp[pos][tight][started] = (count, sum)
    # count: 조건을 만족하는 수의 개수
    # sum: 해당 수들의 f(x) 합
    dp = {}
    
    def rec(pos, tight, started):
        if pos == n:
            return (1 if started else 0, 0)
        
        state = (pos, tight, started)
        if state in dp:
            return dp[state]
        
        limit = int(n_str[pos]) if tight else 9
        count_sum = 0
        value_sum = 0
        
        for digit in range(10):
            if digit > limit:
                break
            
            new_tight = tight and (digit == limit)
            new_started = started or (digit > 0)
            
            if digit == 1:
                # 1은 제거되므로 기여하지 않음
                sub_count, sub_sum = rec(pos + 1, new_tight, new_started)
                count_sum = (count_sum + sub_count) % MOD
                value_sum = (value_sum + sub_sum) % MOD
            else:
                # 1이 아닌 숫자
                sub_count, sub_sum = rec(pos + 1, new_tight, new_started)
                count_sum = (count_sum + sub_count) % MOD
                
                # 이 자릿수의 기여도 계산
                if new_started:
                    # digit * 10^(remaining_non_1_digits) * sub_count
                    remaining_digits = n - pos - 1
                    # 나머지 자리에서 1이 아닌 숫자의 개수 기댓값
                    pow10 = pow(10, remaining_digits, MOD)
                    contribution = (digit * pow10 * sub_count) % MOD
                    value_sum = (value_sum + sub_sum + contribution) % MOD
                else:
                    value_sum = (value_sum + sub_sum) % MOD
        
        dp[state] = (count_sum, value_sum)
        return dp[state]
    
    _, result = rec(0, True, False)
    return result

def digit_dp(k, n_str):
    """일반적인 경우의 digit DP"""
    n = len(n_str)
    
    # memo[pos][tight][started] = sum of f(x) for all valid x
    memo = {}
    
    def dp(pos, tight, started, current_value, multiplier):
        if pos == n:
            return current_value if started else 0
        
        state = (pos, tight, started, current_value % (MOD * 1000), multiplier % (MOD * 1000))
        if state in memo:
            return memo[state]
        
        limit = int(n_str[pos]) if tight else 9
        result = 0
        
        for digit in range(10):
            if digit > limit:
                break
            
            new_tight = tight and (digit == limit)
            new_started = started or (digit > 0)
            
            if digit == k:
                # k는 제거되므로 현재 값과 승수는 그대로
                result = (result + dp(pos + 1, new_tight, new_started, current_value, multiplier)) % MOD
            else:
                # k가 아닌 숫자
                if new_started:
                    new_value = (current_value + digit * multiplier) % MOD
                    new_multiplier = (multiplier * 10) % MOD
                    result = (result + dp(pos + 1, new_tight, new_started, new_value, new_multiplier)) % MOD
                else:
                    result = (result + dp(pos + 1, new_tight, new_started, 0, 1)) % MOD
        
        memo[state] = result
        return result
    
    return dp(0, True, False, 0, 1)

# 입력 처리
k = int(input())
n_str = input().strip()

print(solve(k, n_str))