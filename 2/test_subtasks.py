import subprocess
import sys

def run_solution(k, n_str):
    """Run solution.py with given input and return output"""
    input_data = f"{k}\n{n_str}"
    try:
        result = subprocess.run(['python3', 'solution.py'], 
                              input=input_data, 
                              text=True, 
                              capture_output=True, 
                              timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"ERROR: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"EXCEPTION: {e}"

def test_subtask_1():
    """서브태스크 1: 1 ≤ N < 1,000,000"""
    print("=== 서브태스크 1 테스트 ===")
    
    test_cases = [
        (3, "5"),           # 예제 1
        (1, "10"),          # 작은 k=1 케이스
        (5, "999999"),      # 최대 N
        (9, "123456"),      # 중간 N
        (2, "888888"),      # k가 많이 포함된 경우
    ]
    
    for k, n_str in test_cases:
        result = run_solution(k, n_str)
        print(f"k={k}, N={n_str}: {result}")
        if result.startswith("ERROR") or result == "TIMEOUT":
            print("  ❌ 실패")
        else:
            print("  ✅ 성공")
    print()

def test_subtask_2():
    """서브태스크 2: k=1, N=10^t (0 ≤ t < 100,000)"""
    print("=== 서브태스크 2 테스트 ===")
    
    test_cases = [
        (1, "1"),           # 10^0
        (1, "10"),          # 10^1
        (1, "100"),         # 10^2
        (1, "1000"),        # 10^3
        (1, "10000"),       # 10^4
        (1, "100000"),      # 10^5
        (1, "1000000"),     # 10^6
        (1, "10000000"),    # 10^7
    ]
    
    for k, n_str in test_cases:
        result = run_solution(k, n_str)
        print(f"k={k}, N=10^{len(n_str)-1}: {result}")
        if result.startswith("ERROR") or result == "TIMEOUT":
            print("  ❌ 실패")
        else:
            print("  ✅ 성공")
    print()

def test_subtask_3():
    """서브태스크 3: k=1 (일반적인 경우)"""
    print("=== 서브태스크 3 테스트 ===")
    
    test_cases = [
        (1, "99"),          # k=1, 1이 없는 수
        (1, "111"),         # k=1, 모든 자리가 1
        (1, "12345"),       # k=1, 혼합
        (1, "987654321"),   # k=1, 큰 수
        (1, "1111111111"),  # k=1, 긴 1들
    ]
    
    for k, n_str in test_cases:
        result = run_solution(k, n_str)
        print(f"k={k}, N={n_str}: {result}")
        if result.startswith("ERROR") or result == "TIMEOUT":
            print("  ❌ 실패")
        else:
            print("  ✅ 성공")
    print()

def test_subtask_4():
    """서브태스크 4: N < 10^2000 (매우 큰 수)"""
    print("=== 서브태스크 4 테스트 ===")
    
    # 2000자리까지는 아니지만 충분히 큰 수들
    test_cases = [
        (3, "1" + "0" * 50),    # 10^50
        (7, "9" * 100),         # 999...999 (100자리)
        (2, "1" + "2" * 200),   # 122...222 (201자리)
        (5, "123456789" * 10),  # 반복 패턴 (90자리)
    ]
    
    for k, n_str in test_cases:
        result = run_solution(k, n_str)
        print(f"k={k}, N={n_str[:20]}... ({len(n_str)}자리): {result}")
        if result.startswith("ERROR") or result == "TIMEOUT":
            print("  ❌ 실패")
        else:
            print("  ✅ 성공")
    print()

def test_subtask_5():
    """서브태스크 5: 제약 없음 (매우 큰 경우)"""
    print("=== 서브태스크 5 테스트 ===")
    
    # 실제 제한에 가까운 매우 큰 수들
    test_cases = [
        (1, "1" + "0" * 1000),      # 10^1000
        (9, "9" * 5000),            # 999...999 (5000자리)
        (4, "1234567890" * 500),    # 반복 패턴 (5000자리)
    ]
    
    for k, n_str in test_cases:
        result = run_solution(k, n_str)
        print(f"k={k}, N={n_str[:20]}... ({len(n_str)}자리): {result}")
        if result.startswith("ERROR") or result == "TIMEOUT":
            print("  ❌ 실패")
        else:
            print("  ✅ 성공")
    print()

if __name__ == "__main__":
    print("서브태스크별 테스트 시작...\n")
    
    test_subtask_1()
    test_subtask_2() 
    test_subtask_3()
    test_subtask_4()
    test_subtask_5()
    
    print("모든 테스트 완료!")