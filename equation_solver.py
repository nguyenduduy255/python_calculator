from decimal import *

def solver(*para):
    n = int(len(para) ** 0.5)
    p = [[para[i * (n + 1) + j] for j in range(n + 1)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            for h in range(i + 1, n + 1):
                p[j][h] = p[i][i] * p[j][h] - p[i][h] * p[j][i]

    for i in range(n - 1, -1, -1):
        print(i)
        p[i][n] = p[i][n] / p[i][i]
        for j in range(i - 1, -1, -1):
            p[j][n] -= p[i][n]

    return p

print(solver(1, 2, 3, 4, 5, 6))
