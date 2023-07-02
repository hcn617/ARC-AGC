def solve():
    N = int(input())
    S = input()
    for i in range(N - 1):
        A, B = S[:i + 1], S[i + 1:]
        if A < B:
            return True
    return False


T = int(input())
for _ in range(T):
    if solve():
        print("Yes")
    else:
        print("No")
