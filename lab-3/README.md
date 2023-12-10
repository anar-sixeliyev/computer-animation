# README

## Project Description: Physics-Based Motion Control System
Implement a system to generate the motions of rigid bodies using physical
principles. Include the effect of gravity and collision between objects. You may make some
simple approximations for rotational dynamics. For collisions, reflect the velocity. Collision
detection becomes easy if you consider a bounding sphere of the objects in the scene.

## Overview
This Python script demonstrates a simple physics simulation using OpenGL to render a 3D scene with bouncing balls. The simulation includes gravitational effects, collisions with the ground, walls, and other balls, and elastic collisions between balls.
## Dependencies

The script relies on the following Python libraries:

* math: Provides mathematical functions.
* OpenGL.GL: OpenGL bindings for rendering graphics.
* OpenGL.GLU: OpenGL Utility Library for higher-level functionality.
* OpenGL.GLUT: OpenGL Utility Toolkit for handling windows and user input.

Make sure to install these dependencies before running the script.

## Example Input 
 Program will take inputs in the below format:
* Ball([0.0, 40.0, 0.0], 5.0, [1.0, 0.0, 0.0], [1.0, 2.0, 3.0], 5), 

The inputs order:  position, radius, color, velocity, mass


### Link to the demo
https://youtu.be/hq-7O5v4VeQ