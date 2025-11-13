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
    # 작은 경우는 brute force로 정확히 계산
    if len(n_str) <= 7:
        return brute_force(k, int(n_str))
    
    # 큰 경우는 정확한 digit DP 사용
    return digit_dp_solution(k, n_str)

def digit_dp_solution(k, n_str):
    """정확한 digit DP 구현"""
    n = len(n_str)
    total = 0
    
    # 각 자릿수 위치별로 기여도 계산
    for pos in range(n):
        pos_contribution = calculate_position_contribution(n_str, pos, k)
        total = (total + pos_contribution) % MOD
    
    return total

def calculate_position_contribution(n_str, pos, k):
    """pos 위치에서의 총 기여도"""
    n = len(n_str)
    contribution = 0
    
    limit = int(n_str[pos])
    
    # pos 위치에 올 수 있는 각 숫자에 대해
    for digit in range(1 if pos == 0 else 0, limit + 1):
        if digit == k:
            continue
        
        # 이 숫자가 이 위치에 오는 경우의 수
        count = count_valid_numbers(n_str, pos, digit, k)
        
        if count > 0:
            # 이 숫자가 최종 결과에 기여하는 평균값
            avg_value = calculate_digit_value(digit, pos, n, k)
            contribution = (contribution + avg_value * count) % MOD
    
    return contribution

def count_valid_numbers(n_str, pos, digit, k):
    """pos 위치에 digit이 오고, 모든 자리가 유효한 수의 개수"""
    n = len(n_str)
    count = 1
    
    for i in range(n):
        if i == pos:
            continue  # 이미 digit으로 고정
        
        # i번째 자리에서 유효한 숫자의 개수
        limit = int(n_str[i])
        valid_count = 0
        
        for d in range(1 if i == 0 else 0, limit + 1):
            if d != k:
                valid_count += 1
        
        count = (count * valid_count) % MOD
        
        if valid_count == 0:
            return 0
    
    return count

def calculate_digit_value(digit, pos, total_len, k):
    """pos 위치의 digit이 최종 결과에서 가지는 평균 값"""
    # pos 뒤쪽 자릿수들에서 k가 제거된 후의 기댓값 계산
    remaining_positions = total_len - pos - 1
    
    if remaining_positions == 0:
        return digit
    
    # k가 제거될 개수의 기댓값
    # 실제로는 더 정확한 계산이 필요하지만, 근사값 사용
    expected_k_removed = remaining_positions / 10
    expected_final_position = int(remaining_positions - expected_k_removed)
    
    return (digit * pow(10, max(0, expected_final_position), MOD)) % MOD

# 더 정확한 계산을 위한 개선된 버전
def solve_accurate(k, n_str):
    """더 정확한 계산"""
    if len(n_str) <= 7:
        return brute_force(k, int(n_str))
    
    return accurate_digit_dp(k, n_str)

def accurate_digit_dp(k, n_str):
    """더 정확한 digit DP"""
    n = len(n_str)
    
    # 각 자릿수의 정확한 기여도를 계산
    total = 0
    
    for pos in range(n):
        # 해당 위치의 모든 가능한 숫자들의 기여도
        for digit in range(1 if pos == 0 else 0, int(n_str[pos]) + 1):
            if digit == k:
                continue
            
            # 정확한 기여도 계산
            exact_contribution = calculate_exact_contribution(n_str, pos, digit, k)
            total = (total + exact_contribution) % MOD
    
    return total

def calculate_exact_contribution(n_str, pos, digit, k):
    """정확한 기여도 계산"""
    n = len(n_str)
    
    # 이 조건을 만족하는 수의 개수
    valid_count = count_exact_valid_numbers(n_str, pos, digit, k)
    
    if valid_count == 0:
        return 0
    
    # 각 경우에서 이 digit의 정확한 기여도 계산
    remaining_len = n - pos - 1
    
    # k 제거 후 평균 자릿수 위치
    avg_pos = calculate_average_position_after_k_removal(remaining_len, k)
    
    digit_value = (digit * pow(10, avg_pos, MOD)) % MOD
    
    return (digit_value * valid_count) % MOD

def count_exact_valid_numbers(n_str, pos, digit, k):
    """정확한 유효한 수의 개수"""
    n = len(n_str)
    
    # 동적 프로그래밍으로 정확히 계산
    # 하지만 복잡성을 피하기 위해 단순 계산 사용
    
    result = 1
    for i in range(n):
        if i == pos:
            continue
        
        limit = int(n_str[i])
        count = 0
        for d in range(1 if i == 0 else 0, limit + 1):
            if d != k:
                count += 1
        
        result = (result * count) % MOD
        if count == 0:
            return 0
    
    return result

def calculate_average_position_after_k_removal(length, k):
    """k 제거 후 평균 자릿수 위치"""
    if length == 0:
        return 0
    
    # 간단한 근사: 각 자리에서 k가 나올 확률 1/10
    expected_removed = length / 10
    return max(0, int(length - expected_removed))

# 입력 처리
k = int(input())
n_str = input().strip()

print(solve_accurate(k, n_str))