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


def min_from_4(a, b, c, d):
    return min(min(min(a, b), c), d)


def max_from_4(a, b, c, d):
    return max(max(max(a, b), c), d)


def mul_intervals(tuple_f, tuple_s):
    f_low, f_up = tuple_f[0], tuple_f[1]
    s_low, s_up = tuple_s[0], tuple_s[1]
    return min_from_4(f_low * s_low, f_low * s_up, f_up * s_low, f_up * s_up), \
           max_from_4(f_low * s_low, f_low * s_up, f_up * s_low, f_up * s_up)


def sup_intervals(tuple_f, tuple_s):
    return tuple_f[0] - tuple_s[1], tuple_f[1] - tuple_s[0]


def sum_intervals(tuple_f, tuple_s):
    return tuple_f[0] + tuple_s[0], tuple_f[1] + tuple_s[1]


def determinant_2(matrix):
    return sup_intervals(mul_intervals(matrix[0][0], matrix[1][1]), mul_intervals(matrix[0][1], matrix[1][0]))


def determinant_3(matrix):
    first_one = mul_intervals(matrix[0][0], sup_intervals(mul_intervals(matrix[1][1], matrix[2][2]), mul_intervals(matrix[1][2], matrix[2][1])))
    second_one = mul_intervals(matrix[0][1], sup_intervals(mul_intervals(matrix[1][0], matrix[2][2]), mul_intervals(matrix[2][0], matrix[1][2])))
    third_one = mul_intervals(matrix[0][2], sup_intervals(mul_intervals(matrix[1][0], matrix[2][1]), mul_intervals(matrix[2][0], matrix[1][1])))
    return sum_intervals(sup_intervals(first_one, second_one), third_one)


def determinant_4(matrix, epsilon):
    matrix_f = create_int_matrix(3, epsilon)
    first_one = mul_intervals(matrix[0][0], determinant_3(matrix_f))
    matrix_s = [[(0, epsilon), (0, epsilon), (0, epsilon)], [(0, epsilon), (1, 1), (0, epsilon)], [(0, epsilon), (0, epsilon), (1, 1)]]
    second_one = mul_intervals(matrix[0][1], determinant_3(matrix_s))
    matrix_t = [[(0, epsilon), (1, 1), (0, epsilon)], [(0, epsilon), (0, epsilon), (0, epsilon)], [(0, epsilon), (0, epsilon), (1, 1)]]
    third_one = mul_intervals(matrix[0][2], determinant_3(matrix_t))
    matrix_f = [[(0, epsilon), (1, 1), (0, epsilon)], [(0, epsilon), (0, epsilon), (1, 1)], [(0, epsilon), (0, epsilon), (0, epsilon)]]
    forth_one = mul_intervals(matrix[0][3], determinant_3(matrix_f))
    return sum_intervals(sup_intervals(first_one, second_one), sup_intervals(third_one, forth_one))


if __name__ == "__main__":
    print('Task first.')
    print('Enter epsilon: ')
    eps = float(input())
    matrix = [[(1 - eps, 1 + eps), (1 - eps, 1 + eps)], [(1.1 - eps, 1.1 + eps), (1 - eps, 1 + eps)]]
    result_beck, rho = beck_criteria(matrix)
    result_diag, dmax = diag_max_criteria(matrix)
    print('Beck criteria result:', result_beck, '; rho = ', np.around(rho, decimals=3))
    print('Diag max criteria result:', result_diag, '; max in diagonal = ', np.around(dmax, decimals=3))
    det = determinant_2(matrix)
    print('Determinant: (', np.around(det[0], decimals=5), ', ', np.around(det[1], decimals=5), ')')
    eps = 0
    stop = True
    while stop:
        matrix = [[(1 - eps, 1 + eps), (1 - eps, 1 + eps)], [(1.1 - eps, 1.1 + eps), (1 - eps, 1 + eps)]]
        det_2 = determinant_2(matrix)
        if det_2[0] * det_2[1] < 0:
            print('Determinant: (', np.around(det_2[0], decimals=5), ', ', np.around(det_2[1], decimals=5), ')')
            print('Found epsilon:', np.around(eps, decimals=3))
            stop = False
        eps += 0.001



    print('\nTask second. ')
    print('Enter dimension: ')
    size = int(input())
    eps = 0
    stop = True
    while stop:
        matrix_int = create_int_matrix(size, eps)
        if size == 3:
            det_3 = determinant_3(matrix_int)
        else:
            det_3 = determinant_4(matrix_int, eps)
        if det_3[0] * det_3[1] <= 0:
            print('Determinant: (', np.around(det_3[0], decimals=5), ', ', np.around(det_3[1], decimals=5), ')')
            print('Found epsilon:', np.around(eps, decimals=3))
            stop = False
        result_beck, rho = beck_criteria(matrix_int)
        result_diag, dmax = diag_max_criteria(matrix_int)
        if result_beck == 'undefined' and result_diag == 'true, special matrix':
            print('Found epsilon:', np.around(eps, decimals=3))
            stop = False
            print('Beck criteria result:', result_beck, '; rho = ', np.around(rho, decimals=3))
            print('Diag max criteria result:', result_diag, '; max in diagonal = ', np.around(dmax, decimals=3))
        eps += 0.01


