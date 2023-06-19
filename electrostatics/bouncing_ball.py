
from vpython import *

def bouncing_ball_restitution(g,e,vy):
    # STEP 1: Draw a sphere

    # Define sphere dimensions and initial conditions
    R = 1                    # m
    m = 0.1                  # kg
    r0 = vector(0,7.0,0)  # m    Notice this is a vector, not a number!!!!!
    v0 = vector(0,vy,0)    # m/s

    # Draw the sphere itself, specify attributes, and name it ball

    scene = canvas() 
    s = "Rotate the camera by dragging with the right mouse button,\n"
    s += "To zoom, drag with the left+right mouse buttons or use the mouse pad.\n"
    s += "Touch screen: pinch/extend to zoom, swipe or two-finger rotate."
    scene.caption = s

    ball = sphere (pos = r0, radius = R, color=color.red)  # r0  is already a vector

    # Add an extra attribute to the sphere that we'll use to make it move.
    # We initially set it equal to v0

    ball.velocity  = v0

    # STEP 2: Draw a box in which to put the sphere called "ball"

    # Draw a box
    floor   = box (pos = vector( 0,-8, 0), length =  20, height =  0.5, width = 4, color=color.blue)
    #ceiling = box (pos = vector( 0, 8, 0), length =  20, height =  0.5, width = 4, color=color.blue)
    #left    = box (pos = vector(-10, 0, 0), length = 0.5, height = 16.5, width = 4, color=color.blue)
    #right   = box (pos = vector(10, 0, 0), length = 0.5, height = 16.5, width = 4, color=color.blue)

    # STEP 3: Add and/or calculate physical parameters

    # Gravitational force
    Fg = m*vector(0.0, -g, 0.0)   # N    This is a scalar times a vector, so Fg is a vector

    # Time

    time = 0    # s    Set the initial time to zero
    dt = 0.01   # s    We'll only step forward 10ms each iteration through while loop
    t_f = 10    # s    How long the simulation lasts 

    # STEP 4: Define constants to improve simulation display
    # Slow frame update rate so human eye can track objects

    frequency = 100

    # STEP 5: Execute simulation by repeatedly updating "ball" position

    # Define algorithm to move simulation forward in time by one unit "dt"

    while time < t_f: # Update for a fixed number of time steps

        # Calculate acceleration of "ball" at current position. NOT AN UPDATE!
        ball.accel = Fg / m # This is constant because gravity is constant. Could also use g.

        # Length over which ball and floor overlap - this is one simple way of modeling
        # the bouncing.
        overlap = ball.pos.y - R - floor.pos.y  - floor.height/2

    
        # Update velocity of "ball"
    
        if overlap > 0: #  the ball is not in contact with the floor
             ball.velocity = ball.velocity + ball.accel * dt 
        else:
             ball.velocity = - e*ball.velocity
    
        ball.velocity = ball.velocity + ball.accel * dt 

        # Continue running simulation at human-manageable speed
        rate (frequency) # Simulate slow enough for human eye

        # Update position of "ball"
        ball.pos = ball.pos + ball.velocity * dt 

        # Keep time variable up to date
        time = time + dt # update the time

  
