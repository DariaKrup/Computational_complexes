import scipy.optimize as opt
from tolsolvty import tolsolvty
import numpy as np
import matplotlib.pyplot as plt

A_first = np.array([[10, -11, -12], [1.1, 0, 0], [-5, 11, 12]])
c = [0, 0, 0, 1, 1, 1]
inf_b = np.array([-1, -5, 6])
sup_b = np.array([1, -3, 8])
#[tolmax, argmax, envs, ccode, f1] = tolsolvty(A_first, A_first, inf_b, sup_b)
C = [[10, -11, -12, -1, 0, 0],
     [1.1, 0, 0, 0, -1, 0],
     [-5, 11, 12, 0, 0, -1],
     [-10, 11, 12, -1, 0, 0],
     [-1.1, 0, 0, 0, -1, 0],
     [5, -11, -12, 0, 0, -1]]
r = [0, -4, 7, 0, 4, -7]

#1.6
bounds = ((None, None), (None, None), (None, None), (None, None), (None, None), (None, None))
res = opt.linprog(c, A_ub=C, b_ub=r, bounds=bounds, method='interior-point')
print('Interior-method results:')
print('x: (' + str(np.around(res.x[0],decimals=4)) + ',' + str(np.around(res.x[1], decimals=4))
      + ',' + str(np.around(res.x[2], decimals=4)) + ')')
print('w: (' + str(np.around(res.x[3], decimals=4)) + ',' + str(np.around(res.x[4], decimals=4))
      + ',' + str(np.around(res.x[5], decimals=4)) + ')')

#0.6045
bounds = ((None, None), (0.5807, None), (None, None), (None, None), (None, None), (None, None))
res_simpl = opt.linprog(c, A_ub=C, b_ub=r, bounds=bounds, method='simplex')
print('Simplex results:')
print('x: (' + str(res_simpl.x[0]) + ',' + str(res_simpl.x[1]) + ',' +
      str(np.around(res_simpl.x[2], decimals=4)) + ')')
print('w: (' + str(res_simpl.x[3]) + ',' + str(np.around(res_simpl.x[4], decimals=4)) + ','
      + str(np.around(res_simpl.x[5], decimals=4)) + ')')



bounds_none = ((None, None), (None, None), (None, None), (None, None), (None, None), (None, None))
steps = np.arange(0, 2, 0.1)
points_2 = []
points_3 = []
simplex_2 = []
simplex_3 = []
index = 0
for i in steps:
    bounds = ((None, None), (i, None), (i, None), (None, None), (None, None), (None, None))
    res_p = opt.linprog(c, A_ub=C, b_ub=r, bounds=bounds, method='interior-point')
    res_s = opt.linprog(c, A_ub=C, b_ub=r, bounds=bounds, method='simplex')
    points_2.append(res_p.x[1])
    simplex_2.append(res_s.x[1])
    points_3.append(res_p.x[2])
    simplex_3.append(res_s.x[2])
    index = index + 1
plt.figure()

plt.subplot(2, 1, 1)
plt.plot(steps, points_2, label='Interior-point')
plt.plot(steps, simplex_2, label='Simplex')
plt.legend()
plt.title('Changing of lowest bound of both 2-rd coordinate')

plt.subplot(2, 1, 2)
plt.plot(steps, points_3, label='Interior-point')
plt.plot(steps, simplex_3, label='Simplex')
plt.legend()
plt.title('Changing of lowest bound of both 3-rd coordinate')
plt.savefig('points_b_changing.png', format='png')
plt.show()