
import numpy as np
from scipy.optimize import fsolve
from math import sin, cos, atan2, sqrt, pi

members = [
    {'length': 0.8,
    'angle': -pi/4
    },
    {'length': 0.1,
    'angle':  0
    },
    {'length': 0.5,
    'angle': pi / 6},
    {'length': 0.5,
    'angle': 3*pi/8}
]
K = 800  # (N / m) from http://web.mit.edu/sp255/www/reference_vault/acct_rope_behavior.pdf
FL = 1000  # (N)


def member_elongation(x, y):
    # change in length of members
    def elongation(member):
        return sqrt( (member['length'] * sin(member['angle']) + x)**2 + (member['length'] * cos(member['angle']) + y)**2  ) - member['length']

    return [elongation(member) for member in members]

def member_forces(deltas):
    # force proportional to displacement
    def force(delta, member):
        return K * delta / member['length']
    
    return [force(delta, member) for delta, member in zip(deltas, members)]

def angles_after_elongation(x, y):
    # New anlge of members after elongation
    def get_angles(member):
        return atan2(member['length'] * sin(member['angle']) + x, member['length'] * cos(member['angle']) + y)
    return [get_angles(member) for member in members]

def y_equilibrium(forces, angles):
    def y_component(force, angle):
        return force * cos(angle)
    
    forces = [y_component(force, angle) for force, angle in zip(forces, angles)]
    return sum(forces) - FL

def x_equilibrium(forces, angles):
    def x_component(force, angle):
        return force * sin(angle)
    
    forces = [x_component(force, angle) for force, angle in zip(forces, angles)]
    return sum(forces)

def anchor_equilibrium(z):
    x = z[0]
    y = z[1]

    deltas = member_elongation(x, y)
    forces = member_forces(deltas)
    angles2 = angles_after_elongation(x, y)
    
    # equilibrium equations
    y_eq = y_equilibrium(forces, angles2)
    x_eq = x_equilibrium(forces, angles2)
    return [x_eq, y_eq]

# Use solver to determine displacement
guess = np.array([0, 0.01])
x,y = fsolve(anchor_equilibrium, guess)
print(f"Master point displacement when loaded: x: {x}, y {y}")

# With the elongation, calculate the forces
deltas = member_elongation(x, y)
forces = member_forces(deltas)
angles2 = angles_after_elongation(x, y)
print(f"Change in length of members: {deltas}")
print(f"Anlges after displacement {angles2}")
print(f"Resultant forces {forces}")