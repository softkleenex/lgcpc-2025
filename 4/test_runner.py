import subprocess

test_cases = [
    ("test1.txt", "비용 0인 신호기 하나로 모두 커버"),
    ("test2.txt", "선형 트리, 비용 0인 신호기가 중간에 있음"),
    ("test3.txt", "모든 신호기가 자기 자신만 커버, 하나는 모두 커버"),
    ("test4.txt", "두 정점, 각자가 모두 커버 가능"),
    ("input.txt", "예제 입력")
]

for test_file, desc in test_cases:
    print(f"\n===== {test_file}: {desc} =====")
    
    # 입력 확인
    with open(test_file, 'r') as f:
        lines = f.readlines()
        n = int(lines[0])
        print(f"N = {n}")
        
        if n <= 5:
            print("신호기 정보:")
            for i in range(1, n + 1):
                a, b = map(int, lines[i].split())
                print(f"  {i}번: 비용={a}, 범위={b}")
    
    # 실행
    result = subprocess.run(
        ["python3", "solution.py"],
        stdin=open(test_file, 'r'),
        capture_output=True,
        text=True
    )
    
    print(f"출력: {result.stdout.strip()}")
    
    if result.stderr:
        print(f"에러: {result.stderr}")