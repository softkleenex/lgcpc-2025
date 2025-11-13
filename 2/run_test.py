#!/usr/bin/env python3
import subprocess

test_cases = [
    # (k, N, 예상답)
    ("3", "5", "12"),
    ("3", "4860000", None),  # 큰 수는 나중에
    ("1", "10", "44"),
    ("1", "100", "4444"),
    ("3", "33", "402"),
    ("3", "333", "37971"),
    ("2", "25", "190"),
    ("5", "55", "1215"),
    ("7", "77", "2198"),
    ("9", "99", "3636"),
]

print("solution.py 테스트")
print("="*50)

for k, n, expected in test_cases:
    input_data = f"{k}\n{n}\n"
    
    try:
        result = subprocess.run(
            ["python3", "solution.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=5
        )
        
        output = result.stdout.strip()
        
        if expected:
            status = "✓" if output == expected else "✗"
            print(f"k={k}, N={n:>10}: 결과={output:>10}, 예상={expected:>10} {status}")
        else:
            print(f"k={k}, N={n:>10}: 결과={output:>10}")
            
    except subprocess.TimeoutExpired:
        print(f"k={k}, N={n:>10}: TIMEOUT")
    except Exception as e:
        print(f"k={k}, N={n:>10}: ERROR - {e}")

# 예제 테스트
print("\n예제 입력 테스트:")
print("-"*30)

examples = [
    ("3", "5", "12"),
    ("3", "4860000", "465808830"),
]

for k, n, expected in examples:
    input_data = f"{k}\n{n}\n"
    
    try:
        result = subprocess.run(
            ["python3", "solution.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=5
        )
        
        output = result.stdout.strip()
        status = "✓" if output == expected else "✗"
        print(f"예제 {k},{n}: 결과={output}, 예상={expected} {status}")
        
    except Exception as e:
        print(f"예제 {k},{n}: ERROR - {e}")