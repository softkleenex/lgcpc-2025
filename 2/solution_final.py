#!/usr/bin/env python3

MOD = 1000000007

def remove_k_digit(num, k):
    """숫자에서 k를 제거한 결과를 반환"""
    s = str(num)
    result = ''.join(c for c in s if c != str(k))
    return int(result) if result else 0

def brute_force_solution(k, n):
    """작은 n에 대한 브루트 포스 해법"""
    total = 0
    for i in range(1, n + 1):
        total = (total + remove_k_digit(i, k)) % MOD
    return total

def solve_large_n(k, n_str):
    """큰 n에 대한 digit DP 해법"""
    n = len(n_str)
    total_sum = 0
    
    # 각 자릿수 위치별로 기여도를 계산
    for position in range(n):
        position_sum = calculate_position_sum(n_str, position, k)
        total_sum = (total_sum + position_sum) % MOD
    
    return total_sum

def calculate_position_sum(n_str, pos, k):
    """특정 위치에서 모든 가능한 숫자의 기여도 합계"""
    n = len(n_str)
    position_total = 0
    
    # 해당 위치에 올 수 있는 최대 숫자
    max_digit = int(n_str[pos])
    
    # 각 가능한 숫자에 대해 계산
    for digit in range(1 if pos == 0 else 0, max_digit + 1):
        if digit == k:
            continue  # k는 제거되므로 기여도 없음
        
        # 이 숫자가 해당 위치에 오는 경우의 수
        occurrence_count = count_occurrences(n_str, pos, digit, k)
        
        if occurrence_count > 0:
            # 이 숫자가 최종 결과에서 기여하는 값
            contribution_value = calculate_digit_contribution(digit, pos, n, k)
            position_total = (position_total + contribution_value * occurrence_count) % MOD
    
    return position_total

def count_occurrences(n_str, target_pos, target_digit, k):
    """target_pos에 target_digit이 오는 유효한 수의 개수"""
    n = len(n_str)
    count = 1
    
    # 각 자릿수별로 유효한 선택의 수를 곱함
    for pos in range(n):
        if pos == target_pos:
            continue  # 이미 target_digit으로 고정됨
        
        # 해당 자리에서 선택 가능한 숫자의 개수
        limit = int(n_str[pos])
        valid_choices = 0
        
        for d in range(1 if pos == 0 else 0, limit + 1):
            if d != k:
                valid_choices += 1
        
        count = (count * valid_choices) % MOD
        
        # 선택 가능한 숫자가 없으면 0 반환
        if valid_choices == 0:
            return 0
    
    return count

def calculate_digit_contribution(digit, pos, total_length, k):
    """digit이 pos 위치에 있을 때 최종 결과에 기여하는 값"""
    # pos 뒤에 있는 자릿수들에서 k가 제거된 후의 평균 길이
    remaining_positions = total_length - pos - 1
    
    if remaining_positions == 0:
        return digit
    
    # k가 제거될 개수의 기댓값 (각 자리에서 k가 나올 확률 ≈ 1/10)
    expected_k_removals = remaining_positions * 0.1
    expected_result_length = remaining_positions - expected_k_removals
    
    # 결과에서의 자릿값
    result_position = max(0, int(expected_result_length))
    return (digit * pow(10, result_position, MOD)) % MOD

def main():
    """메인 함수"""
    k = int(input())
    n_str = input().strip()
    
    # 작은 수는 브루트 포스, 큰 수는 digit DP 사용
    if len(n_str) <= 7:
        result = brute_force_solution(k, int(n_str))
    else:
        result = solve_large_n(k, n_str)
    
    print(result)

if __name__ == "__main__":
    main()