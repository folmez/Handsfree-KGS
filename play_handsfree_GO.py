from pynput.mouse import Button, Controller
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
    print(f"\nPlease put a {color} stone at {src.convert_physical_board_ij_to_str(i,j)}...")

    # Assert the stone with desired color is on the goban at the exact spot
    while True:
        time.sleep(5)
        frame_num = frames.get()
        img_name = f"images/game_log/opencv_frame_{frame_num}.png"
        rgb = imageio.imread(img_name)
        plt.imshow(rgb)
        plt.title(f"This board should have a {color} stone at {src.convert_physical_board_ij_to_str(i,j)}.")
        plt.show()
        ans = input(f"Did you put a {color} stone at {src.convert_physical_board_ij_to_str(i,j)}? [y/n]: ")
        if ans is 'y':
            rgb = src.rescale_pyhsical_goban_rgb(rgb, ob)
            assert src.is_this_stone_on_the_board(rgb, x_idx, y_idx, \
                    red_scale_th, blue_scale_th, color, i, j, plot_stuff=True)
            remove_this_frame(img_name)
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
            remove_this_frame(img_name)
            frames.task_done()
    print('Unused frames removed...')

board_corners = []
def onclick(event):
    print(event.xdata, event.ydata)
    board_corners.append(event.xdata)
    board_corners.append(event.ydata)

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
            # Skip if nothing is clicked
            remove_this_frame(img_name)
            frames.task_done()
        else:
            # Read goban corners
            ob = board_corners
            assert ob[2] > ob[0] and ob[6] > ob[4] and \
                    ob[7] > ob[4] and ob[5] > ob[1]
            # Remove this filename as it served its purpose and break out of loop
            remove_this_frame(img_name)
            frames.task_done()
            break

    # Remove all unused frames at the end
    remove_unused_frames()

    # Remove non-goban part from the RGB matrix and make it a square matrix
    rgb = src.rescale_pyhsical_goban_rgb(rgb, ob)

    # Find the indices of board points in the new square RGB matrix
    x_idx, y_idx = src.find_board_points(rgb, plot_stuff=False)

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
            rgb = src.rescale_pyhsical_goban_rgb(rgb, ob)
            # Calibrate
            red_scale_th1, blue_scale_th1 = src.calibrate(rgb, x_idx, y_idx, bxy, wxy)
            # Refind stones using the above thresholds
            bxy_new, wxy_new = src.mark_stones(rgb, x_idx, y_idx, \
                            red_scale_th1, blue_scale_th1, plot_stuff=False)
            remove_this_frame(img_name)
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
            rgb = src.rescale_pyhsical_goban_rgb(rgb, ob)
            # Calibrate
            red_scale_th2, blue_scale_th2 = src.calibrate(rgb, x_idx, y_idx, bxy, wxy)
            # Refind stones using the above thresholds
            bxy_new, wxy_new = src.mark_stones(rgb, x_idx, y_idx, \
                            red_scale_th2, blue_scale_th2, plot_stuff=False)
            remove_this_frame(img_name)
            frames.task_done()
            remove_unused_frames()
            break
        else:
            remove_this_frame(img_name)
            frames.task_done()

    red_scale_th = 0.5 * (red_scale_th1 + red_scale_th2)
    blue_scale_th = 0.5 * (blue_scale_th1 + blue_scale_th2)

    # VERIFY CALIBRATION OF PHYSICAL BOARD
    print(' [PLEASE KEEP IN MIND THAT YOUR LOWER-LEFT CORNER IS (1,1)]')
    verify_calibration(x_idx, y_idx, red_scale_th, blue_scale_th, 'black', 3, 4)
    verify_calibration(x_idx, y_idx, red_scale_th, blue_scale_th, 'white', 1, 1)
    verify_calibration(x_idx, y_idx, red_scale_th, blue_scale_th, 'black', 10, 10)
    verify_calibration(x_idx, y_idx, red_scale_th, blue_scale_th, 'white', 19, 19)
    print("CALIBRATION IS VERIFIED\n" + 50*"-")

    # DIGITAL BOARD DETECTION

    # Ask the user to open a KGS board
    print('\n   OPEN A KGS BOARD/GAME NOW')
    input('ENTER when the digital board is open: ')

    # Get the user to click on come corners to get to know the digital board
    UL_x, UL_y, goban_step = src.get_goban_corners()

    # Test by moving to the star points on the board
    for str in ['D16', 'K16', 'Q16', 'D10', 'K10', 'Q10', 'D4', 'K4', 'Q4']:
        i, j = src.str_to_integer_coordinates(str)
        x, y = src.int_coords_to_screen_coordinates(UL_x, UL_y, i, j, goban_step)
        src.make_the_move(mouse, x, y, no_click=True)

    # START REPLAYING PYHSICAL BOARD MOVES ON THE DIGITAL BOARD
    # Plan - 1) check frames continously until a move is made by you
    #        2) check digital board until a move is made by your opponent


    # First, remove all unused frames
    remove_unused_frames()

    # Scan the frames for moves every five seconds
    mouse = Controller() # obtain mouse controller
    bxy, wxy = [], []   # empty board in the beginning
    while True:
        time.sleep(5)
        frame_num = frames.get()
        img_name = f"images/game_log/opencv_frame_{frame_num}.png"
        color, i, j = src.scan_next_move(img_name, ob, x_idx, y_idx, \
                                        red_scale_th, blue_scale_th, bxy, wxy)
        if color is not None:
            # Play the move and update the stone lists
            bxy, wxy = src.play_next_move_on_digital_board(mouse, color, \
                                        i, j, bxy, wxy, UL_x, UL_y, goban_step)
            # Start checking the digital board for new moves
        else:
            # Remove this frame and start waiting for the next frame
            remove_this_frame(img_name)
            frames.task_done()


    # Wait for the threads to finish...
    my_frame_grabber.join()

    print('Main Terminating...')
