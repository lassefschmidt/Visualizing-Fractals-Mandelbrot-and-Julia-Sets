# Visualizing Fractals -- ReadMe Guide

This file will explain to users how to run our "Visualizing Fractals" code to generate and customize a Mandelbrot Set in pygame.

This guide includes information on:

- Features of the code
- How to run the code and navigate the program
- How to choose "good" settings for the Mandelbrot Set

## Features

Our "Visualizing Fractals" code allows the user to:

- Genreate a Mandelbrot Set in pygame
- Zoom in and out, and navigate around the pygame window with his/her mouse
- Customize the pygame window from a series of settings in tkinter GUI

Tkinter GUI settings include:

- Resolution: Size of the users pygame window
- Color Scheme: Color map for the Mandelbrot visualization
- Color Interpolation: Method by which the function travels through the selected color gradient
- Color Selection based on: Method by which colors are selected based on iteration count
- Julia Set: Julia Set inclusion in the pygame window
- Iterations: Number of times the equation runs
- Number of Colors: Number of colors included from the color map

## Running the Code & Navigating the Program

1) Download and open all associated files / folders including the main, pygameGUI, fractals, and other associated init, pydoc, and pycache files
2) Run the program from the main.py file
3) In the tkinter window that opens, choose any settings and then click the "Update Fractal" button. (It is recommended to begin with default settings and then customize them later.)
4) Once the pygame window is generated, navigate around the window by:
    a) Left-clicking to zoom-in (or clicking regularly on a Mac)
    b) Right-clicking to zoom-out (or clicking with two fingers on a Mac)
    c) Clicking in locations where you would like to zoom-in and zoom-out of (i.e. the zoom will be directed to / from where the cursor is at the time of the mouse click)
5) Click the "Open Settings" button in the top left of the screen to return to the tkinter window and update your settings
6) Exit the pygame window by clicking the "Exit Game" button, closing the window, or terminating the program
    
### Additional Note
- When the Julia Set is selected, move your mouse anywhere on the Mandelbort side of the screen to see how the Julia Set changes

## Choosing "Good" Settings

While the user is free to choose any settings he/she pleases, certain setting combinations will yield particularly fascinating results while others will cause difficulties with the program. 

The below list includes a few tips for the user to navigate the fractals but is by no means comprehensive of the various combinations of settings that can / should be chosen:

- Depending on the size of the user's computer screen, the resolution settings should be adjusted so no portion of the pygame window is displayed off the screen
- Except in instances of deep zoom and high iteration count, the user should set the Color Selection based on smoothed iteration count; however, at deep zoom, the simple iteration count will yield hyper fragmented and interesting images
- The Julia Sets are best explored from a less-deep zoom as it will be more dynamic the faster along the coordinate plane that the mouse is moving
- Depending on the computing power of the user's machine, he/she should be wary of going above an iteration count of 1000 as above that the program can run much slower as the user zooms