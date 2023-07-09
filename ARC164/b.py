class dsu():
    """Union-Find

    syakayamiさん作、PythonバージョンのACLよりコピペしたものです。
    使わせていただきありがとうございます！
    https://github.com/shakayami/ACL-for-python/blob/master/dsu.py

    ・使い方(個人的まとめ):
        uf=dsu(N): 初期化(Nは頂点の数)
        uf.merge(a,b): 頂点aがある連結成分と頂点bがある連結成分を合体します。
        uf.same(a,b): 頂点a,bが同じ連結成分ならTrue, そうでないならFalseを返します。
        uf.leader(a): 頂点aの連結成分の代表元を返します。
        uf.size(a): 頂点aの連結成分にある超点数を返します(頂点a自身を含みます)。
        uf.groups(): グラフの連結成分の情報を答えます。

    ・使い方URL
        https://github.com/shakayami/ACL-for-python/wiki/dsu
    """
    n = 1
    parent_or_size = [-1 for i in range(n)]

    def __init__(self, N):
        self.n = N
        self.parent_or_size = [-1 for i in range(N)]

    def merge(self, a, b):
        assert 0 <= a < self.n, "0<=a<n,a={0},n={1}".format(a, self.n)
        assert 0 <= b < self.n, "0<=b<n,b={0},n={1}".format(b, self.n)
        x = self.leader(a)
        y = self.leader(b)
        if x == y:
            return x
        if (-self.parent_or_size[x] < -self.parent_or_size[y]):
            x, y = y, x
        self.parent_or_size[x] += self.parent_or_size[y]
        self.parent_or_size[y] = x
        return x

    def same(self, a, b):
        assert 0 <= a < self.n, "0<=a<n,a={0},n={1}".format(a, self.n)
        assert 0 <= b < self.n, "0<=b<n,b={0},n={1}".format(b, self.n)
        return self.leader(a) == self.leader(b)

    def leader(self, a):
        assert 0 <= a < self.n, "0<=a<n,a={0},n={1}".format(a, self.n)
        if (self.parent_or_size[a] < 0):
            return a
        self.parent_or_size[a] = self.leader(self.parent_or_size[a])
        return self.parent_or_size[a]

    def size(self, a):
        assert 0 <= a < self.n, "0<=a<n,a={0},n={1}".format(a, self.n)
        return -self.parent_or_size[self.leader(a)]

    def groups(self):
        leader_buf = [0 for i in range(self.n)]
        group_size = [0 for i in range(self.n)]
        for i in range(self.n):
            leader_buf[i] = self.leader(i)
            group_size[leader_buf[i]] += 1
        result = [[] for i in range(self.n)]
        for i in range(self.n):
            result[leader_buf[i]].append(i)
        result2 = []
        for i in range(self.n):
            if len(result[i]) > 0:
                result2.append(result[i])
        return result2


N, M = map(int, input().split())
edges = []
for _ in range(M):
    a, b = [int(x) - 1 for x in input().split()]
    edges.append((a, b))
c = list(map(int, input().split()))

uf = dsu(N)
edges2 = []
for a, b in edges:
    if c[a] != c[b]:
        uf.merge(a, b)
    else:
        edges2.append((a, b))
for a, b in edges2:
    if uf.same(a, b):
        print("Yes")
        exit()
print("No")
