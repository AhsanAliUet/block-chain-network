import numpy as np

def degree2rad(angle_in_degree):
    return angle_in_degree * (np.pi/180)

def pol2cart(rho, phi):

    x = rho * np.cos(degree2rad(phi))
    y = rho * np.sin(degree2rad(phi))
    return(x, y)

interval_angle = 360/16
total_angle    = 360
initial_angle  = 0

rho = 36
phi = 0
while (total_angle >= 0):
    x, y = pol2cart(rho, phi)
    print(f"x = {x}")
    print(f"y = {y}")
    print("\n==============\n")
    phi = phi - interval_angle
    total_angle = total_angle - interval_angle
