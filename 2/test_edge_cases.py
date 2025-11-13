#!/usr/bin/env python3

# 다양한 엣지 케이스 테스트

test_cases = [
    (1, "10"),      # k=1, N=10 (서브태스크 2 관련)
    (1, "100"),     # k=1, N=100  
    (1, "1000"),    # k=1, N=1000
    (9, "999"),     # k=9, N=999 (많은 9가 포함된 경우)
    (5, "555555"),  # k=5, N=555555 (k로만 이루어진 수들 포함)
    (1, "1111111"), # k=1, N=1111111 (1이 많이 포함된 경우)
    (2, "12345"),   # k=2, 일반적인 경우
]

for k, n_str in test_cases:
    print(f"k={k}, N={n_str}")
    
    # 작은 경우는 brute force로 검증
    if len(n_str) <= 6:
        def remove_k(num, k):
            s = str(num)
            result = ''.join(c for c in s if c != str(k))
            return int(result) if result else 0

        def brute_force(k, n):
            total = 0
            for i in range(1, n + 1):
                total = (total + remove_k(i, k)) % 1000000007
            return total
        
        expected = brute_force(k, int(n_str))
        print(f"Expected (brute force): {expected}")
    
    # 파일로 테스트 케이스 저장하고 실행
    with open("temp_test.txt", "w") as f:
        f.write(f"{k}\n{n_str}\n")
    
    import subprocess
    result = subprocess.run(["python3", "solution_final_correct.py"], 
                          stdin=open("temp_test.txt"), 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Our solution: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    
    print("---")