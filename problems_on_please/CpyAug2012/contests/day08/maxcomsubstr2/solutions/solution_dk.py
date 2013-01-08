#!/usr/bin/python3

fin = open("maxcommonsubstr.in", "r")
fout = open("maxcommonsubstr.out", "w")

POW = 179
MOD = 10 ** 17 + 3
A = fin.readline().rstrip()
LA = len(A)
B = fin.readline().rstrip()
LB = len(B)
n = max(LA, LB)
Powers = [1] + [0] * n
HashA = [0] * (LA + 1)
HashB = [0] * (LB + 1)
for i in range(1, n + 1):
    Powers[i] = Powers[i - 1] * POW % MOD
for i in range(1, LA + 1):
    HashA[i] = (HashA[i - 1] * POW + ord(A[i - 1])) % MOD
for i in range(1, LB + 1):
    HashB[i] = (HashB[i - 1] * POW + ord(B[i - 1])) % MOD

def Hash(H, i, j): # Hash of S[a:b]
    return (H[j] - H[i] * Powers[j - i]) % MOD

def Solve(L, A, B, HashA, HashB):
    Hashes = set()
    for i in range(L, len(A) + 1):
        Hashes.add(Hash(HashA, i - L, i))
    for i in range(L, len(B) + 1):
        if Hash(HashB, i - L, i) in Hashes:
            return True
    return False

left = 0
right = min(len(A), len(B)) + 1
while right - left > 1:
    middle = (left + right) // 2
    if Solve(middle, A, B, HashA, HashB):
        left = middle
    else:
        right = middle
fout.write(str(left) + "\n")
fin.close()
fout.close()

