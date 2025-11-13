MOD = 1000000007

k = int(input())
n = input().strip()

def f(x):
    s = str(x)
    r = ''.join(c for c in s if c != str(k))
    return int(r) if r else 0

# 작은 수는 브루트포스
if len(n) <= 6:
    print(sum(f(i) for i in range(1, int(n)+1)) % MOD)
else:
    # digit DP
    dp = {}
    
    def go(idx, tight, cnt, val, start):
        if idx == len(n):
            return val if start else 0
        
        if cnt > 18: cnt = 18  # 메모리 최적화
        key = (idx, tight, cnt, val % MOD, start)
        if key in dp:
            return dp[key]
        
        lim = int(n[idx]) if tight else 9
        ans = 0
        
        for d in range(0, lim+1):
            if not start and d == 0:
                ans = (ans + go(idx+1, False, 0, 0, False)) % MOD
            elif d == k:
                ans = (ans + go(idx+1, tight and d==lim, cnt, val, True)) % MOD
            else:
                ans = (ans + go(idx+1, tight and d==lim, cnt+1, (val*10+d)%MOD, True)) % MOD
        
        dp[key] = ans
        return ans
    
    print(go(0, True, 0, 0, False))