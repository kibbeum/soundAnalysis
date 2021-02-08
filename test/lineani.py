import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

X_MIN = -6
X_MAX = 6
Y_MIN = -1
Y_MAX = 1
X_VALS = range(X_MIN, X_MAX+1) # possible x values for the line


def update_line(num, line):
    print("yes")
    i = X_VALS[num]
    line.set_data( [i, i], [Y_MIN, Y_MAX])
    return line,

fig = plt.figure()

x = np.arange(X_MIN, X_MAX, 0.1);
y = np.sin(x)

plt.scatter(x, y)

l , v = plt.plot(-6, -1, 6, 1, linewidth=2, color= 'red')

plt.xlim(X_MIN, X_MAX)
plt.ylim(Y_MIN, Y_MAX)
plt.xlabel('x')
plt.ylabel('y = sin(x)')
plt.title('Line animation')

line_anim = animation.FuncAnimation(fig, update_line, len(X_VALS), fargs=(l, ))


#line_anim.save('line_animation.gif', writer='imagemagick', fps=4);

plt.show()