# README

## Project Description

This repository contains a computer graphics program that focuses on the reshape and render functions for rendering a 3D object. The program reads geometric data for an object, a set of control points, the type of interpolation algorithm (Catmull-Rom or B-spline), and the time spacing (dt) from an `input_file.txt` file located in the `inputs` folder.

## Input File Format

The `input_file.txt` file should follow a specific format:

1. The first line must contain the value of `dt`, which determines the time spacing for the animation.
2. The second line must specify the algorithm to be used. You can choose between "B-spline (BS)" or "Catmull-Rom (CMS)".
3. Starting from the third line and onwards, the file should contain the geometric data of the object. You do not need to specify whether the coordinates are given with fixed angles or quaternions. The program will automatically identify and process the data based on its length.

## Example Input File

Here's an example of an `input_file.txt`:
```bash
0.1
CMS
1.0 2.0 3.0 30.0 45.0 60.0
2.0 3.0 4.0 45.0 60.0 90.0
3.0 4.0 5.0 60.0 90.0 120.0
```

In this example, `0.1` is the time spacing (`dt`), and "CMS" indicates the use of the Catmull-Rom interpolation algorithm. The following lines represent the geometric data for the object, including position and orientation values.

## Running the Program

To run the program, execute the main Python script. The program will load the input data and render the object according to the specified algorithm and time spacing.

```bash
python main-pygame.py
```

Make sure you have the necessary dependencies installed, including OpenGL and related libraries.


## Note

The program is designed to handle different input data formats and automatically determine whether the coordinates are specified with fixed angles or quaternions. The primary focus is on the reshape and render functions, which are essential for the 3D rendering of the object.

### Link to the demo
https://youtu.be/UegaK6z6IfY