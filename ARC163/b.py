N, M = map(int, input().split())
A = list(map(int, input().split()))

l, r = A[0], A[1]

A = A[2:]
A.sort()

ans = 1 << 80
for i in range(N - 2):
    j = i + M - 1
    if j == N - 2:
        break
    left, right = A[i], A[j]
    val = 0
    if left < l:
        val += l - left
    if r < right:
        val += right - r
    ans = min(ans, val)

print(ans)
