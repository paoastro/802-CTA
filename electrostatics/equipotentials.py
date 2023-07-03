from matplotlib import pyplot
import numpy

import electrostatics
from electrostatics import PointCharge, ElectricField, Potential, GaussianCircle,LineCharge
from electrostatics import finalize_plot

def calculate_E(q,r_S,r_P): 
    e0 = 8.854187817e-12  
    k = 1.0 / (4 * pi * e0)
    rSP = sqrt(((r_P[0]-r_S[0])**2) + ((r_P[1]-r_S[1])**2) + ((r_P[2]-r_S[2])**2))
    E_x = k*q *( (r_P[0]-r_S[0]) / rSP**3) 
    E_y = k*q *( (r_P[1]-r_S[1]) / rSP**3) 
    E_z = k*q *( (r_P[2]-r_S[2]) / rSP**3)      
    return([E_x,E_y,E_z])

def draw_E_and_V(charges,locations,background=False,circlesize=True,lines=True):

    XMIN, XMAX = -40, 40
    YMIN, YMAX = -40, 40
    ZOOM = 5
    XOFFSET = 0

    electrostatics.init(XMIN, XMAX, YMIN, YMAX, ZOOM, XOFFSET)

    # Set up the charges, electric field, and potential
    charges = [PointCharge(charges[i]*1e9,locations[i][:2]) for i in range(len(charges))]


    field = ElectricField(charges)
    potential = Potential(charges)

    # Set up the Gaussian surface
    fieldlines = []

    for charge in charges:
        g = GaussianCircle(charge.x, 0.1)

    # Create the field lines

        for x in g.fluxpoints(field, 12):
            fieldlines.append(field.line(x))
    fieldlines.append(field.line([10, 0]))

    # Create the vector grid
    x, y = numpy.meshgrid(numpy.linspace(XMIN/ZOOM+XOFFSET, XMAX/ZOOM+XOFFSET, 41),
                          numpy.linspace(YMIN/ZOOM, YMAX/ZOOM, 31))
    u, v = numpy.zeros_like(x), numpy.zeros_like(y)
    n, m = x.shape
    for i in range(n):
        for j in range(m):
            if any(numpy.isclose(electrostatics.norm(charge.x-[x[i, j], y[i, j]]),
                                 0) for charge in charges):
                u[i, j] = v[i, j] = None
            else:
                mag = field.magnitude([x[i, j], y[i, j]])**(1/5)
                a = field.angle([x[i, j], y[i, j]])
                u[i, j], v[i, j] = mag*numpy.cos(a), mag*numpy.sin(a)

    ## Plotting ##

    # Electric field lines and potential contours
    fig = pyplot.figure(figsize=(20,9))

    pyplot.subplot(1, 2, 1)

    #fig = pyplot.figure(figsize=(8, 6))
    potential.plot()
    potential.plot_color()
    if background:
        field.plot()

    if lines:
        for fieldline in fieldlines:
            fieldline.plot()
    for charge in charges:
        charge.plot(circlesize)
    finalize_plot()
    #fig.savefig('dipole-field-lines.pdf', transparent=True)

    # Field vectors
    pyplot.subplot(1, 2, 2)

    #fig = pyplot.figure(figsize=(8,6))
    cmap = pyplot.cm.get_cmap('hsv')
    pyplot.quiver(x, y, u, v, pivot='mid', cmap=cmap, scale=35)
    for charge in charges:
        charge.plot()
    finalize_plot()
    #fig.savefig('dipole-field-vectors.pdf', transparent=True)

    pyplot.show()
