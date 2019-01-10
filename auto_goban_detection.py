import matplotlib.pyplot as plt
import imageio
import numpy as np
import src

IMG_PATH = 'images/empty_pyshical_goban1.png'

board_corners = []
def onclick(event):
    print(event.xdata, event.ydata)
    board_corners.append((event.xdata, event.ydata))

# Get RGB matrix of the picture with goban
rgb = imageio.imread(IMG_PATH)
fig = plt.figure()
plt.imshow(rgb)
plt.title("Please click on UL-UR-BL-BR corners...")
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

UL_outer_x, UL_outer_y = board_corners[0]
UR_outer_x, UR_outer_y = board_corners[1]
BL_outer_x, BL_outer_y = board_corners[2]
BR_outer_x, BR_outer_y = board_corners[3]

# Remove non-goban part from the RGB matrix and make it a square matrix
rgb = src.rescale_pyhsical_goban_rgb(rgb, \
                        UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
                        BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y)

# Find the indices of board points in the new square RGB matrix
x_idx, y_idx = src.find_board_points(rgb, plot_stuff=True)

# Mark board points
src.mark_board_points(rgb, x_idx, y_idx)

#bxy, wxy = [(4,4), (16,4)], [(4,16),(16,16)]

#src.mark_board_points(rgb, x_idx, y_idx, bxy, wxy)

#red_scale_th, blue_scale_th = src.calibrate(rgb, x_idx, y_idx, bxy, wxy)
#bxy_new, wxy_new = src.mark_stones(rgb, x_idx, y_idx, red_scale_th, blue_scale_th)

#src.is_this_stone_on_the_board(rgb, x_idx, y_idx, red_scale_th, blue_scale_th, \
#                                'black', 16,4)
