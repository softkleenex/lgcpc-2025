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
    if len(n_str) <= 7:  # 조금 더 큰 범위까지 brute force
        return brute_force(k, int(n_str))
    
    # 큰 수의 경우 정확한 digit DP
    return digit_dp_correct(k, n_str)

def digit_dp_correct(k, n_str):
    """정확한 digit DP - 각 자릿수의 기여도를 정확히 계산"""
    n = len(n_str)
    ans = 0
    
    # 각 자릿수 위치에서 각 숫자가 기여하는 값을 계산
    for pos in range(n):
        limit = int(n_str[pos])
        
        for digit in range(1 if pos == 0 else 0, limit + 1):
            if digit == k:
                continue
            
            # 이 자리에 이 digit이 오는 경우의 수
            ways = count_ways(n_str, pos, digit, k)
            
            if ways > 0:
                # 이 digit이 최종 결과에서 기여하는 값
                contribution = digit_contribution(digit, pos, n, k) * ways % MOD
                ans = (ans + contribution) % MOD
    
    return ans

def count_ways(n_str, pos, digit, k):
    """pos 위치에 digit이 오고, 다른 자리는 k가 아닌 수인 경우의 수"""
    n = len(n_str)
    
    # pos보다 앞자리에서 가능한 경우의 수
    front_ways = 1
    for i in range(pos):
        curr_limit = int(n_str[i])
        
        # tight한 조건에서 가능한 숫자 개수 계산
        count = 0
        for d in range(1 if i == 0 else 0, curr_limit + 1):
            if d != k:
                count += 1
        
        front_ways = (front_ways * count) % MOD
        if count == 0:
            return 0
    
    # pos보다 뒷자리에서 가능한 경우의 수
    back_ways = 1
    for i in range(pos + 1, n):
        curr_limit = int(n_str[i])
        
        # 각 자리에서 k가 아닌 숫자 개수
        count = 0
        for d in range(10):
            if d <= curr_limit and d != k:
                count += 1
        
        back_ways = (back_ways * count) % MOD
        if count == 0:
            return 0
    
    return (front_ways * back_ways) % MOD

def digit_contribution(digit, pos, total_len, k):
    """digit이 pos 위치에 있을 때 최종 결과에 기여하는 평균값"""
    # 뒤쪽 자릿수들에서 k가 제거된 후 예상되는 자릿수
    remaining_positions = total_len - pos - 1
    
    # k가 제거될 개수의 기댓값: 각 자리에서 k가 나올 확률은 대략 1/10
    expected_k_removed = remaining_positions / 10
    expected_final_pos = int(remaining_positions - expected_k_removed)
    
    return digit * pow(10, expected_final_pos, MOD) % MOD

# 더 정확한 방법: 각 경우를 직접 계산
def solve_precise(k, n_str):
    if len(n_str) <= 7:
        return brute_force(k, int(n_str))
    
    return precise_calculation(k, n_str)

def precise_calculation(k, n_str):
    """더 정확한 계산 방법"""
    n = len(n_str)
    
    # 전체 합을 구하는 다른 접근법
    # 1부터 N까지 각 수에 대해 f(x)를 계산하는 대신
    # 각 자릿수가 최종 결과에 기여하는 총합을 직접 계산
    
    total = 0
    
    # 각 원본 자릿수 위치에 대해
    for orig_pos in range(n):
        # 해당 위치에서 각 숫자(k 제외)의 총 기여도
        pos_sum = calculate_position_sum_precise(n_str, orig_pos, k)
        total = (total + pos_sum) % MOD
    
    return total

def calculate_position_sum_precise(n_str, pos, k):
    """특정 위치에서 모든 숫자의 기여도 합"""
    n = len(n_str)
    total = 0
    
    limit = int(n_str[pos])
    for digit in range(1 if pos == 0 else 0, limit + 1):
        if digit == k:
            continue
        
        # 이 digit이 이 위치에 오는 모든 수들에서 기여하는 총합
        contribution = calculate_digit_total_contribution(n_str, pos, digit, k)
        total = (total + contribution) % MOD
    
    return total

def calculate_digit_total_contribution(n_str, pos, digit, k):
    """특정 위치의 특정 digit의 총 기여도"""
    n = len(n_str)
    
    # 이 조건을 만족하는 수의 개수
    count = count_valid_numbers(n_str, pos, digit, k)
    
    # 각각에서 이 digit이 기여하는 평균값
    avg_contribution = calculate_average_contribution(pos, n, k)
    
    return (digit * avg_contribution * count) % MOD

def count_valid_numbers(n_str, pos, digit, k):
    """pos 위치에 digit이 오고 전체가 유효한 수의 개수"""
    n = len(n_str)
    
    count = 1
    
    # 각 자리별로 가능한 경우의 수 계산
    for i in range(n):
        if i == pos:
            continue  # 이미 digit으로 고정됨
        
        limit = int(n_str[i])
        valid_count = 0
        
        for d in range(1 if i == 0 else 0, limit + 1):
            if d != k:
                valid_count += 1
        
        count = (count * valid_count) % MOD
        if valid_count == 0:
            return 0
    
    return count

def calculate_average_contribution(pos, total_len, k):
    """pos 위치의 숫자가 최종 결과에서 차지하는 자릿값의 평균"""
    remaining = total_len - pos - 1
    
    # 뒤쪽에서 k가 제거될 개수의 기댓값
    expected_removed = remaining * 0.1  # 각 자리에서 k가 나올 확률 1/10
    expected_pos = int(remaining - expected_removed)
    
    return pow(10, max(0, expected_pos), MOD)

# 입력 처리
k = int(input())
n_str = input().strip()

print(solve_precise(k, n_str))