import numpy as np
import matplotlib.pyplot as plt

A = np.array([[[2, 4], [-2, 1]],
              [[-2, 1], [2, 4]]])
d_low = np.array([-2, -2])
d_up = np.array([2, 2])


def min_from_4(a, b, c, d):
    return min(min(min(a, b), c), d)


def max_from_4(a, b, c, d):
    return max(max(max(a, b), c), d)


def mul_intervals(f_low, f_up, s_low, s_up):
    return min_from_4(f_low * s_low, f_low * s_up, f_up * s_low, f_up * s_up), \
           max_from_4(f_low * s_low, f_low * s_up, f_up * s_low, f_up * s_up)


def sum_intervals(list):
    result = [0, 0]
    for interval in list:
        result[0] += interval[0]
        result[1] += interval[1]
    return result[0], result[1]


def get_sti(vector_low, vector_up):
    return np.append(-vector_low, vector_up)


def sti_reversed(vector):
    middle = vector.shape[0] // 2
    return -vector[:middle], vector[middle:]


def get_g(vector, C, d):
    applied_sti_low, applied_sti_up = sti_reversed(vector)
    C_sti_vector = [sum_intervals([mul_intervals(C[i][j][0], C[i][j][1], applied_sti_low[j], applied_sti_up[j])
                                   for j in range(len(applied_sti_low))]) for i in range(len(C))]
    high_matrix = []
    low_matrix = []
    for interval in C_sti_vector:
        low_matrix.append(interval[0])
        high_matrix.append(interval[1])
    return get_sti(np.array(low_matrix), np.array(high_matrix)) - d


def dx_pos(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0.9
    else:
        return 0


def dx_neg(x):
    if x < 0:
        return -1
    elif x == 0:
        return -0.9
    else:
        return 0


def pos(x):
    return x if x > 0 else 0


def neg(x):
    return -x if x < 0 else 0


def dmax_first(A, i, j, x):
    n = x.shape[0] // 2
    prod_1 = pos(A[i][j][1]) * pos(x[j])
    prod_2 = neg(A[i][j][0]) * pos(x[j+n])
    if prod_1 > prod_2:
        return pos(A[i][j][1]), 0
    elif prod_1 == prod_2:
        return 0.1 * pos(A[i][j][1]), 0.1 * neg(A[i][j][0])
    else:
        return 0, neg(A[i][j][0])


def dmax_second(A, i, j, x):
    n = x.shape[0] // 2
    prod_1 = pos(A[i][j][1]) * pos(x[j+n])
    prod_2 = neg(A[i][j][0]) * pos(x[j])
    if prod_1 > prod_2:
        return 0, pos(A[i][j][1])
    elif prod_1 == prod_2:
        return 0.1 * neg(A[i][j][0]), 0.1 * pos(A[i][j][1])
    else:
        return neg(A[i][j][0]), 0


def dF(C, i, x):
    n = x.shape[0] // 2
    res = np.zeros(2 * n)
    if 0 <= i < n:
        for j in range(0, n):
            temp = dmax_first(C, i, j, x)
            res_1 = pos(C[i][j][0]) * dx_neg(x[j]) + neg(C[i][j][1]) * dx_neg(x[j+n]) - temp[0]
            res_2 = pos(C[i][j][0]) * dx_neg(x[j]) + neg(C[i][j][1]) * dx_neg(x[j+n]) - temp[1]
            res[j] -= res_1
            res[j+n] -= res_2
    else:
        i -= n
        for j in range(0, n):
            temp = dmax_second(C, i, j, x)
            res_1 = temp[0] - pos(C[i][j][0]) * dx_neg(x[j+n]) - neg(C[i][j][1]) * dx_neg(x[j])
            res_2 = temp[1] - pos(C[i][j][0]) * dx_neg(x[j+n]) - neg(C[i][j][1]) * dx_neg(x[j])
            res[j] += res_1
            res[j+n] += res_2
    return res


def get_sub_grad(C, vector):
    n = vector.shape[0]
    D = np.zeros((n, n))
    for i in range(0, n):
        D[i][:] = dF(C, i, vector)
    return D


def sub_grad_2(A, b_inf, b_sup, eps):
    sti_b = get_sti(b_inf, b_sup)
    x = np.zeros_like(sti_b)

    prev_g = get_g(x, A, sti_b)
    iter_count = 0
    while np.linalg.norm(prev_g) > eps:
        iter_count += 1
        sub_grad = get_sub_grad(A, x)
        func_g = get_g(x, A, sti_b)
        #print(np.linalg.det(sub_grad))
        x = np.subtract(x, np.linalg.inv(sub_grad).dot(func_g))
        print(x)
        prev_g = func_g
    return sti_reversed(x), iter_count

# First task
eps_s = [1e-3, 1e-5, 1e-10]
for eps in eps_s:
    print('Accuracy: ' + str(eps))
    (x_inf, x_sup), iterations = sub_grad_2(A, d_low, d_up, eps)
    for i in range(len(x_inf)):
        print('[' + str(x_inf[i]) + ', ' + str(x_sup[i]) + ']')
    print('Quantity of iterations: ' + str(iterations))
    print()


eps_0 = 0.01
iters = []
x = []
for i in range(18):
    x.append(eps_0)
    (x_inf, x_sup), iterations = sub_grad_2(A, d_low, d_up, eps_0)
    iters.append(iterations)
    eps_0 /= 10
plt.plot(x, iters)
plt.xlabel('Accuracy')
plt.ylabel('Quantity of iterations')
plt.savefig('iterations.png', format='png')
plt.show()


def plot_result(x, x_sup, x_inf, A, b_low, b_up, title):
    plt.plot(np.dot(A, x_inf), label='A * x_inf', color='darkblue')
    plt.plot(np.dot(A, x_sup), label='A * x_sup', color='deepskyblue')
    plt.plot(np.dot(A, x), label='b', color='aquamarine')
    plt.plot(b_low, label='b_inf', ls='--', color='lawngreen')
    plt.plot(b_up, label='b_sup', ls='--', color='yellow')
    plt.legend()
    plt.title('Results')
    plt.grid()
    plt.savefig(title + '.png', format='png')
    plt.show()


def plot_x(x, x_inf, x_sup):
    plt.figure(figsize=(18, 8))
    plt.plot(x, label='s_new', color='darkred')
    plt.plot(x_inf, label='x_inf', color='orchid')
    plt.plot(x_sup, label='x_sup', color='indigo')
    plt.xlabel('index')
    plt.ylabel('value')
    plt.title('Сравнение полученного решения с исходным')
    plt.legend()
    plt.grid()
    plt.savefig('w_s_new' + '.png', format='png')
    plt.show()


# Second part
files = ['matrix_n_phi_1.txt', 'matrix_n_phi_6.txt']
title = ['matrix_n_phi_1', 'matrix_n_phi_6']
i = 0
for file in files:
    matrix = np.loadtxt(file)
    matrix = np.array(matrix[:128, :])
    # Delete null columns
    null_columns = []
    for i in range(matrix.shape[1]):
        count = 0
        for j in range(matrix.shape[0]):
            if matrix[j][i] == 0:
                count += 1
        if count == matrix.shape[0]:
            null_columns.append(i)
    matrix = np.delete(matrix, null_columns, axis=1)
    print(matrix.shape[0], matrix.shape[1])

    # Leave most filled lines
    counters = np.zeros(matrix.shape[0])
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] != 0:
                counters[i] += 1

    deleting = []
    not_10 = False
    for i in range(len(counters)):
        if counters[i] < 11:
            #if counters[i] == 10 and not not_10:
            #    not_10 = True
            #    continue
            deleting.append(i)
    #for j in range(len(deleting)):
     #   deleting[j] += 1
    rand = np.random.randint(0, len(deleting) - 1)
    print(rand)
    deleting.pop(rand)
    row = deleting[0]
    matrix = np.delete(matrix, deleting, axis=0)
    first = np.random.randint(0, matrix.shape[1])
    second = np.random.randint(0, matrix.shape[1])
    #matrix = np.rot90(matrix)
    for i in range(matrix.shape[1]):
       matrix[i][first], matrix[i][second] = matrix[i][second], matrix[i][first]
    print('Determinant of cut matrix: ' + str(np.linalg.det(matrix)))
    #np.savetxt('matrix.txt', matrix)


    """cor_lim = 0.6
    deleting = []
    for i in range(matrix.shape[0] - 1):
        if pearsonr(matrix[i][:], matrix[i + 1][:])[0] > cor_lim:
            deleting.append(i)
    deleting.pop(len(deleting) // 4)
    matrix = np.delete(matrix, deleting, axis=0)
    print(matrix.shape[0], matrix.shape[1])
    print(np.linalg.matrix_rank(matrix))
    np.random.shuffle(matrix)
    print('Determinant of cut matrix: ' + str(np.linalg.det(matrix)))
    np.savetxt('matrix.txt', matrix)"""


    n = matrix.shape[0]
    x = np.random.uniform(low=0.5, high=2, size=n)
    print('x: ', x)
    b = matrix.dot(x)
    rad = np.random.uniform(low=1.5, high=3, size=n)
    print('rad:', rad)
    matrix_m = []
    for i in range(len(matrix)):
        array = []
        for j in range(n):
            rad_m = np.random.random(1)
            array.append(np.append(matrix[i][j] - rad_m, matrix[i][j] + rad_m))
        matrix_m.append(array)
    b_low = b - rad
    b_up = b + rad


    eps = 1e-5
    (x_inf, x_sup), iterations = sub_grad_2(matrix_m, b_low, b_up, eps)
    for i in range(len(x_inf)):
        print('[' + str(x_inf[i]) + ', ' + str(x_sup[i]) + ']')
    print('Quantity of iterations: ' + str(iterations))
    print()

    plot_result(x, x_sup, x_inf, A, b_low, b_up, title[i])
    i += 1

size = 18

b = np.array(np.loadtxt('bnew.txt'))
b = b[row: row + size]
rads = np.random.uniform(low=0.5, high=2, size=size)
b_inf = b - rads  # make b interval
b_sup = b + rads
x = np.array(np.loadtxt('snew.txt'))[:size]
print(x.shape[0])

x_inf, x_sup = sub_grad_2(A, b_inf, b_sup, 1e-5)
plot_x(x, x_sup, x_inf)
