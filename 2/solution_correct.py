#!/usr/bin/env python3

MOD = 1000000007

def solve(k, n_str):
    if len(n_str) <= 6:
        return brute_force(k, int(n_str))
    
    return digit_dp(k, n_str)

def brute_force(k, n):
    total = 0
    for i in range(1, n + 1):
        s = str(i)
        filtered = ''.join(c for c in s if c != str(k))
        if filtered:
            total = (total + int(filtered)) % MOD
    return total

def digit_dp(k, n_str):
    n = len(n_str)
    
    # dp[pos][tight][started] = sum of f(x)
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
            
            # 재귀 호출로 나머지 부분의 합 구하기
            sub_result = rec(pos + 1, new_tight, new_started)
            
            if digit == k:
                # k는 제거되므로 기여하지 않음
                result = (result + sub_result) % MOD
            else:
                # k가 아닌 숫자의 경우
                if new_started:
                    # 이 숫자가 기여하는 값 계산
                    contribution = calculate_contribution(digit, pos, n, k, new_tight, n_str[pos+1:] if pos+1 < n else "")
                    result = (result + sub_result + contribution) % MOD
                else:
                    result = (result + sub_result) % MOD
        
        dp[state] = result
        return result
    
    return rec(0, True, False)

def calculate_contribution(digit, pos, total_len, k, tight, remaining_str):
    """pos 위치의 digit이 최종 결과에 기여하는 값을 계산"""
    
    # 남은 자릿수에서 k가 아닌 숫자들의 개수를 계산
    remaining_len = total_len - pos - 1
    
    if remaining_len == 0:
        return digit
    
    # 남은 자릿수에서 가능한 k가 아닌 숫자 조합의 수와 그 합을 계산
    count, total_ways = count_non_k_numbers(remaining_len, k, tight, remaining_str if tight else "")
    
    if total_ways == 0:
        return digit
    
    # digit * 10^(남은 k가 아닌 자릿수) * 경우의 수
    non_k_positions = count_expected_non_k_positions(remaining_len, k)
    multiplier = pow(10, non_k_positions, MOD)
    
    return (digit * multiplier * total_ways) % MOD

def count_non_k_numbers(length, k, tight, limit_str):
    """길이가 length인 수들 중에서 k가 없는 수들의 개수와 총 경우의 수를 반환"""
    if length == 0:
        return 0, 1
    
    # 각 자릿수에서 k가 아닌 숫자가 나올 확률은 9/10
    # 하지만 정확한 계산을 위해 DP 사용
    dp = {}
    
    def rec(pos, tight_remaining):
        if pos == length:
            return 1
        
        state = (pos, tight_remaining)
        if state in dp:
            return dp[state]
        
        if tight_remaining and pos < len(limit_str):
            limit = int(limit_str[pos])
        else:
            limit = 9
            tight_remaining = False
        
        result = 0
        for d in range(10):
            if d > limit:
                break
            if d != k:
                new_tight = tight_remaining and (d == limit)
                result = (result + rec(pos + 1, new_tight)) % MOD
        
        dp[state] = result
        return result
    
    ways = rec(0, tight)
    avg_non_k_digits = (length * 9 * ways // 10) if ways > 0 else 0
    
    return avg_non_k_digits, ways

def count_expected_non_k_positions(length, k):
    """길이가 length인 수에서 k가 아닌 자릿수의 기댓값"""
    # 각 자리에서 k가 아닐 확률이 9/10이므로
    # 기댓값은 length * 9/10
    # 하지만 정수로 근사
    return (length * 9) // 10

# 입력 처리
k = int(input())
n_str = input().strip()

print(solve(k, n_str))