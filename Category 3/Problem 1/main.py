T = int(input())
X = []
for i in range(T): X.append(int(input()) % 10)
print(*X , sep="\n")