# README

## Project Description: Behavioral Motion Control System
Implement a behavioral system like [Reynolds] flocking system. You can start
with a set of simple behaviors that are mediated by simple weighted average then make
extensions with more complex behaviors and better mediation schemes. The boids can live in 2-
D space (e.g., earth-bound beings) or 3-D space.

## Overview

This project implements a behavioral boid simulation using OpenGL, where a leader boid (cube) is followed by a group of follower boids (spheres). The simulation leverages behavioral rules, such as following a leader, responding to nearby collisions, and normalizing velocity and position based on neighboring boids.

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Input File Format](#input-file-format)
- [Simulation Details](#simulation-details)
- [Controls](#controls)
- [Dependencies](#dependencies)

## Project Structure

- `boid_simulation.py`: Main Python script containing the boid simulation logic.
- `inputs/input_file.txt`: Example input file with simulation parameters.
- `outputs/`: Placeholder for any generated output files.
- `README.md`: Project documentation.

## Getting Started

To run the simulation, follow these steps:

1. Ensure you have Python installed on your machine.
2. Install the necessary dependencies using:

    ```bash
    pip install numpy PyOpenGL
    ```

3. Run the simulation:

    ```bash
    python boid_simulation.py
    ```

## Usage

The simulation starts with a leader boid and a group of follower boids. The leader reads parameters from the `input_file.txt` file, and the simulation unfolds based on behavioral rules.

## Input File Format

The `input_file.txt` file specifies simulation parameters and geometric data for the leader boid. The format is as follows:

1. The first line contains the spacing parameter (`dt`).
2. The second line contains the algorithm to be used (`BS` for B-spline or `CMS` for Catmull-Rom).
3. Starting from the third line, geometric data for the leader boid is specified. Comments (lines starting with `#`) are ignored.

Example:

```plaintext
1
CMS
1 1 -15 1 0 0 0
4 4 -20 0.707 0 0.707 0
-5 0 -15 0.707 0.707 0 0
-5 5 -15 0.5 0.5 -0.5 -0.5
-1 1 -15 0.707 0 0.707 0
1 5 -35 0.5 -0.5 0.5 -0.5
0 0 -5 0.707 0 0.707 0
1 1 -15 1 0 0 0
```
or

```plaintext
0.5
BS
1 3 -15 0 0 0
2 3 -15 0 0 0
3 3 -15 0 0 0
3 2 -15 45 0 0
3 1 -15 45 0 0
3 0 -15 45 0 0
3 -1 -15 45 0 0
3 -2 -15 45 0 0
3 -3 -15 45 0 0
2 -3 -16 45 0 0
1 -3 -17 45 0 0
0 -3 -18 45 0 0
-1 -3 -19 45 0 0
-2 -3 -20 45 0 0
-3 -3 -20 45 0 0
-3 -2 -20 0 90 0
-3 -1 -20 0 90 0
-3 0 -20 0 90 0
-3 1 -20 0 90 0
-3 2 -20 0 90 0
-3 3 -19 0 90 0
-2 3 -18 0 90 0
-1 3 -17 0 90 0
0 3 -16 0 90 0
1 3 -15 0 0 0
```
## Simulation Details

- **Boid Class (`Boid`):**
  - Represents an individual boid with position, velocity, and behavioral attributes.

- **Boids Class (`Boids`):**
  - Manages a collection of boids, including the leader and followers.

- **Rendering:**
  - The simulation renders the leader as a cube and followers as spheres.

- **Interpolation:**
  - Catmull-Rom spline and B-spline interpolation are used for leader position and orientation.

- **Behavioral Rules:**
  - Boids follow a leader, respond to nearby collisions, and normalize velocity and position based on neighboring boids.

## Controls

- Press `Esc` or `q` to exit the simulation.

## Dependencies

- Python 3.x
- NumPy
- PyOpenGL

Install dependencies using:

```bash
pip install numpy PyOpenGL
```

### Link to the demo
https://youtu.be/y204I-Bq_5o