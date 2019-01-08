import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelmin
import src

def is_there_a_stone_at_this_position(x,y):
    pass

def find_board_points(rgb, plot_stuff=False):
    """
        You have the RGB matrix of the goban as a square matrix but you don't
        know which entries correspon to the points on the board. This code finds
        the board points by plotting average red, green and blue scales and
        calculating the 19 local minima. Why? Because board points are
        intersections of black lines and RGB value of black color is [0,0,0].
    """
    if plot_stuff:
        plt.subplot(221)
        plt.imshow(rgb)
        plt.subplot(222)
        x1_idx = find_custom_local_minima(np.mean(rgb[:,:,0],axis=0), 'r', plot_stuff)
        plt.subplot(223)
        x2_idx = find_custom_local_minima(np.mean(rgb[:,:,1],axis=0), 'g', plot_stuff)
        plt.subplot(224)
        x3_idx = find_custom_local_minima(np.mean(rgb[:,:,2],axis=0), 'b', plot_stuff)
        plt.show()

        plt.subplot(221)
        plt.imshow(rgb)
        plt.subplot(222)
        y1_idx = find_custom_local_minima(np.mean(rgb[:,:,0],axis=1), 'r', plot_stuff)
        plt.subplot(223)
        y2_idx = find_custom_local_minima(np.mean(rgb[:,:,1],axis=1), 'g', plot_stuff)
        plt.subplot(224)
        y3_idx = find_custom_local_minima(np.mean(rgb[:,:,2],axis=1), 'b', plot_stuff)
        plt.show()

    else:
        x1_idx = find_custom_local_minima(np.mean(rgb[:,:,0],axis=0), 'r', plot_stuff)
        x2_idx = find_custom_local_minima(np.mean(rgb[:,:,1],axis=0), 'g', plot_stuff)
        x3_idx = find_custom_local_minima(np.mean(rgb[:,:,2],axis=0), 'b', plot_stuff)

        y1_idx = find_custom_local_minima(np.mean(rgb[:,:,0],axis=1), 'r', plot_stuff)
        y2_idx = find_custom_local_minima(np.mean(rgb[:,:,1],axis=1), 'g', plot_stuff)
        y3_idx = find_custom_local_minima(np.mean(rgb[:,:,2],axis=1), 'b', plot_stuff)

    # Sometimes indices found by red, green and blue scales don't agree
    x_idx = src.make_indices_agree(x1_idx, x2_idx, x3_idx)
    y_idx = src.make_indices_agree(y1_idx, y2_idx, y3_idx)

    return x_idx, y_idx

def rescale_pyhsical_goban_rgb(rgb, \
                            UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
                            BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y):
    # Rescale to n by n matrix
    n = 300

    # find n points on the left and on the right boundaries
    x_left_vals, y_left_vals, rgb, _ = \
            src.return_int_pnts(n, rgb, BL_outer_x, BL_outer_y, UL_outer_x, UL_outer_y)
    x_right_vals, y_right_vals, rgb, _ = \
            src.return_int_pnts(n, rgb, BR_outer_x, BR_outer_y, UR_outer_x, UR_outer_y)

    # Calculate a new RGB matrix only for the board, by removing outside the board
    new_rgb = np.zeros([n,n,3])
    for i in range(n):
        x1, y1 = x_left_vals[i], y_left_vals[i]
        x2, y2 = x_right_vals[i], y_right_vals[i]
        # print((x1,y1), (x2,y2))
        _, _, rgb, v = src.return_int_pnts(n, rgb, x1, y1, x2, y2)
        for j in range(n):
            new_rgb[n-i-1, j, :] = v[j]

    return  new_rgb.astype(np.uint8)

def plot_goban_rgb(rgb, bxy=[], wxy=[]):
    plt.imshow(rgb)
    plt.ylabel('1st index = 1, ..., 19')
    plt.xlabel('2nd index = 1, ..., 19')
    plt.show()

def average_RGB(rgb, xMAX, yMAX, x, y, w):
    # Calculates average RGB around a board point for stone detection
    xL, xR = np.maximum(0, x-w), np.minimum(x+w+1, xMAX-1)
    yL, yR = np.maximum(0, y-w), np.minimum(y+w+1, yMAX-1)
    red_scale = np.mean(np.mean(rgb[yL:yR, xL:xR, 0]))
    green_scale = np.mean(np.mean(rgb[yL:yR, xL:xR, 1]))
    blue_scale = np.mean(np.mean(rgb[yL:yR, xL:xR, 2]))
    return [red_scale, green_scale, blue_scale]

def make_indices_agree(x1, x2, x3):
    # Board points are determined from local extrema of R,G,B values.
    # But sometimes they don't match. In that case, choose the one whose
    #  second difference looks like a constant
    a1 = np.amax(abs(np.diff(np.diff(x1))))
    a2 = np.amax(abs(np.diff(np.diff(x2))))
    a3 = np.amax(abs(np.diff(np.diff(x3))))
    x = 0
    x = x1 if a1 <= a2 and a1 <= a3 else x
    x = x2 if a2 <= a1 and a2 <= a3 else x
    x = x3 if a3 <= a1 and a3 <= a2 else x
    assert x is not 0
    return x

def calibrate(rgb, x_idx, y_idx, bxy=[], wxy=[]):
    """
    Depending on light, laptop angle etc. the board may have different RGB values
    at different times. So how do we distinguis black and white stones?
    RGB of black = [0,0,0]
    RGB of white = [255,255,255]
    We will use red scale to distinguish black stones and blue scale to
    distinguish white stones.
    """
    xMAX, yMAX, _ = rgb.shape
    roll_w = int(np.round(0.01*xMAX))

    # BLACK STONE CALIBRATION

    # Input black stone indices is bxy is empty
    if not bxy:
        msg = 'Enter black stone indices (e.g. 1 14 and 0 for end): '
        while True:
            input_text = input(msg)
            if input_text == '0':
                break
            else:
                j,i = list(map(int, input_text.split()))
                bxy.append((i,j))
                RGB = src.average_RGB(rgb, xMAX, yMAX, x_idx[i-1], y_idx[j-1], roll_w)
                print('RGB = ', RGB)

    # Find maximum red scale of black stones
    RMAX = 0
    for j,i in bxy:
        RGB = src.average_RGB(rgb, xMAX, yMAX, x_idx[i-1], y_idx[j-1], roll_w)
        RMAX = np.maximum(RMAX, RGB[0])

    # Find the min red scale of the rest to distinguish
    RMIN_rest = 255
    for i,x in enumerate(x_idx, start=1):
        for j,y in enumerate(y_idx, start=1):
            if (j,i) not in bxy:
                RGB = src.average_RGB(rgb, xMAX, yMAX, x, y, roll_w)
                RMIN_rest = np.minimum(RMIN_rest, RGB[0])
    print('\nBlack stones have a maximum red scale =', RMAX)
    print('Rest of the board have a minimum red scale', RMIN_rest)
    print('Black stone red scale threshold will be average of these two.\n')

    # Red scale threshold for black stone detection
    assert RMAX < RMIN_rest
    red_scale_th = 0.5 * RMAX + 0.5 * RMIN_rest

    # WHITE STONE CALIBRATION

    # Input white stone indices is wxy is empty
    if not wxy:
        msg = 'Enter white stone indices (e.g. 1 14 and 0 for end): '
        while True:
            input_text = input(msg)
            if input_text == '0':
                break
            else:
                j,i = list(map(int, input_text.split()))
                wxy.append((i,j))
                RGB = src.average_RGB(rgb, xMAX, yMAX, x_idx[i-1], y_idx[j-1], roll_w)
                print('RGB = ', RGB)

    # Find minimum blue scale of white stones
    BMIN = 255
    for (j,i) in wxy:
        RGB = src.average_RGB(rgb, xMAX, yMAX, x_idx[i-1], y_idx[j-1], roll_w)
        BMIN = np.minimum(BMIN, RGB[2])

    # Find the max blue scale of the rest to distinguis
    BMAX_rest = 0
    for i,x in enumerate(x_idx, start=1):
        for j,y in enumerate(y_idx, start=1):
            if (j,i) not in wxy:
                RGB = src.average_RGB(rgb, xMAX, yMAX, x, y,roll_w)
                BMAX_rest = np.maximum(BMAX_rest, RGB[2])
    print('\nWhite stones have a minimum blue scale >', BMIN)
    print('Rest of the board have a maximum blue scale', BMAX_rest)
    print('White stone blue scale threshold will be average of these two.\n')

    # Blue scale threshold for white stone detection
    assert BMIN > BMAX_rest
    blue_scale_th = 0.5 * BMIN + 0.5 * BMAX_rest

    return red_scale_th, blue_scale_th

def is_this_stone_on_the_board(rgb, x_idx, y_idx, red_scale_th, blue_scale_th, \
                                    color, i, j):
    i,j = j,i # RGB matrix is messed up so this needs to be done
    xMAX, yMAX, _ = rgb.shape
    roll_w = int(np.round(0.01*xMAX))
    x, y = x_idx[i-1], y_idx[j-1]
    xL, xR = np.maximum(0, x-roll_w), np.minimum(x+roll_w+1, xMAX-1)
    yL, yR = np.maximum(0, y-roll_w), np.minimum(y+roll_w+1, yMAX-1)
    red_scale = np.mean(np.mean(rgb[yL:yR, xL:xR, 0]))
    blue_scale = np.mean(np.mean(rgb[yL:yR, xL:xR, 2]))
    if color == 'black' and red_scale < red_scale_th:
        print(f"There is black stone at {src.int_coords_to_str(i,j)} = ({i},{j})")
        return True
    elif color == 'white' and blue_scale > blue_scale_th:
        print(f"There is white stone at {src.int_coords_to_str(i,j)} = ({i},{j})")
        return True
    else:
        return False

def mark_stones(rgb, x_idx, y_idx, red_scale_th, blue_scale_th, plot_stuff=True):
    xMAX, yMAX, _ = rgb.shape
    roll_w = int(np.round(0.01*xMAX))
    new_rgb = np.copy(rgb)
    bxy, wxy = [], [] # black and white stone lists including pairs
    for i, x in enumerate(x_idx, start=1):
        for j, y in enumerate(y_idx, start=1):
            xL, xR = np.maximum(0, x-roll_w), np.minimum(x+roll_w+1, xMAX-1)
            yL, yR = np.maximum(0, y-roll_w), np.minimum(y+roll_w+1, yMAX-1)
            red_scale = np.mean(np.mean(rgb[yL:yR, xL:xR, 0]))
            blue_scale = np.mean(np.mean(rgb[yL:yR, xL:xR, 2]))
            #print((x,y), red_scale, blue_scale)
            if red_scale < red_scale_th or blue_scale > blue_scale_th:
                if blue_scale > blue_scale_th:
                    wxy.append((j,i))
                    new_rgb[yL:yR, xL:xR,:] = 255, 255, 255 # white stone
                elif red_scale < red_scale_th:
                    bxy.append((j,i))
                    new_rgb[yL:yR, xL:xR,:] = 255, 255, 0 # black stone
            else:
                new_rgb[yL:yR, xL:xR,:] = 255, 0, 0 # empty

    if plot_stuff:
        src.plot_goban_rgb(new_rgb)

    return bxy, wxy

def mark_board_points(rgb, x_idx, y_idx, bxy=[], wxy=[]):
    """
    Mark board points with red squares. Use yellow color for black stones and
    white color for white stones that are inputted.
    """
    xMAX, yMAX, _ = rgb.shape
    roll_w = int(np.round(0.01*xMAX))
    new_rgb = np.copy(rgb)
    for i,x in enumerate(x_idx, start=1):
        for j,y in enumerate(y_idx, start=1):
            xL, xR = np.maximum(0, x-roll_w), np.minimum(x+roll_w+1, xMAX-1)
            yL, yR = np.maximum(0, y-roll_w), np.minimum(y+roll_w+1, yMAX-1)
            if (j,i) in bxy: # black stone
                new_rgb[yL:yR, xL:xR,:] = 255, 255, 0 # yellow color
            elif (j,i) in wxy: # white stone
                new_rgb[yL:yR, xL:xR,:] = 255, 255, 255 # white color
            else: # empty board point
                new_rgb[yL:yR, xL:xR,:] = 255, 0, 0 # red color
    src.plot_goban_rgb(new_rgb)

def find_custom_local_minima(ar1, color, plot_stuff):
    roll_w = int(np.round(len(ar1)/100))
    ar2 = subtract_rolling_sum(roll_w, ar1)
    idx = find_local_minima(ar2)
    if plot_stuff:
        plt.plot(ar2, color)
        for i in idx:
            plt.plot(i, ar2[i], 'k*')
    return idx

def find_local_minima(ar):
    # Try to find the optional cut-off that may help determine the 19 points on
    # the go board. Start with an interval [min_val, max_val] and squeeze until
    # it hits exactly 19 points
    # Find indices that correspond to local minima
    x = argrelmin(ar)
    idx_list = x[0]

    target = 19
    min_val, max_val = np.amin(ar), 100.0

    # Assert that above choices are good
    assert sum(ar[i] <= min_val for i in idx_list) < target
    assert sum(ar[i] <= max_val for i in idx_list) > target

    # Find the cut-off below which there are exactly 19 local minima
    while True:
        new_val = 0.5 * min_val + 0.5 * max_val
        if sum(ar[i] <= new_val for i in idx_list) < target:
            min_val = new_val
        elif sum(ar[i] <= new_val for i in idx_list) > target:
            max_val = new_val
        elif sum(ar[i] <= new_val for i in idx_list) == target:
            break

    # Find the indices
    return [i for i in idx_list if ar[i] <= new_val]

def rolling_sum(w, ar):
    new_ar = np.zeros(len(ar))
    for i in range(len(ar)):
        if i >= w and i <= len(ar)-w-1:
            new_ar[i] = np.mean(ar[i-w:i+w+1])
        elif i < w:
            new_ar[i] = np.mean(ar[0:i+1])
        elif i > len(ar)-w-1:
            new_ar[i] = np.mean(ar[i:len(ar)+1])
    assert len(new_ar) == len(ar)
    return new_ar

def subtract_rolling_sum(w, ar):
    return ar - rolling_sum(w,ar)

def return_int_pnts(num, rgb, x1, y1, x2, y2):
    x_vals = np.round(np.linspace(x1, x2, num=num, endpoint=True))
    x_vals = x_vals.astype(int)
    y_vals = np.round(np.linspace(y1, y2, num=num, endpoint=True))
    y_vals = y_vals.astype(int)
    # one of these two must not contain any duplicates
    assert len(x_vals) == len(set(x_vals)) or len(y_vals) == len(set(y_vals))
    # Return RGB values
    return_array = [rgb[y,x,0:3] for x,y in zip(x_vals, y_vals)]
    # make all red
    # for x,y in zip(x_vals, y_vals):
    #    rgb[y,x,0:3] = 255, 0, 0
    return x_vals, y_vals, rgb, return_array
