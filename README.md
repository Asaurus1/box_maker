box_maker
=========

Box-Maker is a small Python project to create acryllic box toolpaths for NUsolar and to experiment with packing algorithms. 
It generates point lists according to the dimensions specified in the commandline arguments, and generates an svg polygon
using the svgwrite library. Currently positioning of the box elements on the drawing is static. In the future I hope to develop
a simplified packing algorithm which will allow the user to specify the dimensions of her cutting material and have the software
generate an optimally packed configuration that leaves the most usable material.
