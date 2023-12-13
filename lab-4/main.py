## This lab is built on top of the first lab(Lab-1). It implements a behavioral system. First we have a leader boid(cube)
## which will read the inputs ( Geometric data for an object, Set of control points, the type (Catmull-Rom or B), and the spacing (dt))
## from the input_file.txt file under the inputs folder. File has to be in the below format:
## First line must contain the value of the dt
## Second line must contain the value of the Algorithm to be used - B-spline(BS) or Catmull-Rom(CMS)
## Starting from the third line and forward will contain the geometric data of the object.
## No need to spesify if the coordinates given with  Fixed Angles or Quaternions, code can identify it(by checking length) and process it by itself.
## Then we have other boids(sphere) which follow the leader with different mediation schemes

import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Global variables
g_screenWidth = 0
g_screenHeight = 0
g_frameIndex = 0
g_angle = 0
current_frame = 0
num_frames = 100

followers_location = [
    [0, 0, -15],
    [0, 1, -10],
    [0, 2, -15],
    [1, 2, -10],
    [2, 2, -15],
    [2, 1, -10],
    [2, 0, -15],
    [1, 0, -10],
]
num_boids = len(followers_location)

position_followers = []


class Boid:
    # individual boid in a simulation.
    def __init__(self, position, velocity):
        # Constructor to initialize a Boid with a given position and velocity.
        self.position = position  # Current position of the boid.
        self.velocity = velocity  # Current velocity of the boid.
        self.Matrix = np.eye(4)  # Transformation matrix for OpenGL rendering.
        self.Matrix[:3, 3] = position  # Set the translation part of the matrix to the initial position.
        self.followLeader = np.zeros(3)  # Vector representing the boid's tendency to follow a leader.
        self.boid_collide = np.zeros(3)  # Vector representing the boid's response to nearby boid collisions.
        self.normalize_velocity = np.zeros(3)  # Vector for normalizing the boid's velocity.
        self.normalize_position = np.zeros(3)  # Vector for normalizing the boid's position.

    def set_velocity(self, velocity):
        # Method to set the boid's velocity.
        self.velocity = velocity

    def set_position(self, position):
        # Method to set the boid's position and update the transformation matrix.
        self.position = position
        self.Matrix[:3, 3] = position

    def distance(self, other):
        # Method to calculate the Euclidean distance between this boid and another boid.
        return np.linalg.norm(self.position - other.position)

    def to_matrix(self):
        # Method to get the transformation matrix of the boid.
        return self.Matrix

    def to_one_d_matrix(self):
        # Method to flatten the transformation matrix into a one-dimensional array.
        return self.Matrix.flatten()


class Boids:
    # This class represents a collection of boids in a simulation.
    def __init__(self, number):
        # Constructor to initialize Boids with a given number of boids.
        self.number = number  # Number of boids in the simulation.
        # Create a list of boids with initial positions and zero velocities.
        self.boids = [Boid(position=np.array(followers_location[i]), velocity=np.zeros(3)) for i in range(number)]
        self.leader_boid = [0, 0, 0]  # Default position and velocity for the leader.

    def followLeader(self, index):
        # Method to update a boid's tendency to follow a leader.
        current = self.boids[index]
        current.followLeader = (self.leader_boid - current.position) / 100

    def boid_collide(self, index):
        # Method to update a boid's response to nearby boid collisions.
        current = self.boids[index]
        count = 0
        for i, next_boid in enumerate(self.boids):
            if i != index and current.distance(next_boid) < 4:
                count += 1
                current.boid_collide += -current.distance(next_boid) / 150
        current.boid_collide /= count

    def normalize_velocity(self, index):
        # Method to normalize a boid's velocity based on the velocities of other boids.
        current = self.boids[index]
        total_velocity = np.zeros(3)
        for i, boid in enumerate(self.boids):
            total_velocity += boid.velocity

        average_velocity = (total_velocity - current.velocity) / (self.number - 1)

        current.normalize_velocity = (average_velocity - current.velocity) / 1000

    def normalize_position(self, index):
        # Method to normalize a boid's position based on the positions of other boids.
        current = self.boids[index]
        total_position = np.zeros(3)
        for i, boid in enumerate(self.boids):
            total_position += boid.position

        center_position = (total_position - current.position) / (self.number - 1)

        current.normalize_position = (center_position - current.position) / 250

    def boid_animator(self, index):
        # Method to update a boid's position and velocity based on various behaviors.
        current = self.boids[index]
        self.followLeader(index)
        self.boid_collide(index)
        self.normalize_velocity(index)
        self.normalize_position(index)
        # Calculate the new velocity and position based on the various behaviors.
        new_velocity = current.velocity + current.followLeader + current.boid_collide + current.normalize_velocity + current.normalize_position
        new_position = current.position + new_velocity * dt  # dt
        # if index == 1:
        #     print('===>index', index, ' current.velocity', current.velocity, ' : followLeader ', current.followLeader,
        #           ' boid_collide ', current.boid_collide, ' normalize_velocity ', current.normalize_velocity,
        #           ' normalize_position ', current.normalize_position)

        # Update the boid's velocity and position.
        current.set_velocity(new_velocity)
        current.set_position(new_position)

# Create an instance of the Boids class with a specified number of boids.
boids = Boids(num_boids)

# Initialize function
def init():
    pass

# Render function
def render():
    global g_angle
    global current_frame

    # Clear the OpenGL buffer
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Configure rendering settings
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    # Enable lighting and set light source attributes
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Light source attributes
    LightAmbient = [0.4, 0.4, 0.4, 1.0]
    LightDiffuse = [0.3, 0.3, 0.3, 1.0]
    LightSpecular = [0.4, 0.4, 0.4, 1.0]
    LightPosition = [5.0, 5.0, 5.0, 1.0]

    # Configure OpenGL light source
    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmbient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDiffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, LightSpecular)
    glLightfv(GL_LIGHT0, GL_POSITION, LightPosition)

    # Surface material attributes
    material_Ka = [0.11, 0.06, 0.11, 1.0]
    material_Kd = [0.43, 0.47, 0.54, 1.0]
    material_Ks = [0.33, 0.33, 0.52, 1.0]
    material_Ke = [0.1, 0.0, 0.1, 1.0]
    material_Se = 10

    # Set material properties
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_Ka)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_Kd)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_Ks)
    glMaterialfv(GL_FRONT, GL_EMISSION, material_Ke)
    glMaterialf(GL_FRONT, GL_SHININESS, material_Se)

    # =================================================
    t = current_frame / (num_frames - 1)

    # Interpolate position and orientation based on 'algo' variable
    if algo == "CMS\n":
        position, orientation = interpolate_catmull_rom(t)
    elif algo == 'BS\n':
        position, orientation = interpolate_B_spline(t)
    else:
        print("Invalid algo format in the input file:", algo)
        sys.exit()

    # Render the teapot at the interpolated position and orientation
    render_leader(position, orientation)
    boids.leader_boid = position
    for i in range(num_boids):
        boids.boid_animator(i)
        render_single_boid(boids.boids[i].position)
    # Increment current frame
    current_frame += dt
    if current_frame >= num_frames:
        current_frame = 0

    # =================================================

    # Disable lighting
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)

    # Swap back and front buffers
    glutSwapBuffers()


# Render the teapot at a given position and orientation
def render_leader(position, orientation):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    if len(control_points[0]) == 6:  # Eular angles
        glRotatef(orientation[0], 1, 0, 0)
        glRotatef(orientation[1], 0, 1, 0)
        glRotatef(orientation[2], 0, 0, 1)
    elif len(control_points[0]) == 7:  # Quaternions
        rotation_matrix = quaternion_to_matrix(orientation)
        glMultMatrixf(rotation_matrix)

    # glutWireTeapot(1)
    glutSolidCube(1)

    glPopMatrix()


def render_single_boid(position):
    #Rendering a single boid element as a solid sphere figure
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glutSolidSphere(0.2, 20, 20)
    glPopMatrix()


# Convert quaternion to rotation matrix
def quaternion_to_matrix(quaternion):
    w, x, y, z = quaternion
    return [
        [1 - 2 * y * y - 2 * z * z, 2 * x * y - 2 * z * w, 2 * x * z + 2 * y * w, 0],
        [2 * x * y + 2 * z * w, 1 - 2 * x * x - 2 * z * z, 2 * y * z - 2 * x * w, 0],
        [2 * x * z - 2 * y * w, 2 * y * z + 2 * x * w, 1 - 2 * x * x - 2 * y * y, 0],
        [0, 0, 0, 1]
    ]


# Catmull-Rom spline interpolation
def interpolate_catmull_rom(t):
    # Interpolate position and orientation based on control points
    n = len(control_points)
    i = int(t * (n - 1))
    t = t * (n - 1) - i

    p0 = np.array(control_points[(i - 1) % n][:3])
    p1 = np.array(control_points[i][:3])
    p2 = np.array(control_points[(i + 1) % n][:3])
    p3 = np.array(control_points[(i + 2) % n][:3])

    position = catmull_rom(t, p0, p1, p2, p3)

    o0 = np.array(control_points[(i - 1) % n][3:])
    o1 = np.array(control_points[i][3:])
    o2 = np.array(control_points[(i + 1) % n][3:])
    o3 = np.array(control_points[(i + 2) % n][3:])

    orientation = catmull_rom(t, o0, o1, o2, o3)

    return position, orientation


# Calculate Catmull-Rom interpolation
def catmull_rom(t, p0, p1, p2, p3):
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2 + (
            -p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)


# B-spline interpolation
def interpolate_B_spline(t):
    # Interpolate position and orientation based on control points
    n = len(control_points)
    i = int(t * (n - 1))
    t = t * (n - 1) - i

    p0 = np.array(control_points[(i - 1) % n][:3])
    p1 = np.array(control_points[i][:3])
    p2 = np.array(control_points[(i + 1) % n][:3])
    p3 = np.array(control_points[(i + 2) % n][:3])

    position = b_spline(t, p0, p1, p2, p3)

    o0 = np.array(control_points[(i - 1) % n][3:])
    o1 = np.array(control_points[i][3:])
    o2 = np.array(control_points[(i + 1) % n][3:])
    o3 = np.array(control_points[(i + 2) % n][3:])

    orientation = b_spline(t, o0, o1, o2, o3)

    return position, orientation


# Calculate B-spline interpolation
def b_spline(t, p0, p1, p2, p3):
    # The B-spline matrix
    matrix = np.array([
        [-1.0 / 6, 3.0 / 6, -3.0 / 6, 1.0 / 6],
        [3.0 / 6, -6.0 / 6, 3.0 / 6, 0.0],
        [-3.0 / 6, 0.0, 3.0 / 6, 0.0],
        [1.0 / 6, 4.0 / 6, 1.0 / 6, 0.0]
    ])

    t_vector = np.array([t ** 3, t ** 2, t, 1])
    control_points_matrix = np.array([p0, p1, p2, p3])

    result = np.dot(t_vector, np.dot(matrix, control_points_matrix))

    return result


# Keyboard input function
def keyboard(key, x, y):
    if key == b'\x1b' or key == b'q':
        sys.exit()


# Reshape function
def reshape(w, h):
    global g_screenWidth, g_screenHeight
    g_screenWidth = w
    g_screenHeight = h

    # Viewport
    glViewport(0, 0, w, h)

    # Projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w) / float(h), 0.01, 5000.0)


# Timer function
def timer(value):
    glutPostRedisplay()
    glutTimerFunc(60, timer, 0)  # 16 ms per frame (about 60 frames per second)


# Load data from an input file
def load_data_from_file(file_path):
    global control_points, dt, algo

    with open(file_path, 'r') as file:
        lines = file.readlines()

    dt = float(lines[0])
    algo = lines[1]
    control_points = []
    for i in range(2, len(lines)):
        data = lines[i].split()
        if lines[i].startswith("#"):
            continue  # Skip comments

        if len(data) == 6:
            x, y, z, rx, ry, rz = map(float, data)
            control_points.append((x, y, z, rx, ry, rz))
        elif len(data) == 7:
            x, y, z, rx, ry, rz, rw = map(float, data)
            control_points.append((x, y, z, rx, ry, rz, rw))
        else:
            print("Invalid data format in the input file.")
            sys.exit()

    if len(control_points) < 4:
        print("You need at least 4 control points for interpolation.")
        sys.exit()


# Main function
def main():
    global g_screenWidth, g_screenHeight

    # Load data from an input file
    load_data_from_file('inputs/input_file')

    # Create an OpenGL window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(sys.argv[0])

    # Initialize
    init()

    # Set callback functions
    glutDisplayFunc(render)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(60, timer, 0)

    # Main loop
    glutMainLoop()


if __name__ == "__main__":
    main()
