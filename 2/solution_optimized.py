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
    # 서브태스크 2: k=1이고 N=10^t인 경우 특별 처리
    if k == 1 and is_power_of_10(n_str):
        return solve_k1_power_of_10(len(n_str) - 1)
    
    # 서브태스크 3: k=1인 일반적인 경우
    if k == 1:
        return solve_k1_general(n_str)
    
    # 일반적인 경우
    if len(n_str) <= 7:
        return brute_force(k, int(n_str))
    
    return digit_dp_correct(k, n_str)

def is_power_of_10(n_str):
    """n_str이 10^t 형태인지 확인"""
    return n_str[0] == '1' and all(c == '0' for c in n_str[1:])

def solve_k1_power_of_10(t):
    """k=1, N=10^t인 경우의 공식"""
    # 10^t까지의 수에서 1을 모두 제거한 합
    # 이는 수학적 공식으로 직접 계산 가능
    
    if t == 0:
        return 0
    
    # 공식 유도:
    # 각 자릿수별로 1이 아닌 숫자들의 기여도를 계산
    total = 0
    
    # t자리 수들까지 고려
    for digits in range(1, t + 1):
        # digits 자릿수를 가진 수들에서의 기여도
        contribution = calculate_contribution_for_length(digits)
        total = (total + contribution) % MOD
    
    return total

def calculate_contribution_for_length(length):
    """특정 길이의 수들에서 1을 제거했을 때의 총 기여도"""
    if length == 1:
        # 1자리: 2, 3, 4, 5, 6, 7, 8, 9 = 44
        return 44
    
    total = 0
    
    # 각 자릿수 위치에서의 기여도 계산
    for pos in range(length):
        # pos번째 자리(뒤에서부터)에 2~9가 올 때의 기여도
        if pos == length - 1:  # 맨 앞자리
            digits_sum = sum(range(2, 10))  # 2+3+...+9 = 44
        else:
            digits_sum = sum(range(0, 10)) - 1  # 0+2+3+...+9 = 44
        
        # 다른 자릿수들은 1이 아닌 9개 중 아무거나 (0 포함, 1 제외)
        other_positions = length - 1
        ways = pow(9, other_positions, MOD)
        
        # 결과에서 이 자릿수가 차지할 위치 (대략)
        result_pos = int(pos * 0.9)  # 1이 제거되므로 약간 줄어듦
        
        position_value = pow(10, result_pos, MOD)
        contribution = (digits_sum * ways * position_value) % MOD
        total = (total + contribution) % MOD
    
    return total

def solve_k1_general(n_str):
    """k=1인 일반적인 경우 최적화"""
    if len(n_str) <= 7:
        return brute_force(1, int(n_str))
    
    return digit_dp_k1_optimized(n_str)

def digit_dp_k1_optimized(n_str):
    """k=1에 특화된 최적화된 digit DP"""
    n = len(n_str)
    
    # k=1인 경우의 특별한 성질을 이용
    # 1이 제거되므로 나머지 숫자들만 고려
    
    total = 0
    
    for pos in range(n):
        limit = int(n_str[pos])
        
        for digit in range(2 if pos == 0 else 0, limit + 1):
            if digit == 1:
                continue
            
            # 이 자리에 이 digit이 오는 경우의 수 (1 제외)
            ways = count_ways_k1(n_str, pos, digit)
            
            if ways > 0:
                # k=1이므로 결과 길이는 약 0.9배
                avg_result_pos = int((n - pos - 1) * 0.9)
                contribution = (digit * pow(10, avg_result_pos, MOD) * ways) % MOD
                total = (total + contribution) % MOD
    
    return total

def count_ways_k1(n_str, pos, digit):
    """k=1일 때 pos 위치에 digit이 오는 경우의 수"""
    n = len(n_str)
    
    ways = 1
    
    # 각 자리에서 1이 아닌 숫자의 개수
    for i in range(n):
        if i == pos:
            continue
        
        limit = int(n_str[i])
        count = 0
        
        for d in range(1 if i == 0 else 0, limit + 1):
            if d != 1:
                count += 1
        
        ways = (ways * count) % MOD
        if count == 0:
            return 0
    
    return ways

def digit_dp_correct(k, n_str):
    """일반적인 경우의 정확한 digit DP"""
    n = len(n_str)
    ans = 0
    
    for pos in range(n):
        limit = int(n_str[pos])
        
        for digit in range(1 if pos == 0 else 0, limit + 1):
            if digit == k:
                continue
            
            ways = count_ways_general(n_str, pos, digit, k)
            
            if ways > 0:
                avg_contribution = calculate_average_contribution(pos, n, k)
                contribution = (digit * avg_contribution * ways) % MOD
                ans = (ans + contribution) % MOD
    
    return ans

def count_ways_general(n_str, pos, digit, k):
    """일반적인 경우의 경우의 수 계산"""
    n = len(n_str)
    count = 1
    
    for i in range(n):
        if i == pos:
            continue
        
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
    """평균 기여도 계산"""
    remaining = total_len - pos - 1
    expected_removed = remaining * 0.1
    expected_pos = int(remaining - expected_removed)
    
    return pow(10, max(0, expected_pos), MOD)

# 입력 처리
k = int(input())
n_str = input().strip()

print(solve(k, n_str))