"""
Name: Nathan Roberts
PID: A14384608
"""
#imports
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from celluloid import Camera
from mpl_toolkits.mplot3d import Axes3D

MAXPNT = 100

def main(acc, verbose=False):
	#initial conditions
	n = 3 #set number of points
	x = np.zeros(n) #set initial position as 0 as default for all points
	v = np.zeros(n) #set initial velocity as 0 as default for all points
	tnow = 0 #set initial time
	t_history = []

	x[0] = 2
	v[0] = 0

	x[1] = 0
	v[1] = 3

	x[2] = 1
	v[2] = 0
	
	x_history = [[i] for i in x]
	v_history = [[i] for i in v]
	t_history.append(tnow)
	#integration perameters
	max_step = 256
	nout = 4
	dt = 1 / 32

	#looping to perform integration
	for i in range(max_step):
		if (i % nout == 0): #if enough steps have passed, print the state
			if(verbose):
				printstate(x, v, n, tnow)
			x_history = np.append([[i] for i in x], x_history, axis=1)
			v_history = np.append([[i] for i in v], v_history, axis=1)
			t_history.append(tnow)



		x, v = leapstep(acc, x, v, n, dt) #take an integration step
		
		tnow += dt

	if (max_step % nout == 0): #if the last step would have printed
		if(verbose):
			printstate(x, v, n, tnow) #then print
		x_history = np.append([[i] for i in x], x_history, axis=1)
		v_history = np.append([[i] for i in v], v_history, axis=1)
		t_history.append(tnow)


	return x_history, v_history, t_history

def leapstep(acc, x, v, n, dt):
	a = acc(x) #call the acceleration code

	for i in range(n):
		v[i] = v[i] + 0.5 * dt * a[i] #loop over all points and increase the velocities by a half setp

	for i in range(n): #loop again an increase the positions by a full step
		x[i] = x[i] + dt * v[i]

	a = acc(x) #call the acceleration code again
	
	for i in range(n):
		v[i] = v[i] + 0.5 * dt * a[i] #another loop through velocity half-stepping

	return x, v

accel = lambda x: [-i for i in x]
inv_linPen = lambda x: [i for i in x]
nonlin_pen = lambda x: [-np.sin(i) for i in x]

def printstate(x, v, n, tnow):
	#point_history.append(x[0])
	print('Time: ' + str(tnow))

	for i in range(n):
		print(str(i) + ':   x=' + str(x[i]) + '  v=' + str(v[i]))

	print('-----------------------')


def animate(ph, dt):
	fig = plt.figure()
	ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
	#camera = Camera(fig)
	for i in range(len(ph)):
		ax.clear()
		ax.set_xlim(-2,2)
		ax.plot([-2, ph[i]], [0, 0], color='gray', linestyle='-.')
		ax.scatter(ph[i], 0)
		plt.pause(0.1)
		plt.savefig('out/movingpoint_' + str(i) + '.png')
		#plt.show()
		#camera.snap()
def prob_1a():
	a, b, c = main(accel)
	print(len(a[0]))
	print(len(b[0]))
	print(len(c))
	plot_prob1_2d(a,b)
	plot_prob1_3d(a,b,c)


def prob_1b():
	a, b, c = main(inv_linPen)
	plot_prob1_2d(a, b)
	plot_prob1_3d(a, b, c)


def prob_1d():
	a, b, c = main(nonlin_pen)
	plot_prob1_2d(a, b)
	plot_prob1_3d(a, b, c)

def plot_prob1_2d(x_history, v_history):
	for i in range(len(x_history)):
		plt.plot(x_history[i], v_history[i])
		plt.plot(x_history[i][-1], v_history[i][-1], 'or')


	plt.title('Position and Velocity History of Points')
	plt.xlabel('X (m)')
	plt.ylabel('V (m/s)')

def plot_prob1_3d(x_history, v_history, t_history):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for i in range((len(x_history))):
		ax.plot(xs=x_history[i], ys=v_history[i], zs=t_history)
		#ax.plot(xs=x_history[i][-1], ys=v_history[i][-1], zs=t_history[-1])

	ax.set_title('Position and Velocity Through Time')
	ax.set_xlabel('Position (m)')
	ax.set_ylabel('Velocity (m/s)')
	ax.set_zlabel('Time (s)')
