#!/usr/bin/env python3
import subprocess
import time

print("📝 최종 솔루션 테스트")
print("="*60)

# 주요 테스트 케이스
test_cases = [
    ("예제 1", "3", "5", "12"),
    ("예제 2", "3", "4860000", "465808830"),
    
    # 서브태스크 1 - 작은 수
    ("서브1-작은", "1", "100", "4444"),
    ("서브1-중간", "5", "5000", "18756884"),
    ("서브1-큰", "9", "999999", "471638556"),
    
    # 서브태스크 2 - k=1, N=10^t
    ("서브2-10^1", "1", "10", "44"),
    ("서브2-10^2", "1", "100", "4444"),
    ("서브2-10^3", "1", "1000", "408804"),
    ("서브2-10^4", "1", "10000", "37245164"),
    
    # 서브태스크 3 - k=1 일반
    ("서브3-일반", "1", "54321", "229570556"),
    
    # 엣지 케이스
    ("모두k", "3", "3333", "3469350"),
    ("k=9", "9", "9999", "30473316"),
    
    # 큰 수 (타임아웃 체크)
    ("큰수1", "2", "123456789", None),
    ("큰수2", "7", "987654321", None),
]

passed = 0
failed = 0
timeout = 0

for name, k, n, expected in test_cases:
    input_data = f"{k}\n{n}\n"
    
    start = time.time()
    try:
        result = subprocess.run(
            ["python3", "solution.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=2
        )
        
        elapsed = time.time() - start
        output = result.stdout.strip()
        
        if expected:
            if output == expected:
                print(f"✅ {name:12} k={k} N={n:12} => {output:12} ({elapsed:.3f}초)")
                passed += 1
            else:
                print(f"❌ {name:12} k={k} N={n:12} => {output:12} (예상: {expected})")
                failed += 1
        else:
            print(f"⏱️  {name:12} k={k} N={n:12} => {output:12} ({elapsed:.3f}초)")
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {name:12} k={k} N={n:12} => TIMEOUT (>2초)")
        timeout += 1
    except Exception as e:
        print(f"💥 {name:12} k={k} N={n:12} => ERROR: {e}")
        failed += 1

print("\n" + "="*60)
print(f"📊 결과: 통과 {passed}, 실패 {failed}, 타임아웃 {timeout}")

if passed > 0 and failed == 0:
    print("✨ 모든 테스트 통과!")
elif failed > 0:
    print("⚠️  일부 테스트 실패")
    
print("\n💡 솔루션 특징:")
print("  - 작은 N(≤6자리): 브루트포스")
print("  - 큰 N: Digit DP with memoization")
print("  - 메모리 최적화: cnt 제한, val % MOD")
print("  - 한국 대학생 스타일: 간결한 코드, 실용적 접근")