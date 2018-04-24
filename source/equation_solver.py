from decimal import *

def linear_solver(*para):
    n = int(len(para) ** 0.5)
    # Create a matrix that present the equation
    # [[52, 96, 30, 94],
    #  [31, 92, 58, 49],
    #  [88, 18, 35, 21]]
    para = [[para[row * (n + 1) + col] for col in range(n + 1)] for row in range(n)]

    # Reduce the matrix, top left * bottom right - top right * bottom left
    # [[52, 96, 30, 94],
    #  [0, 1808, 2086, -366],
    #  [0, -7512, -820, -7180]]
    # Then to
    # [[52, 96, 30, 94],
    #  [0, 1808, 2086, -366],
    #  [0, 0, 14187472, -15730832]]

    for row in range(n):
        for col in range(row + 1, n):
            for h in range(row + 1, n + 1):
                para[col][h] = para[row][row] * para[col][h] - para[row][h] * para[col][row]

    # Devide from bottom up to top to get result
    # [[52, 96, 30, 94], -> [52, 96, 127.26] -> [52, 23.88] -> [0.459]
    #  [0, 1808, 2086, -366], -> [1808, 1946.92] -> [1.076]
    #  [0, 0, 14187472, -15730832] -> [-1.108]

    for row in range(n - 1, -1, -1):
        para[row][n] = para[row][n] / para[row][row]
        for col in range(row - 1, -1, -1):
            para[col][n] -= para[row][n] * para[col][row]

    return [para[row][n] for row in range(n)]

def quad_solver(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta >= 0:
        return (b - delta ** 0.5) / 2, (b + delta ** 0.5) / 2

if __name__ == '__main__':
    print(linear_solver(52, 96, 30, 94, 31, 92, 58, 49, 88, 18, 35, 21))
    print(quad_solver(1, -1, -1))
