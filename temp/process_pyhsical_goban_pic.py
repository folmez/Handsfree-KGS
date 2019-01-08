import matplotlib.pyplot as plt
import imageio
import numpy as np
import src

IMG_PATH = 'images/pyshical_goban_pic1.png'
#IMG_PATH = 'images/pyshical_goban_pic2.png'
#IMG_PATH = 'images/pyshical_goban_pic3.png'
UL_outer_x, UL_outer_y = 315, 24
UR_outer_x, UR_outer_y = 999, 40
BL_outer_x, BL_outer_y = 3, 585
BR_outer_x, BR_outer_y = 1273, 621
#IMG_PATH = 'images/pyshical_goban_pic4.png'
#UL_outer_x, UL_outer_y = 321, 235
#UR_outer_x, UR_outer_y = 793, 244
#BL_outer_x, BL_outer_y = 92, 603
#BR_outer_x, BR_outer_y = 933, 608

# Get RGB matrix of the picture with goban
rgb = imageio.imread(IMG_PATH)
plt.imshow(rgb)
plt.show()

# Remove non-goban part from the RGB matrix and make it a square matrix
rgb = src.rescale_pyhsical_goban_rgb(rgb, \
                        UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
                        BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y)

# Find the indices of board points in the new square RGB matrix
x_idx, y_idx = src.find_board_points(rgb, plot_stuff=True)

bxy, wxy = [(4,4), (16,4)], [(4,16),(16,16)]

src.mark_board_points(rgb, x_idx, y_idx, bxy, wxy)

red_scale_th, blue_scale_th = src.calibrate(rgb, x_idx, y_idx, bxy, wxy)

bxy_new, wxy_new = src.mark_stones(rgb, x_idx, y_idx, red_scale_th, blue_scale_th)

src.is_this_stone_on_the_board(rgb, x_idx, y_idx, red_scale_th, blue_scale_th, \
                                'black', 16,4)
