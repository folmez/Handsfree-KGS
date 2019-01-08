import pyscreeze
import numpy as np
import matplotlib.pyplot as plt
import src

def get_digital_goban_state(rgb_pix, plot_stuff=False):
    # RGB of Black = [  0,   0,   0]
    # RGB of White = [255, 255, 255]
    # RGB of Orange = [255, 160, 16]
    # Use red scale to find out black stones, blue scale to find out white stones
    # (1, 1, 1)  - Black A1 (upper corner)
    # (2, 19, 19) - White T10 (lower corner)
    idx = np.arange(19)+1

    m, n, z = rgb_pix.shape
    assert m == n

    # Approximate diameter of a stone in terms of pixels
    stone_diam = n/19

    # Calculate pixels where stone centers will be positioned
    stone_centers = np.round(stone_diam*idx) - 0.5 * np.round(stone_diam) - 1
    stone_centers = stone_centers.astype(int)

    # For every stone center, we will check a square matrix centered around
    # the stone center and find the average color. If it is black, then the
    # stone is black, if it is white, then the stone is white, otherwise no stone
    square_length_in_a_stone = int(np.round((n/19) / np.sqrt(2)))
    if square_length_in_a_stone % 2 == 0:
        d = square_length_in_a_stone / 2
    else:
        d = (square_length_in_a_stone-1) / 2
    d = int(d-1) # just in case, make square smaller and integer

    # Calculate the mean of a small matrix around every board point to find out
    # if there is a black stone or white stone or nothing
    stones = set()
    for posi, i in enumerate(stone_centers, start=1):
        for posj, j in enumerate(stone_centers, start=1):
            # Find black stones
            mat = rgb_pix[:,:,0]
            color = np.mean(np.mean(mat[i:i+d+1, j:j+d+1]))
            if color < 125:
                stones.add((1, posj, posi)) # black stone
                rgb_pix[i-d+1:i+d, j-d+1:j+d, :] = 0

            # Find white stones
            mat = rgb_pix[:,:,2]
            color = np.mean(np.mean(mat[i:i+d+1, j:j+d+1]))
            if color > 125:
                stones.add((2, posj, posi)) # white stone
                rgb_pix[i-d+1:i+d, j-d+1:j+d] = 255

    # Plot for debugging
    if plot_stuff:
        plt.imshow(rgb_pix)
        plt.show()

    return stones

def KGS_goban_rgb_screenshot(UL_x, UL_y, goban_step):
    UL_outer_x = UL_x - 0.5*goban_step
    UL_outer_y = UL_y - 0.5*goban_step
    BR_outer_x = UL_x + 18*goban_step  + 0.5*goban_step
    BR_outer_y = UL_y + 18*goban_step + 0.5*goban_step
    im = pyscreeze.screenshot(region=(UL_outer_x, UL_outer_y, \
                                    BR_outer_x-UL_outer_x, BR_outer_y-UL_outer_y))

    pix = np.array(im)
    rgb_pix = pix[...,:3]

    return rgb_pix
