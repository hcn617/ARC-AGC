class LinearSieve():

    def __init__(self, n_max):
        self.n_max = n_max
        self.__build()

    def __build(self):
        self.arr = [i for i in range(self.n_max + 1)]
        self.arr[0] = -1
        self.arr[1] = -1
        for i in range(2, self.n_max + 1):
            # これ以降は、iが最小の素因数になることはないので、breakする。
            if i * i > self.n_max:
                break

            # iが素数でないときはcontinue
            if self.arr[i] != i:
                continue

            num = i + i
            while num <= self.n_max:
                if self.arr[num] == num:
                    self.arr[num] = i
                num += i

    def is_prime(self, num: int) -> bool:
        assert 1 <= num <= self.n_max
        return self.arr[num] == num

    def factorization(self, num: int) -> list:
        assert 2 <= num <= self.n_max
        min_divisor = -2
        ret = []
        while num > 1:
            divisor = self.arr[num]
            if min_divisor == divisor:
                ret[-1][1] += 1
            else:
                ret.append([divisor, 1])
                min_divisor = divisor
            num //= divisor
        return ret


'''
tatyamさん作の、SortedSetです。
使わせていただき、ありがとうございます！
https://github.com/tatyam-prime/SortedSet/blob/main/SortedSet.py

・使い方(個人的まとめ)
s=SortedSet()
s.a: SortedSetの中身を返す。
len(s), x in s, x not in s: リストと同じ要領で使える。
s.add(x): xを追加してTrueを返す。ただしxがすでにs内にある場合、xは追加せずにFalseを返す。
s.discard(x): xを削除してTrueを返す。ただしxがs内にない場合、何もせずにFalseを返す。
s.lt(x): xより小さい最大の要素を返す。もし存在しないなら、Noneを返す。
s.le(x): x　以下の　最大の要素を返す。もし存在しないなら、Noneを返す。
s.gt(x): xより大きい最小の要素を返す。もし存在しないなら、Noneを返す。
s.ge(x): x　以上の　最小の要素を返す。もし存在しないなら、Noneを返す。
s.index(x): xより小さい要素の数を返す。
s.index_right(x): x以下の要素の数を返す。

・使い方URL
https://github.com/tatyam-prime/SortedSet
'''

# https://github.com/tatyam-prime/SortedSet/blob/main/SortedSet.py
import math
from bisect import bisect_left, bisect_right
from typing import Generic, Iterable, Iterator, TypeVar, Union, List

T = TypeVar('T')


class SortedSet(Generic[T]):
    BUCKET_RATIO = 50
    REBUILD_RATIO = 170

    def _build(self, a=None) -> None:
        "Evenly divide `a` into buckets."
        if a is None: a = list(self)
        size = self.size = len(a)
        bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
        self.a = [a[size * i // bucket_size: size * (i + 1) // bucket_size] for
                  i in range(bucket_size)]

    def __init__(self, a: Iterable[T] = []) -> None:
        "Make a new SortedSet from iterable. / O(N) if sorted and unique / O(N log N)"
        a = list(a)
        if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
            a = sorted(set(a))
        self._build(a)

    def __iter__(self) -> Iterator[T]:
        for i in self.a:
            for j in i: yield j

    def __reversed__(self) -> Iterator[T]:
        for i in reversed(self.a):
            for j in reversed(i): yield j

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return "SortedSet" + str(self.a)

    def __str__(self) -> str:
        s = str(list(self))
        return "{" + s[1: len(s) - 1] + "}"

    def _find_bucket(self, x: T) -> List[T]:
        "Find the bucket which should contain x. self must not be empty."
        for a in self.a:
            if x <= a[-1]: return a
        return a

    def __contains__(self, x: T) -> bool:
        if self.size == 0: return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        return i != len(a) and a[i] == x

    def add(self, x: T) -> bool:
        "Add an element and return True if added. / O(√N)"
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return True
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x: return False
        a.insert(i, x)
        self.size += 1
        if len(a) > len(self.a) * self.REBUILD_RATIO:
            self._build()
        return True

    def discard(self, x: T) -> bool:
        "Remove an element and return True if removed. / O(√N)"
        if self.size == 0: return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i == len(a) or a[i] != x: return False
        a.pop(i)
        self.size -= 1
        if len(a) == 0: self._build()
        return True

    def lt(self, x: T) -> Union[T, None]:
        "Find the largest element < x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]

    def le(self, x: T) -> Union[T, None]:
        "Find the largest element <= x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]

    def gt(self, x: T) -> Union[T, None]:
        "Find the smallest element > x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] > x:
                return a[bisect_right(a, x)]

    def ge(self, x: T) -> Union[T, None]:
        "Find the smallest element >= x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] >= x:
                return a[bisect_left(a, x)]

    def __getitem__(self, x: int) -> T:
        "Return the x-th element, or IndexError if it doesn't exist."
        if x < 0: x += self.size
        if x < 0: raise IndexError
        for a in self.a:
            if x < len(a): return a[x]
            x -= len(a)
        raise IndexError

    def index(self, x: T) -> int:
        "Count the number of elements < x."
        ans = 0
        for a in self.a:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans

    def index_right(self, x: T) -> int:
        "Count the number of elements <= x."
        ans = 0
        for a in self.a:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return ans


def solve():
    N = int(input())
    if N == 1:
        print("Yes")
        print(1)
        return

    if N == 2:
        print("No")
        return

    print("Yes")

    ss = SortedSet([2, 3, 6])
    gar = set()
    while len(ss) + len(gar) < N:
        val = ss.ge(0)
        ft = ls.factorization(val)
        p = [1]
        for prime, cnt in ft:
            for el in p[:]:
                for i in range(1, cnt + 1):
                    p.append(el * prime ** i)
        q = []
        for el in p:
            if el * el > val:
                continue
            el2 = val // el
            a, b = (el + el2) * el, (el + el2) * el2
            q.append((b, a))
        q.sort()
        discard_flag = False
        for el2, el in q:
            if el == el2:
                continue
            if el not in ss and el2 not in ss:
                ss.add(el)
                ss.add(el2)
                discard_flag = True
                # print(f'{el=},{el2=}')
                break
        if discard_flag:
            ss.discard(val)
        else:
            ss.discard(val)
            gar.add(val)
            # print(f'{gar=}')

    for el in gar:
        print(el, end=" ")
    for el in ss:
        print(el, end=" ")
    print("")


T = int(input())
dic = dict()
ls = LinearSieve(10 ** 5)
for _ in range(T):
    solve()
