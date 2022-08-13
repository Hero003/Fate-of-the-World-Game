T = int(input())
ans = []
for i in range(T):
    X = list(map(int, input().split()))
    if X[0] > X[1]:
        ans.append("A")
    else:
        ans.append("B")
print(*ans , sep="\n")