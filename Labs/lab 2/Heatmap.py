import os
import argparse
import csv
import numpy
import matplotlib
from matplotlib import pyplot, image


def draw_display(dispsize, imagefile=None):

    # construct screen (black background)
    screen = numpy.ones((dispsize[1], dispsize[0], 3), dtype='float32')
    # if an image location has been passed, draw the image
    if imagefile != None:
        # check if the path to the image exists
        if not os.path.isfile(imagefile):
            raise Exception("ERROR in draw_display: imagefile not found at '%s'" % imagefile)
        # load image
        img = image.imread(imagefile)

        # width and height of the image
        w, h = len(img[0]), len(img)
        # x and y position of the image on the display
        x = dispsize[0] / 2 - w / 2
        y = dispsize[1] / 2 - h / 2
        # draw the image on the screen
        screen[y:y + h, x:x + w, :] += img
    # dots per inch
    dpi = 100.0
    # determine the figure size in inches
    figsize = (dispsize[0] / dpi, dispsize[1] / dpi)
    # create a figure
    fig = pyplot.figure(figsize=figsize, dpi=dpi, frameon=False)
    ax = pyplot.Axes(fig, [0, 0, 1, 1])
    ax.set_axis_off()
    fig.add_axes(ax)
    # plot display
    ax.axis([0, dispsize[0], 0, dispsize[1]])
    ax.imshow(screen)  # , origin='upper')

    return fig, ax

def gaussian(x, sx, y=None, sy=None):

    # square Gaussian if only x values are passed
    if y == None:
        y = x
    if sy == None:
        sy = sx
    # centers
    xo = x / 2
    yo = y / 2
    # matrix of zeros
    M = numpy.zeros([y, x], dtype=float)
    # gaussian matrix
    for i in range(x):
        for j in range(y):
            M[j, i] = numpy.exp(
                -1.0 * (((float(i) - xo) ** 2 / (2 * sx * sx)) + ((float(j) - yo) ** 2 / (2 * sy * sy))))

    return M

def draw_heatmap(gazepoints, dispsize, imagefile=None, alpha=0.5, savefilename=None, gaussianwh=200, gaussiansd=None):
    # IMAGE
    dispsize_1 = int(dispsize[1])
    dispsize_0 = int(dispsize[0])
    dispsize =  (dispsize_1, dispsize_0)

    fig, ax = draw_display(dispsize, imagefile=imagefile)

    # HEATMAP
    # Gaussian
    gwh = int(gaussianwh)
    gsdwh = gwh / 6 if (gaussiansd is None) else gaussiansd
    gaus = gaussian(gwh, gsdwh)
    # matrix of zeroes
    strt = int(gwh / 2)
    heatmapsize = (int(dispsize[1] + 2 * strt), int(dispsize[0] + 2 * strt))
    heatmap = numpy.zeros(heatmapsize, dtype=float)
    # create heatmap
    for i in range(0, len(gazepoints)):
        # get x and y coordinates
        x = int(strt + gazepoints[i][0] - int(gwh / 2))
        y = int(strt + gazepoints[i][1] - int(gwh / 2))
        # correct Gaussian size if either coordinate falls outside of
        # display boundaries
        if (not 0 < x < dispsize[0]) or (not 0 < y < dispsize[1]):
            hadj = [0, gwh];
            vadj = [0, gwh]
            if 0 > x:
                hadj[0] = abs(x)
                x = 0
            elif dispsize[0] < x:
                hadj[1] = gwh - int(x - dispsize[0])
            if 0 > y:
                vadj[0] = abs(y)
                y = 0
            elif dispsize[1] < y:
                vadj[1] = gwh - int(y - dispsize[1])
            # add adjusted Gaussian to the current heatmap
            try:
                heatmap[y:y + vadj[1], x:x + hadj[1]] += gaus[vadj[0]:vadj[1], hadj[0]:hadj[1]] * gazepoints[i][2]
            except:
                # fixation was probably outside of display
                pass
        else:
            # add Gaussian to the current heatmap
            heatmap[y:y + gwh, x:x + gwh] += gaus * gazepoints[i][2]
    # resize heatmap
    heatmap = heatmap[strt:dispsize[1] + strt, strt:dispsize[0] + strt]
    # remove zeros
    lowbound = numpy.mean(heatmap[heatmap > 0])
    heatmap[heatmap < lowbound] = numpy.NaN
    # draw heatmap on top of image
    ax.imshow(heatmap, cmap='jet', alpha=alpha)

    # FINISH PLOT
    # invert the y axis, as (0,0) is top left on a display
    
    # save the figure if a file name was provided
    if savefilename != None:
        fig.savefig(savefilename)

    return fig

##################
#     Parsing    #
##################

# Define the default values
DEFAULT_DISPLAY_WIDTH = 1000
DEFAULT_DISPLAY_HEIGHT = 1500
DEFAULT_ALPHA = 0.8
DEFAULT_OUTPUT_NAME = 'HEATMAP_50'
DEFAULT_BACKGROUND_IMAGE = None
DEFAULT_N_GAUSSIAN_MATRIX = 50
DEFAULT_STANDARD_DEVIATION = None
DEFAULT_INPUT_PATH = 'Advanced_Visual_Data_Analysis/EyeTrack.csv'

with open(DEFAULT_INPUT_PATH, newline='') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    
    raw = list(reader)
    
    gaze_data = []
    for row in raw:
        if len(row) == 2:
            gaze_data.append((int(row[0]), int(row[1]), 1))
        else:
            gaze_data.append((int(row[0]), int(row[1]), int(row[2])))
    
    res = draw_heatmap(gaze_data, (DEFAULT_DISPLAY_WIDTH, DEFAULT_DISPLAY_HEIGHT), 
                 alpha=DEFAULT_ALPHA, savefilename=DEFAULT_OUTPUT_NAME, 
                 imagefile=DEFAULT_BACKGROUND_IMAGE, gaussianwh=DEFAULT_N_GAUSSIAN_MATRIX, 
                 gaussiansd=DEFAULT_STANDARD_DEVIATION)

""" # Specify the path to the TSV file
# tsv_path = 'Advanced_Visual_Data_Analysis/Data/EyeTrack-raw.tsv'

# # Read the TSV file into a DataFrame
# data = pd.read_csv(tsv_path, sep='\t')

# # Extract the desired columns
# extracted_data = data[['GazePointX(px)', 'GazePointY(px)', 'GazeEventDuration(mS)']]

# # Save the extracted data to a CSV file
# extracted_data.to_csv('EyeTrack.csv', index=False)

# # Optionally, print the extracted data (this will show the first few rows in the console)
# print(extracted_data.head()) """
