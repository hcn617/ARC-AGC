from heapq import heappop, heappush

N = int(input())
que = []
for _ in range(N):
    a, b = map(int, input().split())
    heappush(que, (b - a, a, b))

ans = 0
while que:
    # Alice turn
    dist, a, b = heappop(que)
    heappush(que, (-dist, b, a))

    # Bob turn
    dist, a, b = heappop(que)
    ans += a

print(ans)
