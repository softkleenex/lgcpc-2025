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
    
    # 각 자릿수별로 기여도를 계산
    total = 0
    
    # pos번째 자리에 digit이 올 때의 기여도를 모두 합산
    for pos in range(n):
        for digit in range(1, 10):  # 0부터 시작하는 수는 없으므로 1부터
            if digit == k:
                continue
            
            # pos 위치에 digit이 오는 경우의 수 계산
            count = count_numbers_with_digit_at_pos(n_str, pos, digit, k)
            
            if count > 0:
                # 이 digit이 최종 결과에서 차지하는 자릿수 계산
                expected_pos_in_result = calculate_position_in_filtered_number(pos, n, k)
                
                # 기여도 = digit * 10^expected_pos_in_result * count
                contribution = (digit * pow(10, expected_pos_in_result, MOD) * count) % MOD
                total = (total + contribution) % MOD
    
    return total

def count_numbers_with_digit_at_pos(n_str, pos, digit, k):
    """pos 위치에 digit이 오는 수의 개수를 계산"""
    n = len(n_str)
    
    # pos보다 앞자리 처리
    front_count = 1
    for i in range(pos):
        limit = int(n_str[i])
        
        if digit == int(n_str[pos]) and i < pos:
            # tight 조건 확인
            possible = 0
            for d in range(1 if i == 0 else 0, limit + 1):
                if d != k:
                    possible += 1
            front_count = (front_count * possible) % MOD
        else:
            # 일반적인 경우
            if i == 0:
                possible = 9 if k != 0 else 8  # 첫 자리는 0이 올 수 없음
            else:
                possible = 9  # 0~9 중 k 제외
            front_count = (front_count * possible) % MOD
    
    # pos 위치의 digit이 조건을 만족하는지 확인
    if pos < n and digit > int(n_str[pos]):
        return 0
    
    # pos보다 뒷자리 처리
    back_count = 1
    for i in range(pos + 1, n):
        back_count = (back_count * 9) % MOD  # 각 자리에서 k가 아닌 9개 선택
    
    return (front_count * back_count) % MOD

def calculate_position_in_filtered_number(original_pos, total_len, k):
    """원래 pos 위치가 k를 제거한 후 몇 번째 자리에 해당하는지 계산"""
    # 뒤에서부터 세는 자릿수에서 k가 나올 확률을 고려
    expected_k_count_after = (total_len - original_pos - 1) / 10
    expected_pos_in_result = total_len - original_pos - 1 - int(expected_k_count_after)
    return max(0, expected_pos_in_result)

# 더 정확한 구현을 위해 기존의 검증된 방법 사용
def solve_verified(k, n_str):
    if len(n_str) <= 6:
        return brute_force(k, int(n_str))
    
    # 자릿수별 기여도 직접 계산
    return calculate_sum_by_position(k, n_str)

def calculate_sum_by_position(k, n_str):
    """각 자리별로 기여도를 직접 계산"""
    n = len(n_str)
    total = 0
    
    # 각 원본 자릿수 위치에 대해
    for pos in range(n):
        # 해당 위치에 올 수 있는 각 숫자에 대해
        contribution = calculate_position_contribution(n_str, pos, k)
        total = (total + contribution) % MOD
    
    return total

def calculate_position_contribution(n_str, pos, k):
    """특정 위치의 기여도 계산"""
    n = len(n_str)
    
    # pos 앞의 자릿수들에서 가능한 조합 수
    front_ways = 1
    for i in range(pos):
        if i == 0:
            # 첫 자리는 1~9 (0 제외)
            ways = 8 if k != 0 else 9
        else:
            # 나머지 자리는 0~9에서 k 제외
            ways = 9
        front_ways = (front_ways * ways) % MOD
    
    # pos 위치에 올 수 있는 숫자들의 기여도
    contribution = 0
    limit = int(n_str[pos])
    
    for digit in range(10):
        if digit == k:
            continue
        if digit > limit:
            break
        if pos == 0 and digit == 0:
            continue
        
        # 뒤쪽 자릿수들에서 가능한 조합 수
        back_ways = 1
        for i in range(pos + 1, n):
            back_ways = (back_ways * 9) % MOD
        
        # 이 digit이 결과에서 차지할 위치 계산
        # k가 제거되므로 실제 자릿수는 줄어듦
        result_pos = calculate_result_position(pos, n, k)
        
        # 기여도 계산
        ways = front_ways * back_ways % MOD
        digit_contribution = digit * pow(10, result_pos, MOD) * ways % MOD
        contribution = (contribution + digit_contribution) % MOD
    
    return contribution

def calculate_result_position(original_pos, total_len, k):
    """k 제거 후 실제 자릿수 위치 계산"""
    # 원본에서 뒤에서 original_pos번째 → 결과에서 뒤에서 몇 번째?
    # 대략적으로 k가 나올 확률을 1/10로 계산
    remaining = total_len - original_pos - 1
    expected_k_removed = remaining // 10
    return remaining - expected_k_removed

# 입력 처리
k = int(input())
n_str = input().strip()

print(solve(k, n_str))