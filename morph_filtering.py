# morph_filtering.py
# CSC 205 - Spring 2016
#
# Brett Binnersley
# V00776751
# Csc205, assignment #5

import copy
import math
import sys
import png
import itertools
import numpy

def write_png_grayscale(output_filename, pixels):
	with open(output_filename, 'wb') as f:
		w = png.Writer(pixels.shape[1], pixels.shape[0], greyscale=True)
		w.write(f, pixels)

def read_image_greyscale(filename):
	r = png.Reader(filename)
	image_data = r.asDirect()
	width,height = image_data[0], image_data[1]
	image_raw = numpy.vstack(itertools.imap(numpy.uint8, image_data[2]))
	if image_data[3]['greyscale']:
		image_bw = image_raw
	else:
		image_pixels = image_raw.reshape((height, width, 3))
		image_bw = numpy.array( image_pixels.mean(axis=2), dtype=numpy.uint8)
	return image_bw

# Simple Guassian blur matrix
def GenHMatrix():
    matrix = []
    row = numpy.asarray([0, 0, 1, 0, 0])
    matrix.append(row)

    row = numpy.asarray([0, 1, 1, 1, 0])
    matrix.append(row)

    row = numpy.asarray([1, 1, 1, 1, 1])
    matrix.append(row)

    row = numpy.asarray([0, 1, 1, 1, 0])
    matrix.append(row)

    row = numpy.asarray([0, 0, 1, 0, 0])
    matrix.append(row)

    matrix = numpy.asarray(matrix)
    return matrix

# Apply a gaussian blur to the image
def ApplyDilate(img, gmatrix):
    width = len(img)
    height = len(img[0])
    widthr = range(width)
    heightr = range(height)
    out = copy.deepcopy(img)
    for x in enumerate widthr:
        for y in enumerate heightr:
            color = 255  # White
            for mx in enumerate([-2,-1,0,1,2]):
                for my in enumerate([-2,-1,0,1,2]):
                    if gmatrix[mx + 2][my + 2] == 1:  # Only take the values that are 1 in the matrix
                        # Smearing
                        ix = min(max(x + mx, 0), width - 1)
                        iy = min(max(y + my, 0), height -1)
                        if img[ix][iy] < 128:
                            color = 0  # Black
                            break
            out[x][y] = color
    return out

def ApplyErosion(img, gmatrix):
    width = len(img)
    height = len(img[0])
    widthr = range(width)
    heightr = range(height)
    out = copy.deepcopy(img)
    for x in enumerate widthr:
        for y in enumerate heightr:
            color = 0  # Black
            for mx in enumerate([-2,-1,0,1,2]):
                for my in enumerate([-2,-1,0,1,2]):
                    if gmatrix[mx + 2][my + 2] == 1:  # Only take the values that are 1 in the matrix
                        # Smearing
                        ix = min(max(x + mx, 0), width - 1)
                        iy = min(max(y + my, 0), height -1)
                        if img[ix][iy] >= 128:
                            color = 255  # White
                            break
            out[x][y] = color
    return out

# Main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s <input image> <weight>"
        sys.exit(0)

    # Filenames
    input_filename = sys.argv[1]
    oname = input_filename.rsplit('.',1)[0]
    output_filename = oname + '_filter.png'

    # Read input and generate matrix
    image_intensities = read_image_greyscale(input_filename)
    matrix = GenHMatrix()

    # Apply the matrix blur
    dilated = ApplyDilate(image_intensities, matrix)

    # Apply the Erosion
    eroded = ApplyErosion(image_intensities, matrix)

    # Save output
    write_png_grayscale(output_filename, eroded)
