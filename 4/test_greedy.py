# 그리디가 실패할 수 있는 케이스 테스트

test_cases = []

# 테스트 1: 그리디가 틀릴 수 있는 케이스
# 5개 정점 체인
test1 = """5
1 2
100 10
1 2
1 3
1 1
1 2 1
2 3 1
3 4 1
4 5 1"""

# 테스트 2: 스타 트리
test2 = """7
100 3
10 1
10 1
10 1
10 1
10 1
10 1
1 2 1
1 3 1
1 4 1
1 5 1
1 6 1
1 7 1"""

# 테스트 3: 비용 0인 신호기가 범위도 0인 경우
test3 = """3
0 0
100 100
0 0
1 2 1
2 3 1"""

test_cases = [
    ("test_greedy1.txt", test1, "체인에서 그리디 테스트"),
    ("test_greedy2.txt", test2, "스타 트리에서 그리디 테스트"),
    ("test_greedy3.txt", test3, "비용 0 범위 0 테스트")
]

for filename, content, desc in test_cases:
    with open(filename, 'w') as f:
        f.write(content.strip())
    print(f"Created {filename}: {desc}")

# 두 가지 알고리즘 비교
import subprocess

for filename, _, desc in test_cases:
    print(f"\n=== {desc} ===")
    with open(filename, 'r') as f:
        lines = f.readlines()
        n = int(lines[0])
        print(f"N = {n}")
        for i in range(1, n+1):
            a, b = map(int, lines[i].split())
            print(f"  신호기 {i}: 비용={a}, 범위={b}")
    
    result = subprocess.run(
        ["python3", "solution.py"],
        stdin=open(filename, 'r'),
        capture_output=True,
        text=True
    )
    print(f"결과: {result.stdout.strip()}")