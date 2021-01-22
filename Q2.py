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

def main(print_imgs=False):
	#initial conditions

	#x = np.array([np.zeros(n)]) #set initial position as 0 as default for all points
	#v = np.array([np.zeros(n)]) #set initial velocity as 0 as default for all points
	tnow = 0 #set initial time
	t_history = []
	
	#mercury
	merc_x = np.array([float(2.604201011310763E-01), float(1.864324373512932E-01), float(-9.647552137649361E-03)])
	merc_v = np.array([float(2.127308739205635E-02), float(2.452906275972208E-02), float(3.955906804908533E-03)])

	#venus
	ven_x = np.array([float(-6.609662875246326E-02), float(-7.183627436475873E-01), float(-6.406605566889365E-03)])
	ven_v = np.array([float(2.001649583272528E-02), float(-1.734661816835225E-03), float(-1.178965793918118E-03)])

	#earth
	earth_x = np.array([float(-5.267351086537421E-01), float(8.414619510425699E-01), float(7.409243276119383E-05)])
	earth_v = np.array([float(-1.489005801989798E-02), float(-9.164587690644333E-03), float(1.804115761210164E-07)])
	
	#mars
	mars_x = np.array([float(3.865504084247152E-01), float(1.487195367528798E+00), float(2.150295512204376E-02)])
	mars_v = np.array([float(-1.300215712213690E-02), float(4.773764380908049E-03), float(4.191683415519417E-04)])

	#jupiter
	jup_x = np.array([float(3.158527936260250E+00), float(-3.978110649853764E+00), float(-5.416164966468561E-02)])
	jup_v = np.array([float(5.816292235994370E-03), float(5.049901398046003E-03), float(-1.510665064156852E-04)])

	#saturn
	sat_x = np.array([float(5.574688546121132E+00), float(-8.271472920873290E+00), float(-7.811944780886933E-02)])
	sat_v = np.array([float(4.314319954459810E-03), float(3.104343959012436E-03), float(-2.257570879956657E-04)])

	#uranus
	ura_x = np.array([float(1.529056050687172E+01), float(1.252775181486506E+01), float(-1.515629637047193E-01)])
	ura_v = np.array([float(-2.521700431316857E-03), float(2.859155757368757E-03), float(4.332161177379602E-05)])

	#neptune
	nep_x = np.array([float(2.946488189941961E+01), float(-5.160508095498839E+00), float(-5.727774903045594E-01)])
	nep_v = np.array([float(5.209656741392452E-04), float(3.110459149340707E-03), float(-7.647033897027830E-05)])

	#pluto
	plut_x = np.array([float(1.411559127960592E+01), float(-3.113930516565182E+01), float(-7.509785697469543E-01)])
	plut_v = np.array([float(2.930852460405504E-03), float(6.135845991607150E-04), float(-9.256971366693098E-04)])

	x = np.vstack((ven_x, earth_x, mars_x, jup_x, sat_x, ura_x, nep_x, plut_x))
	v = np.vstack((ven_v, earth_v, mars_v, jup_v, sat_v, ura_v, nep_v, plut_v))
	n = len(x)
	
	x_history = [[i] for i in x]
	v_history = [[i] for i in v]
	t_history.append(tnow)
	#integration perameters
	max_step = 360 * 156
	nout = 4
	dt = 1

	#looping to perform integration
	for i in range(max_step):
		if (i % nout == 0): #if enough steps have passed, print the state
			if(print_imgs):
				printstate(x, x_history, n, tnow)
			x_history = np.append([[i] for i in x], x_history, axis=1)
			v_history = np.append([[i] for i in v], v_history, axis=1)
			t_history.append(tnow)


		x, v = leapstep(x, v, n, dt) #take an integration step
		
		tnow += dt

	if (max_step % nout == 0): #if the last step would have printed
		if(print_imgs):
			printstate(x, x_history, n, tnow) #then print
		x_history = np.append([[i] for i in x], x_history, axis=1)
		v_history = np.append([[i] for i in v], v_history, axis=1)
		t_history.append(tnow)


	return x_history, v_history, t_history

def leapstep(x, v, n, dt):
	a = acc(x, n) #call the acceleration code

	for i in range(n):
		v[i] = v[i] + 0.5 * dt * a[i] #loop over all points and increase the velocities by a half setp

	for i in range(n): #loop again an increase the positions by a full step
		x[i] = x[i] + dt * v[i]

	a = acc(x, n) #call the acceleration code again
	
	for i in range(n):
		v[i] = v[i] + 0.5 * dt * a[i] #another loop through velocity half-stepping

	return x, v

def acc(x, n):
	GM =  0.0002959 #G * M in AU^3 / day^2
	a = []
	for p in range(n):
		pos = x[p]
		rinv = (sum(pos ** 2)) ** (-0.5)
		k = GM * rinv * rinv * rinv #GM / r^3
		a.append(-k * pos)

	return a




nonlin_pen = lambda x: [-np.sin(i) for i in x]

def printstate(x, x_h, n, tnow):
	#point_history.append(x[0])
	fig = plt.figure(figsize=(8, 5))
	ax = fig.add_subplot(111, projection='3d')
	ax.set_title ("Earth's Orbit around the Sun")
	plt.figtext(.5,.9,'Time = ' + str(tnow) + ' (days)', fontsize=12, ha='center')
	ax.plot([0],[0],[0], 'oy')
	for i in range(n):
		xs = [j[0] for j in x_h[i]]
		ys = [j[1] for j in x_h[i]]
		zs = [j[2] for j in x_h[i]]
		ax.plot(xs=xs, ys=ys, zs=zs, color = 'blue')
		ax.plot([x[i][0]], [x[i][1]], [x[i][2]], 'ob')

	plt.savefig('animate/orbit_' + str(tnow) + '.png')

		

def plot_2d(x_history):
	fig = plt.figure()
	plt.plot(0,0, 'oy')

	for planet in x_history:
		xs = [i[0] for i in planet]
		ys = [i[1] for i in planet]
		plt.plot(xs, ys)

	plt.title('Orbits of the Planets Around the Sun')

def plot_3d(x_history, v_history, t_history):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot([0],[0],[0], 'oy')
	for planet in x_history:
		xs = [i[0] for i in planet]
		ys = [i[1] for i in planet]
		zs = [i[2] for i in planet]
		
		ax.plot(xs=xs, ys=ys, zs=zs)
		#ax.plot(xs=x_history[i][-1], ys=v_history[i][-1], zs=t_history[-1])

	ax.set_title('Orbits of the Planets around the Sun (Origin)')
