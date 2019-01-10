import cv2
import imageio
import matplotlib.pyplot as plt
import threading
import time
import queue
import os
import numpy as np
import src

frames = queue.Queue(maxsize=10)

class frameGrabber(threading.Thread):
    def __init__(self):
        # Constructor
        threading.Thread.__init__(self)

    def run(self):
        cam = cv2.VideoCapture(0)
        img_counter = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                break
            img_name = f"images/game_log/opencv_frame_{img_counter}.png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            frames.put(img_counter)
            img_counter += 1
            time.sleep(30)
        cam.release()

def verify_calibration(x_idx, y_idx, red_scale_th, blue_scale_th, color, i, j):
    # Display a message to the user to put a stone
    print(f"\nPlease put a {color} stone at ({i},{j})...")

    # Assert the stone with desired color is on the goban at the exact spot
    while True:
        time.sleep(5)
        frame_num = frames.get()
        img_name = f"images/game_log/opencv_frame_{frame_num}.png"
        rgb = imageio.imread(img_name)
        plt.imshow(rgb)
        plt.title(f"This board should have a {color} stone at ({i},{j}).")
        plt.show()
        ans = input(f"Did you put a {color} stone at ({i},{j})? [y/n]: ")
        if ans is 'y':
            assert src.is_this_stone_on_the_board(rgb, x_idx, y_idx, \
                                    red_scale_th, blue_scale_th, color, i, j)
            frames.task_done()
            remove_unused_frames()
            break
        else:
            remove_this_frame(img_name)
            frames.task_done()

def remove_this_frame(img_name):
    os.remove(img_name)
    print('Frame', img_name, 'removed.')

def remove_unused_frames():
    print('Removing unused frames...')
    while True:
        time.sleep(1)
        try:
            frame_num = frames.get(False)
        except queue.Empty:
            # Handle empty queue here
            break
        else:
            # Handle task here and call q.task_done()
            frame_num = frames.get()
            img_name = f"images/game_log/opencv_frame_{frame_num}.png"
            os.remove(img_name)
            print('Frame', img_name, 'removed.')
            frames.task_done()
    print('Unused frames removed...')

board_corners = []
def onclick(event):
    print(event.xdata, event.ydata)
    board_corners.append((event.xdata, event.ydata))

if __name__ == '__main__':

    # Initiate the frame grabber thread for goban pictures
    my_frame_grabber = frameGrabber()

    # Start running the threads!
    my_frame_grabber.start()
    print('Frame grabbing has started...')

    # MANUAL BOARD EDGE DETECTION FOR THE PYHSICAL BOARD
    # Show a plot frames and ask user to input boundaries
    while True:
        time.sleep(5)
        frame_num = frames.get()
        img_name = f"images/game_log/opencv_frame_{frame_num}.png"
        rgb = imageio.imread(img_name)
        fig = plt.figure()
        plt.imshow(rgb)
        plt.title("Please click on UL-UR-BL-BR corners or close plot...")
        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()
        if not board_corners:
            # Skip this file is nothing is clicked
            os.remove(img_name)
            print('Frame', img_name, 'removed.')
            frames.task_done()
        else:
            # Read goban corners
            UL_outer_x, UL_outer_y = board_corners[0]
            UR_outer_x, UR_outer_y = board_corners[1]
            BL_outer_x, BL_outer_y = board_corners[2]
            BR_outer_x, BR_outer_y = board_corners[3]
            assert UR_outer_x > UL_outer_x and BR_outer_x > BL_outer_x and \
                    BR_outer_y > UR_outer_y and BL_outer_y > UL_outer_y
            # Remove non-goban part from the RGB matrix and make it a square matrix
            rgb = src.rescale_pyhsical_goban_rgb(rgb, \
                            UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
                            BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y)
            # Find the indices of board points in the new square RGB matrix
            x_idx, y_idx = src.find_board_points(rgb, plot_stuff=False)
            # Remove this filename as it served its purpose
            remove_this_frame(img_name)
            frames.task_done()
            # Remove all unused frames
            remove_unused_frames()
            break

    # CALIBRATION OF PYHSICAL BOARD
    # Ask the user to put black and white stones on the board
    print('\nPlease put black stones on corners and a white stone at center')
    bxy, wxy = [(1,1), (19,19), (1,19), (19,1)], [(10,10)]
    while True:
        time.sleep(5)
        frame_num = frames.get()
        img_name = f"images/game_log/opencv_frame_{frame_num}.png"
        rgb = imageio.imread(img_name)
        plt.imshow(rgb)
        plt.title('Did you put black on corners and white at center?')
        plt.show()
        ans = input('Did you put black stones on corners and a white stone at center? [y/n]: ')
        if ans is 'y':
            # Remove non-goban part from the RGB matrix and make it a square matrix
            rgb = src.rescale_pyhsical_goban_rgb(rgb, \
                            UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
                            BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y)
            # Calibrate
            red_scale_th1, blue_scale_th1 = src.calibrate(rgb, x_idx, y_idx, bxy, wxy)
            # Refind stones using the above thresholds
            bxy_new, wxy_new = src.mark_stones(rgb, x_idx, y_idx, \
                            red_scale_th1, blue_scale_th1, plot_stuff=False)
            frames.task_done()
            remove_unused_frames()
            break
        else:
            remove_this_frame(img_name)
            frames.task_done()

    print('\nPlease put white stones on corners and a black stone at center')
    wxy, bxy = [(1,1), (19,19), (1,19), (19,1)], [(10,10)]
    while True:
        time.sleep(5)
        frame_num = frames.get()
        img_name = f"images/game_log/opencv_frame_{frame_num}.png"
        rgb = imageio.imread(img_name)
        plt.imshow(rgb)
        plt.title('Did you put white on corners and black at center?')
        plt.show()
        ans = input('Did you put white stones on corners and a black stone at center? [y/n]: ')
        if ans is 'y':
            # Remove non-goban part from the RGB matrix and make it a square matrix
            rgb = src.rescale_pyhsical_goban_rgb(rgb, \
                            UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
                            BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y)
            # Calibrate
            red_scale_th2, blue_scale_th2 = src.calibrate(rgb, x_idx, y_idx, bxy, wxy)
            # Refind stones using the above thresholds
            bxy_new, wxy_new = src.mark_stones(rgb, x_idx, y_idx, \
                            red_scale_th2, blue_scale_th2, plot_stuff=False)
            frames.task_done()
            remove_unused_frames()
            break
        else:
            remove_this_frame(img_name)
            frames.task_done()

    red_scale_th = 0.5 * (red_scale_th1 + red_scale_th2)
    blue_scale_th = 0.5 * (blue_scale_th1 + blue_scale_th2)

    # VERIFY CALIBRATION OF PHYSICAL BOARD
    verify_calibration(x_idx, y_idx, red_scale_th, blue_scale_th, 'white', 1, 1)
    verify_calibration(x_idx, y_idx, red_scale_th, blue_scale_th, 'black', 10, 10)
    verify_calibration(x_idx, y_idx, red_scale_th, blue_scale_th, 'white', 19, 19)

    # DIGITAL BOARD DETECTION

    # START REPLAYING PYHSICAL BOARD MOVES ON THE DIGITAL BOARD

    # Wait for the threads to finish...
    my_frame_grabber.join()

    print('Main Terminating...')
