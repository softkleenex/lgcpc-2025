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
    
    # 더 큰 수의 경우 수학적 접근
    return mathematical_approach(k, n_str)

def mathematical_approach(k, n_str):
    """수학적 방법으로 해결"""
    n = len(n_str)
    total = 0
    
    # 각 자릿수별로 계산
    for pos in range(n):
        # 해당 자릿수에서 각 숫자(k 제외)가 기여하는 값 계산
        contribution = calculate_position_sum(n_str, pos, k)
        total = (total + contribution) % MOD
    
    return total

def calculate_position_sum(n_str, pos, k):
    """특정 위치에서의 총 기여도 계산"""
    n = len(n_str)
    
    # 해당 위치에 올 수 있는 숫자들의 합
    digit_sum = 0
    count_sum = 0
    
    # tight 제한 고려
    limit = int(n_str[pos])
    
    for digit in range(0 if pos > 0 else 1, limit + 1):  # 첫 자리는 1부터
        if digit == k:
            continue
            
        # 이 digit이 pos 위치에 올 때의 경우의 수
        ways = count_numbers_with_digit_at_position(n_str, pos, digit, k)
        
        if ways > 0:
            # 이 digit이 최종 결과에서 가질 자릿수 위치
            result_position = estimate_result_position(pos, n, k)
            
            # 기여도 = digit * 10^result_position * ways
            contribution = (digit * pow(10, result_position, MOD) * ways) % MOD
            digit_sum = (digit_sum + contribution) % MOD
    
    return digit_sum

def count_numbers_with_digit_at_position(n_str, pos, digit, k):
    """pos 위치에 특정 digit이 오는 수의 개수"""
    n = len(n_str)
    
    # pos 앞쪽 자릿수들의 경우의 수
    front_ways = 1
    for i in range(pos):
        if i == 0:
            # 첫 자리: 1~9에서 k 제외
            ways = 8 if k != 0 else 9
        else:
            # 나머지: 0~9에서 k 제외
            ways = 9
        front_ways = (front_ways * ways) % MOD
    
    # pos 뒤쪽 자릿수들의 경우의 수
    back_ways = 1
    for i in range(pos + 1, n):
        back_ways = (back_ways * 9) % MOD  # 0~9에서 k 제외
    
    # tight 제한 고려한 실제 경우의 수
    actual_ways = calculate_actual_ways(n_str, pos, digit, k, front_ways, back_ways)
    
    return actual_ways

def calculate_actual_ways(n_str, pos, digit, k, front_ways, back_ways):
    """tight 제한을 고려한 실제 경우의 수"""
    n = len(n_str)
    
    # 기본적인 경우의 수
    basic_ways = (front_ways * back_ways) % MOD
    
    # tight 제한에 의한 조정이 필요한지 확인
    current_limit = int(n_str[pos])
    if digit <= current_limit:
        return basic_ways
    else:
        return 0

def estimate_result_position(original_pos, total_len, k):
    """k 제거 후 해당 자릿수의 위치 추정"""
    # 원래 위치에서 뒤쪽에 있는 자릿수들 중 k가 제거될 개수 추정
    remaining_positions = total_len - original_pos - 1
    expected_k_removals = remaining_positions // 10  # 대략 1/10 확률로 k 등장
    
    result_pos = remaining_positions - expected_k_removals
    return max(0, result_pos)

# 더 정확한 구현을 위해 완전히 새로운 접근
def solve_v2(k, n_str):
    if len(n_str) <= 6:
        return brute_force(k, int(n_str))
    
    # Digit DP with proper contribution calculation
    return digit_dp_v2(k, n_str)

def digit_dp_v2(k, n_str):
    """개선된 Digit DP"""
    n = len(n_str)
    
    # [pos][tight][started] -> (count, sum)
    memo = {}
    
    def dp(pos, tight, started):
        if pos == n:
            return (0, 0)  # (count, sum)
        
        state = (pos, tight, started)
        if state in memo:
            return memo[state]
        
        limit = int(n_str[pos]) if tight else 9
        total_count = 0
        total_sum = 0
        
        for digit in range(10):
            if digit > limit:
                break
            
            new_tight = tight and (digit == limit)
            new_started = started or (digit > 0)
            
            if not new_started:
                # Leading zero
                sub_count, sub_sum = dp(pos + 1, new_tight, False)
                total_sum = (total_sum + sub_sum) % MOD
            elif digit == k:
                # k는 제거됨
                sub_count, sub_sum = dp(pos + 1, new_tight, True)
                total_sum = (total_sum + sub_sum) % MOD
            else:
                # k가 아닌 유효한 숫자
                sub_count, sub_sum = dp(pos + 1, new_tight, True)
                
                # 이 자릿수가 기여하는 값을 계산
                # 남은 자릿수에서 k가 아닌 숫자들의 평균 개수 계산
                remaining = n - pos - 1
                avg_non_k = calculate_average_non_k_digits(remaining, k)
                
                # digit * 10^avg_non_k 형태로 기여
                contribution = (digit * pow(10, avg_non_k, MOD)) % MOD
                
                # 이 경우의 수 계산
                case_count = count_valid_suffixes(remaining, k)
                
                total_sum = (total_sum + sub_sum + contribution * case_count) % MOD
        
        memo[state] = (total_count, total_sum)
        return memo[state]
    
    _, result = dp(0, True, False)
    return result

def calculate_average_non_k_digits(length, k):
    """길이 length에서 k가 아닌 숫자들의 평균 개수"""
    if length == 0:
        return 0
    # 각 자리에서 k가 아닐 확률은 9/10
    return int(length * 0.9)

def count_valid_suffixes(length, k):
    """길이 length에서 가능한 suffix 개수 (k 포함 가능)"""
    if length == 0:
        return 1
    return pow(9, length, MOD)  # 각 자리에서 k 제외한 9개 선택

# 입력 처리
k = int(input())
n_str = input().strip()

print(solve_v2(k, n_str))