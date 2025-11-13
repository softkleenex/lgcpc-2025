import subprocess

def test_solution(k, n_str, timeout=30):
    input_data = f"{k}\n{n_str}"
    try:
        result = subprocess.run(['python3', 'solution.py'], 
                              input=input_data, 
                              text=True, 
                              capture_output=True, 
                              timeout=timeout)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"ERROR"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except:
        return "EXCEPTION"

print("핵심 서브태스크 테스트:")
print()

# 서브태스크 2: k=1, N=10^t
print("서브태스크 2 (k=1, 10^t):")
powers = [1, 10, 100, 1000, 10000, 100000]
for p in powers:
    n_str = str(p)
    result = test_solution(1, n_str, 10)
    print(f"  k=1, N=10^{len(n_str)-1}: {result}")

print()

# 서브태스크 3: k=1 일반
print("서브태스크 3 (k=1 일반):")
cases = ["99", "111", "12345", "987654321"]
for n_str in cases:
    result = test_solution(1, n_str, 10) 
    print(f"  k=1, N={n_str}: {result}")

print()

# 서브태스크 4: 큰 수
print("서브태스크 4 (큰 수):")
big_cases = [
    ("3", "1" + "0" * 50),  # 10^50
    ("7", "9" * 100),       # 999...999 (100자리)
]
for k, n_str in big_cases:
    result = test_solution(int(k), n_str, 15)
    print(f"  k={k}, N={n_str[:10]}... ({len(n_str)}자리): {result}")

print()

# 예제 검증
print("예제 검증:")
print(f"  예제1 k=3, N=5: {test_solution(3, '5')}")
print(f"  예제2 k=3, N=4860000: {test_solution(3, '4860000')}")