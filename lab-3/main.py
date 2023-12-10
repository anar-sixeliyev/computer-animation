## Program will take inputs in the below format:
## Ball([0.0, 40.0, 0.0], 5.0, [1.0, 0.0, 0.0], [1.0, 2.0, 3.0], 5),
## The inputs order:  position, radius, color, velocity, mass

# Importing necessary libraries
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Constants for animation
num_frames = 100
current_frame = 0

# Class definition for a Ball object
class Ball:
    def __init__(self, position, radius, color, velocity, mass):
        # Initialize ball properties
        self.position = position
        self.radius = radius
        self.color = color
        self.velocity = velocity
        self.mass = mass

    def draw(self):
        # Draw the ball using OpenGL commands
        glColor3f(*self.color)
        glPushMatrix()
        glTranslatef(*self.position)
        glutSolidSphere(self.radius, 20, 20)
        glPopMatrix()

    def update(self, delta_time):
        # Update ball properties based on physics and collisions
        # Update velocity based on gravity
        self.velocity[1] += -9.8 * delta_time  # Gravity coefficient
        # Update position based on velocity
        for i in range(3):
            self.position[i] += self.velocity[i] * delta_time

        # Check for collision with the ground
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.velocity[1] = abs(self.velocity[1])  # Reflect velocity

        # Check for collision with walls (assuming balls are not too close to walls)
        for i in range(3):
            if abs(self.position[i]) + self.radius > 30:
                self.position[i] = math.copysign(30 - self.radius, self.position[i])
                self.velocity[i] = -self.velocity[i]  # Reflect velocity

        # Check for collision with other balls
        for other_ball in balls:
            # Skip if it is the same
            if other_ball != self:
                distance = math.sqrt(sum((self.position[i] - other_ball.position[i]) ** 2 for i in range(3)))
                if distance < self.radius + other_ball.radius:
                    # Collision detected, reflect velocities
                    self.reflect_velocities(other_ball)

    def reflect_velocities(self, other_ball):
        # Reflect velocities using elastic collision equations
        # v1f=( (m1−m2)*v1+2*m2*v2 ) / (m1 + m2)
        for i in range(3):
            v1_final = ((self.mass - other_ball.mass) * self.velocity[i] + 2 * other_ball.mass *
                        other_ball.velocity[i]) / (self.mass + other_ball.mass)
            v2_final = ((other_ball.mass - self.mass) * other_ball.velocity[i] + 2 * self.mass *
                        self.velocity[i]) / (self.mass + other_ball.mass)

            self.velocity[i] = v1_final
            other_ball.velocity[i] = v2_final

# List of Ball objects
# follow this order when entering new balls: position, radius, color, velocity, mass
balls = [
    Ball([0.0, 40.0, 0.0], 5.0, [1.0, 0.0, 0.0], [1.0, 2.0, 3.0], 5),
    Ball([5.0, 35.0, 0.0], 3.0, [0.0, 1.0, 0.0], [1.0, 2.0, 3.0], 3),
    Ball([-5.0, 38.0, 5.0], 1.0, [0.0, 0.0, 1.0], [1.0, 2.0, 3.0], 1),
    Ball([8.0, 30.0, -5.0], 4.0, [1.0, 1.0, 0.0], [-2.0, 1.0, -3.0], 4),
    Ball([-10.0, 25.0, 2.0], 2.0, [0.5, 0.5, 0.5], [3.0, -1.0, 2.0], 2),
]

# Function to render the scene
def render_scene():
    # Set the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(90.0, 90.0, 90.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)

    # Render the ground, walls, and roof
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)  # Red color for ground
    # Rendering the ground grid
    for x in range(-30, 31, 5):
        glVertex3f(x, 0, -30)
        glVertex3f(x, 0, 30)
    for z in range(-30, 31, 5):
        glVertex3f(-30, 0, z)
        glVertex3f(30, 0, z)

    # Rendering the back wall
    glColor3f(0.0, 1.0, 0.0)  # Green color for back wall
    for y in range(0, 30):
        glVertex3f(-30, y, -30)
        glVertex3f(30, y, -30)
    for x in range(-30, 31, 5):
        glVertex3f(x, 0, -30)
        glVertex3f(x, 30, -30)

    # Rendering the front wall
    glColor3f(1.0, 1.0, 1.0)  # White color for front wall
    for y in range(0, 30):
        glVertex3f(-30, y, 30)
        glVertex3f(30, y, 30)
    for x in range(-30, 31, 5):
        glVertex3f(x, 0, 30)
        glVertex3f(x, 30, 30)

    # Rendering the left wall
    glColor3f(0.0, 0.0, 1.0)  # Blue color for left wall
    for y in range(0, 30):
        glVertex3f(-30, y, -30)
        glVertex3f(-30, y, 30)
    for z in range(-30, 31, 5):
        glVertex3f(-30, 0, z)
        glVertex3f(-30, 30, z)

    # Rendering the right wall
    for y in range(0, 30):
        glVertex3f(30, y, -30)
        glVertex3f(30, y, 30)
    for z in range(-30, 31, 5):
        glVertex3f(30, 0, z)
        glVertex3f(30, 30, z)

    # Rendering the roof
    glColor3f(0.5, 0.5, 0.5)  # Gray color for roof
    for x in range(-30, 31, 5):
        glVertex3f(x, 30, -30)
        glVertex3f(x, 30, 30)

    for z in range(-30, 31, 5):
        glVertex3f(-30, 30, z)
        glVertex3f(30, 30, z)
    glEnd()

    # Render balls in the scene
    for ball in balls:
        ball.draw()

# Function to update ball positions
def update_balls(delta_time):
    for ball in balls:
        ball.update(delta_time)

# Function to render the scene and update animations
def render():
    global current_frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    render_scene()

    # Update animation frame and ball positions
    current_frame += 0.1
    if current_frame >= num_frames:
        current_frame = 0
    update_balls(0.1)

    glutSwapBuffers()

# Function to handle window resizing
def reshape(w, h):
    # Update viewport and projection matrix on window reshape
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w) / float(h), 0.01, 5000.0)

# Function to handle timer for continuous rendering
def timer(value):
    glutPostRedisplay()
    glutTimerFunc(60, timer, 0)  # 16 ms per frame (about 60 frames per second)

# Main function
def main():
    # Initialize GLUT
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow(b"OpenGL Ground and Walls")
    glutInitWindowSize(800, 600)
    glutDisplayFunc(render)
    glutReshapeFunc(reshape)

    # Enable depth testing for 3D rendering
    glEnable(GL_DEPTH_TEST)

    # Set initial camera position
    glTranslatef(0, 0, -15)

    # Set up timer for continuous rendering
    glutTimerFunc(60, timer, 0)

    # Enter GLUT main loop
    glutMainLoop()

# Entry point for the script
if __name__ == "__main__":
    main()
