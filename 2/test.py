#!/usr/bin/env python3

# 문제: k 혐오자
# f(x) = x에서 숫자 k를 모두 제거한 수
# 구하는 것: f(1) + f(2) + ... + f(N) mod 1000000007

MOD = 1000000007

def f(x, k):
    """x에서 k를 제거한 수 반환"""
    s = str(x)
    r = ''.join(c for c in s if c != str(k))
    return int(r) if r else 0

def solve_small(k, n):
    """작은 N에 대한 브루트포스"""
    return sum(f(i, k) for i in range(1, n+1)) % MOD

# 테스트 케이스들
test_cases = [
    # (k, N, 예상답)
    # 예제 1
    (3, "5", 12),
    # 예제 2  
    (3, "4860000", 465808830),
    
    # 서브태스크 1: N < 1,000,000
    (1, "10", 45),  # f(1)=0, f(2)=2, ..., f(10)=0, sum=2+3+4+5+6+7+8+9=44? 
    (5, "20", 175),  # 1~20에서 5 제거
    (9, "100", 4941),  # 1~100에서 9 제거
    
    # 서브태스크 2: k=1, N=10^t
    (1, "10", 45),  # 10^1
    (1, "100", 4941),  # 10^2
    (1, "1000", 494550),  # 10^3
    
    # 서브태스크 3: k=1 일반
    (1, "15", 69),  # f(1)=0, f(2~9)=2+3+...+9=44, f(10~15)=0+2+3+4+5=14+11=25
    (1, "111", 5490),
    
    # 엣지 케이스
    (3, "3", 3),  # f(1)=1, f(2)=2, f(3)=0
    (3, "33", 258),  
    (3, "333", 25746),
    (3, "3333", 0),  # 3333은 f(3333)=0이 맞나?
    
    # k가 다른 케이스들
    (2, "25", 232),
    (4, "50", 1230),
    (7, "77", 2975),
    (8, "88", 3882),
    (9, "99", 4941),
]

print("테스트 시작...")
print("="*50)

# 작은 케이스들 직접 계산해서 검증
print("\n수동 계산 검증:")
print("-"*30)

# k=3, N=5
print("k=3, N=5:")
for i in range(1, 6):
    print(f"  f({i}) = {f(i, 3)}")
print(f"  합: {sum(f(i, 3) for i in range(1, 6))}")

# k=1, N=10  
print("\nk=1, N=10:")
for i in range(1, 11):
    print(f"  f({i}) = {f(i, 1)}")
print(f"  합: {sum(f(i, 1) for i in range(1, 11))}")

# k=1, N=15
print("\nk=1, N=15:")
total = 0
for i in range(1, 16):
    val = f(i, 1)
    total += val
    print(f"  f({i}) = {val}, 누적={total}")

print("\n" + "="*50)
print("자동 테스트:")
print("-"*30)

correct = 0
failed = []

for k, n_str, expected in test_cases:
    n = int(n_str)
    if n <= 1000000:  # 작은 경우만 테스트
        result = solve_small(k, n)
        status = "✓" if result == expected else "✗"
        if result == expected:
            correct += 1
        else:
            failed.append((k, n_str, expected, result))
        print(f"k={k}, N={n_str:>10}: 결과={result:>10}, 예상={expected:>10} {status}")

print("\n" + "="*50)
print(f"결과: {correct}/{len(test_cases)} 통과")

if failed:
    print("\n실패한 케이스:")
    for k, n, exp, res in failed:
        print(f"  k={k}, N={n}: 예상={exp}, 실제={res}, 차이={res-exp}")