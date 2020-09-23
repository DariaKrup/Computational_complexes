import numpy as np


def mid(matrix):
    n = len(matrix)
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            M[i][j] = (matrix[i][j][0] + matrix[i][j][1]) / 2
    return M


def rad(matrix):
    n = len(matrix)
    R = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            R[i][j] = (matrix[i][j][1] - matrix[i][j][0]) / 2
    return R


def beck_criteria(matrix):
    M = mid(matrix)
    R = rad(matrix)
    M_inv = np.linalg.inv(M)
    M_inv = np.abs(M_inv)

    A = M_inv.dot(R)
    eig = np.abs(np.linalg.eigvals(A))
    rho = np.max(eig)

    result = ''
    if rho < 1:
        result = 'false, non-special matrix'
    else:
        result = 'undefined'

    return result, rho


def diag_max_criteria(matrix):
    n = len(matrix)
    M = mid(matrix)
    R = rad(matrix)
    M_inv = np.linalg.inv(M)
    M_inv = np.abs(M_inv)
    A = R.dot(M_inv)

    dMax = A[0][0]
    for i in range(1, n):
        if dMax < A[i][i]:
            dMax = A[i][i]

    result = ''
    if dMax >= 1:
        result = 'true, special matrix'
    else:
        result = 'undefined'
    #print('Max in diagonal = ', np.around(dMax, decimals=2))
    #print('Matrix is special:', result)
    return result, dMax


def create_int_matrix(size, epsilon):
    matrix_int = [[(0, 0) for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            if i != j:
                matrix_int[i][j] = (0, epsilon)
            else:
                matrix_int[i][j] = (1, 1)
    return matrix_int


if __name__ == "__main__":
    print('Task first.')
    print('Enter epsilon: ')
    eps = float(input())
    matrix = [[(1 - eps, 1 + eps), (1 - eps, 1 + eps)], [(1.1 - eps, 1.1 + eps), (1 - eps, 1 + eps)]]
    result_beck, rho = beck_criteria(matrix)
    result_diag, dmax = diag_max_criteria(matrix)
    print('Beck criteria result:', result_beck, '; rho = ', np.around(rho, decimals=3))
    print('Diag max criteria result:', result_diag, '; max in diagonal = ', np.around(dmax, decimals=3))

    print('\nTask second. ')
    print('Enter dimension: ')
    size = int(input())
    eps = 0
    stop = True
    while stop:
        matrix_int = create_int_matrix(size, eps)
        result_beck, rho = beck_criteria(matrix_int)
        result_diag, dmax = diag_max_criteria(matrix_int)
        if result_beck == 'undefined' and result_diag == 'true, special matrix':
            print('Found epsilon:', np.around(eps, decimals=3))
            stop = False
            print('Beck criteria result:', result_beck, '; rho = ', np.around(rho, decimals=3))
            print('Diag max criteria result:', result_diag, '; max in diagonal = ', np.around(dmax, decimals=3))
        eps += 0.01



