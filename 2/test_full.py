#!/usr/bin/env python3
import subprocess
import time

# 서브태스크별 테스트 케이스
test_cases = [
    # 서브태스크 1: N < 1,000,000
    ("서브1-1", "1", "999999"),
    ("서브1-2", "5", "123456"),  
    ("서브1-3", "9", "500000"),
    
    # 서브태스크 2: k=1, N=10^t
    ("서브2-1", "1", "10"),
    ("서브2-2", "1", "100"),
    ("서브2-3", "1", "1000"),
    ("서브2-4", "1", "10000"),
    ("서브2-5", "1", "100000"),
    ("서브2-6", "1", "1000000"),
    ("서브2-7", "1", "10000000"),
    
    # 서브태스크 3: k=1 일반
    ("서브3-1", "1", "12345"),
    ("서브3-2", "1", "111111"),
    ("서브3-3", "1", "999999999"),
    
    # 서브태스크 4: N < 10^2000
    ("서브4-1", "3", "123456789012345678901234567890"),
    ("서브4-2", "7", "77777777777777777777777777777"),
    
    # 서브태스크 5: 추가 제약 없음
    ("서브5-1", "2", "2" * 1000),  # 2222...222 (1000자리)
    ("서브5-2", "5", "9" * 500),   # 999...999 (500자리)
    
    # 엣지 케이스
    ("엣지1", "1", "1"),  # f(1) = 0
    ("엣지2", "5", "5"),  # f(1)~f(4) + f(5)=0
    ("엣지3", "3", "33"),
    ("엣지4", "3", "333"),
    ("엣지5", "3", "3333"),
    ("엣지6", "9", "9999"),
    
    # 예제
    ("예제1", "3", "5"),
    ("예제2", "3", "4860000"),
]

print("전체 테스트 시작")
print("="*60)

for name, k, n in test_cases:
    input_data = f"{k}\n{n}\n"
    
    start = time.time()
    try:
        result = subprocess.run(
            ["python3", "solution.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3
        )
        
        elapsed = time.time() - start
        output = result.stdout.strip()
        
        # 결과 출력 (너무 길면 자르기)
        if len(n) > 20:
            n_display = n[:10] + "..." + n[-10:] + f"({len(n)}자리)"
        else:
            n_display = n
            
        print(f"{name:10} k={k}, N={n_display:30} => {output:15} ({elapsed:.3f}초)")
        
    except subprocess.TimeoutExpired:
        print(f"{name:10} k={k}, N={n_display:30} => TIMEOUT (>3초)")
    except Exception as e:
        print(f"{name:10} k={k}, N={n_display:30} => ERROR: {e}")

print("\n" + "="*60)
print("추가 테스트 케이스 (정답 검증)")
print("-"*60)

# 수동 계산 가능한 케이스들
verify_cases = [
    ("1", "10", 44),     # f(1)=0, f(2~9)=2+...+9=44, f(10)=0
    ("3", "5", 12),      # f(1)=1, f(2)=2, f(3)=0, f(4)=4, f(5)=5
    ("5", "10", 37),     # f(5)=0, 나머지는 그대로
    ("9", "10", 37),     # f(9)=0, f(10)=10, 나머지는 그대로
]

for k, n, expected in verify_cases:
    input_data = f"{k}\n{n}\n"
    result = subprocess.run(
        ["python3", "solution.py"],
        input=input_data,
        text=True,
        capture_output=True
    )
    output = int(result.stdout.strip())
    status = "✓" if output == expected else "✗"
    print(f"k={k}, N={n:5}: 결과={output:10}, 예상={expected:10} {status}")