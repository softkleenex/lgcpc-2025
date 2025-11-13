# 그리디가 틀릴 수 있는 하드 케이스 생성

# 케이스 1: 비싼 신호기 하나 vs 저렴한 신호기 여러 개
test1 = """6
200 10
1 1
1 1  
1 1
1 1
1 1
1 2 1
2 3 1
3 4 1
4 5 1
5 6 1"""

# 이 경우:
# 신호기 1만 사용: 비용 200 (1부터 거리 10 이내 모두 커버)
# 신호기 2,3,4,5,6 사용: 비용 5
# 최적해는 5

with open("hard1.txt", "w") as f:
    f.write(test1.strip())

# 케이스 2: 겹치는 범위가 많은 경우
test2 = """5
100 3
50 2
50 2
50 2
100 3
1 2 1
2 3 1
3 4 1
4 5 1"""

# 이 경우:
# 1번: 1,2,3,4 커버
# 2번: 1,2,3,4 커버
# 3번: 1,2,3,4,5 커버
# 4번: 2,3,4,5 커버
# 5번: 2,3,4,5 커버
# 최적해: 3번만 = 50

with open("hard2.txt", "w") as f:
    f.write(test2.strip())

# 케이스 3: 필수 신호기 트릭
test3 = """4
100 0
1 100
100 0
1 100
1 2 1
2 3 1
3 4 1"""

# 이 경우:
# 1번: 1만 커버
# 2번: 모두 커버
# 3번: 3만 커버
# 4번: 모두 커버
# 최적해: 2번 또는 4번 = 1

with open("hard3.txt", "w") as f:
    f.write(test3.strip())

import subprocess

tests = [
    ("hard1.txt", "비싼 하나 vs 저렴한 여러개"),
    ("hard2.txt", "겹치는 범위"),
    ("hard3.txt", "필수 신호기 트릭")
]

for filename, desc in tests:
    print(f"\n=== {desc} ===")
    
    # 완전탐색으로 정답 구하기 (N이 작으므로)
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    n = int(lines[0])
    a = [0] * (n+1)
    b = [0] * (n+1)
    
    for i in range(1, n+1):
        a[i], b[i] = map(int, lines[i].split())
    
    print(f"N = {n}")
    for i in range(1, n+1):
        print(f"  신호기 {i}: 비용={a[i]}, 범위={b[i]}")
    
    # 현재 솔루션 실행
    result = subprocess.run(
        ["python3", "solution.py"],
        stdin=open(filename, 'r'),
        capture_output=True,
        text=True
    )
    print(f"솔루션 결과: {result.stdout.strip()}")