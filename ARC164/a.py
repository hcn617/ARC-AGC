def solve():
    N, K = map(int, input().split())
    min_cnt = 0
    while N:
        N, mo = divmod(N, 3)
        min_cnt += mo

    if min_cnt <= K and min_cnt % 2 == K % 2:
        print("Yes")
    else:
        print("No")
    return


T = int(input())
for _ in range(T):
    solve()
