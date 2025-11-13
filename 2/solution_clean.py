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

def digit_dp(k, n_str):
    n = len(n_str)
    
    # memo[pos][tight][started] = sum of f(x) for numbers formed
    memo = {}
    
    def dp(pos, tight, started):
        if pos == n:
            return 0
        
        state = (pos, tight, started)
        if state in memo:
            return memo[state]
        
        limit = int(n_str[pos]) if tight else 9
        result = 0
        
        for digit in range(10):
            if digit > limit:
                break
            
            new_tight = tight and (digit == limit)
            new_started = started or (digit > 0)
            
            if not new_started:
                # 아직 시작되지 않은 경우 (leading zeros)
                result = (result + dp(pos + 1, new_tight, False)) % MOD
            elif digit == k:
                # k 숫자는 제거되므로 다음 자리로
                result = (result + dp(pos + 1, new_tight, True)) % MOD
            else:
                # k가 아닌 숫자인 경우
                # 이 숫자가 결과에 미치는 영향을 계산
                
                # 현재 자리에서 이 digit이 기여하는 값
                contribution = calculate_digit_contribution(digit, pos, n, k, new_tight, n_str[pos+1:] if pos+1 < n else "")
                
                # 나머지 자리들의 기여도
                rest = dp(pos + 1, new_tight, True)
                
                result = (result + contribution + rest) % MOD
        
        memo[state] = result
        return result
    
    return dp(0, True, False)

def calculate_digit_contribution(digit, pos, total_len, k, tight, remaining_str):
    """현재 digit이 최종 합에 기여하는 값을 계산"""
    
    # 남은 자릿수들에서 만들어지는 수들의 개수와 평균 길이를 계산
    remaining_len = total_len - pos - 1
    
    if remaining_len == 0:
        return digit
    
    # 남은 자릿수에서 k가 제거된 후의 예상 자릿수
    expected_result_len = calculate_expected_length_without_k(remaining_len, k, tight, remaining_str)
    
    # 남은 자릿수를 채우는 방법의 수
    ways = count_ways_to_fill(remaining_len, k, tight, remaining_str)
    
    # digit * 10^expected_result_len * ways
    multiplier = pow(10, expected_result_len, MOD)
    return (digit * multiplier * ways) % MOD

def calculate_expected_length_without_k(length, k, tight, limit_str):
    """k를 제거한 후 예상되는 길이"""
    if length == 0:
        return 0
    
    # 간단한 추정: 각 자리에서 k가 나올 확률은 대략 1/10
    # 따라서 k가 아닌 숫자가 나올 확률은 9/10
    return int(length * 0.9)

def count_ways_to_fill(length, k, tight, limit_str):
    """남은 자릿수를 채우는 방법의 수"""
    if length == 0:
        return 1
    
    # 각 자리에서 k가 아닌 숫자를 선택하는 경우의 수
    ways = 1
    for i in range(length):
        if tight and i < len(limit_str):
            limit = int(limit_str[i])
            count = 0
            for d in range(10):
                if d <= limit and d != k:
                    count += 1
            ways = (ways * count) % MOD
            if count == 0:
                return 0
        else:
            ways = (ways * 9) % MOD  # 0~9에서 k 제외한 9개
    
    return ways

def solve(k, n_str):
    if len(n_str) <= 6:
        return brute_force(k, int(n_str))
    else:
        return digit_dp(k, n_str)

# 입력 처리
k = int(input())
n_str = input().strip()

print(solve(k, n_str))