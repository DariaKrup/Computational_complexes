import tolsolvty as t
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

infA = np.array([[11, 13], [15, 17], [21, 10]])
supA = np.array([[15, 17], [21, 21], [25, 14]])
infb = np.array([[7], [10.8], [11.9]])
supb = np.array([[12], [14.8], [15.9]])
x = np.arange(-0.5, 0.5, 0.01)
y = np.arange(-0.5, 0.5, 0.01)
sh = x.shape[0]
z = np.zeros((sh, sh))
#[tolmax, argmax, envs, ccode] = t.tolsolvty(infA, supA, infb, supb)
for i in range(sh):
    for j in range(sh):
        array = np.array([[x[i]], [y[j]]])
        [tolmax, argmax, envs, ccode, z[i, j]] = t.tolsolvty(array, infA, supA, infb, supb)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')
ax.set_xlabel('x_1')
ax.set_ylabel('x_2')
ax.set_zlabel('Tol(x_1, x_2)')
plt.savefig('Tol(x_1, x_2)' +'.png', format='png')
plt.show()