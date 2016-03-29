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

# Apply a gaussian blur to the image
def ScaleImage(img, targetWidth, targetHeight):
    in_width = len(img)
    in_height = len(img[0])
    out = []
    for x in range(targetWidth):
        pixels = []
        for y in range(targetHeight):
            # Grab the X pixel
            in_approx_xpx = float(in_width - 1) / float(targetWidth) * float(x)
            in_approx_ypx = float(in_height - 1) / float(targetHeight) * float(y)
            in_minxpx = int(max(math.floor(in_approx_xpx), 0))
            in_maxxpx = int(max(math.ceil(in_approx_xpx), 0))
            in_minypx = int(max(math.floor(in_approx_ypx), 0))
            in_maxypx = int(max(math.ceil(in_approx_ypx), 0))
            percentX = in_approx_xpx - float(in_minxpx)
            percentY = in_approx_ypx - float(in_minypx)

            p0 = float(img[in_minxpx, in_minypx]) * (1.0 - percentX) + float(img[in_maxxpx, in_minypx]) * (percentX)
            p1 = float(img[in_minxpx, in_maxypx]) * (1.0 - percentX) + float(img[in_maxxpx, in_maxypx]) * (percentX)
            pixel = p0*(1.0-percentY) + p1*percentY
            pixels.append(pixel)

        pixels = numpy.asarray(pixels)
        out.append(pixels)
    out = numpy.asarray(out)
    return out

# Main
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print >>sys.stderr, "Usage: %s %d %d <input image> <TargetWidth> <TargetHeight>"
        sys.exit(0)

    # Filenames
    print("Reading Input")
    input_filename = sys.argv[1]
    oname = input_filename.rsplit('.',1)[0]
    output_filename = oname + '_scaled.png'

    # Read input and generate matrix
    image_intensities = read_image_greyscale(input_filename)
    # Apply the matrix blur
    print("Applying Scaling")
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    scaled = ScaleImage(image_intensities, width, height)

    # Save output
    print("Saving Image")
    write_png_grayscale(output_filename, scaled)
