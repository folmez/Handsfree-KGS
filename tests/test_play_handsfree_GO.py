import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pynput.mouse import Button, Controller
import pytest
import imageio
import src


# Write a test of play_handsfree_GO.py using already existing frames
img_name = []
folder_name = 'images/sample_game_log/ex1/'
# empty board for outer board boundary detection
img_name.append(folder_name + 'opencv_frame_1.png')
UL_outer_x, UL_outer_y = 376.27419354838713, 91.34516129032261
UR_outer_x, UR_outer_y = 962.08064516129020, 101.66774193548395
BL_outer_x, BL_outer_y = 120.79032258064518, 641.0225806451613
BR_outer_x, BR_outer_y = 1265.3064516129032, 652.6354838709677
# black stones on corners and a white stone at center
img_name.append(folder_name + 'opencv_frame_3.png')
# white stones on corners and a black stone at center
img_name.append(folder_name + 'opencv_frame_4.png')
# verifying calibration
img_name.append(folder_name + 'opencv_frame_b_1_1.png') # black at (1,1)
img_name.append(folder_name + 'opencv_frame_b_1_19.png') # black at (1,19)
img_name.append(folder_name + 'opencv_frame_b_19_19.png') # black at (19,19)
img_name.append(folder_name + 'opencv_frame_b_19_1.png') # black at (19,1)
img_name.append(folder_name + 'opencv_frame_b_10_10.png') # black at (10,10)
img_name.append(folder_name + 'opencv_frame_b_4_4.png') # black at (4,4)
img_name.append(folder_name + 'opencv_frame_b_4_10.png') # black at (4,10)
img_name.append(folder_name + 'opencv_frame_b_4_16.png') # black at (4,16)
img_name.append(folder_name + 'opencv_frame_b_16_16.png') # black at (16,16)
img_name.append(folder_name + 'opencv_frame_w_1_1.png') # white at (1,1)
img_name.append(folder_name + 'opencv_frame_w_10_10.png') # white at (10,10)
img_name.append(folder_name + 'opencv_frame_w_16_16.png') # white at (16,16)
img_name.append(folder_name + 'opencv_frame_w_19_19.png') # white at (19,19)
#opencv_frame_b_10_4.png
#opencv_frame_b_10_16.png
#opencv_frame_b_16_4.png
#opencv_frame_b_16_10.png
#opencv_frame_b_19_1.png
#opencv_frame_w_1_19.png
#opencv_frame_w_4_4.png
#opencv_frame_w_4_10.png
#opencv_frame_w_4_16.png
#opencv_frame_w_10_16.png
#opencv_frame_w_16_4.png
#opencv_frame_w_16_10.png
#opencv_frame_w_19_1.png

def test_play_handsfree_GO():
    ps = False
    # STEP 0 - EMPTY GOBAN
    # Get outer boundaries of pyhsical goban -- skipped for speed
    ob = [UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
            BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y]
    # Remove non-goban part from the RGB matrix and make it a square matrix
    # Find the indices of board points in the new square RGB matrix
    #UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
    #    BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y = \
    #    src.get_pyhsical_board_outer_corners(img_name[0])
    rgb = imageio.imread(img_name[0])
    rgb = src.rescale_pyhsical_goban_rgb(rgb, ob)
    x_idx, y_idx = src.find_board_points(rgb, plot_stuff=ps)

    # STEP 1 - GOBAN WITH BLACK STONES ON CORNERS AND A WHITE STONE AT CENTER
    rgb = imageio.imread(img_name[1])
    bxy, wxy = [(1,1), (19,19), (1,19), (19,1)], [(10,10)]
    rgb = src.rescale_pyhsical_goban_rgb(rgb, ob)
    red_scale_th1, blue_scale_th1 = src.calibrate(rgb, x_idx, y_idx, bxy, wxy)
    _, _ = src.mark_stones(rgb, x_idx, y_idx, \
                    red_scale_th1, blue_scale_th1, plot_stuff=ps)

    # STEP 2 - GOBAN WITH WHITE STONES ON CORNERS AND A BLACK STONE AT CENTER
    rgb = imageio.imread(img_name[2])
    wxy, bxy = [(1,1), (19,19), (1,19), (19,1)], [(10,10)]
    rgb = src.rescale_pyhsical_goban_rgb(rgb, ob)
    red_scale_th2, blue_scale_th2 = src.calibrate(rgb, x_idx, y_idx, bxy, wxy)
    _, _ = src.mark_stones(rgb, x_idx, y_idx, \
                    red_scale_th2, blue_scale_th2, plot_stuff=ps)

    red_scale_th = 0.5 * (red_scale_th1 + red_scale_th2)
    blue_scale_th = 0.5 * (blue_scale_th1 + blue_scale_th2)

    # STEP 3 - VERIFY CALIBRATION
    verify_calibration_for_test_purposes(img_name[3], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'black', 1, 1, ps)
    verify_calibration_for_test_purposes(img_name[4], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'black', 1, 19, ps)
    verify_calibration_for_test_purposes(img_name[5], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'black', 19, 19, ps)
    verify_calibration_for_test_purposes(img_name[6], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'black', 19, 1, ps)
    verify_calibration_for_test_purposes(img_name[7], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'black', 10, 10, ps)
    verify_calibration_for_test_purposes(img_name[8], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'black', 4, 4, ps)
    verify_calibration_for_test_purposes(img_name[9], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'black', 4, 10, ps)
    verify_calibration_for_test_purposes(img_name[10], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'black', 4, 16, ps)
    verify_calibration_for_test_purposes(img_name[11], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'black', 16, 16, ps)
    verify_calibration_for_test_purposes(img_name[12], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'white', 1, 1, ps)
    verify_calibration_for_test_purposes(img_name[13], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'white', 10, 10, ps)
    verify_calibration_for_test_purposes(img_name[14], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'white', 16, 16, ps)
    verify_calibration_for_test_purposes(img_name[15], ob, x_idx, y_idx, \
                red_scale_th, blue_scale_th, 'white', 19, 19, ps)

    # DIGITAL BOARD DETECTION

    # Ask the user to open a KGS board
    print('\n   OPEN A KGS BOARD/GAME NOW')
    input('ENTER when the digital board is open: ')

    # Get the user to click on come corners to get to know the digital board
    UL_x, UL_y, goban_step = src.get_goban_corners()

    # START REPLAYING PYHSICAL BOARD MOVES ON THE DIGITAL BOARD
    mouse = Controller() # obtain mouse controller
    print("Placing a black stone at (10,10)")
    bxy, wxy = [], []   # empty board in the beginning
    color, i, j = src.scan_next_move(img_name[7], ob, x_idx, y_idx, \
                        red_scale_th, blue_scale_th, bxy, wxy, plot_stuff=ps)
    _, _ = src.play_next_move_on_digital_board(mouse, color, i, j, bxy, wxy, \
                                                    UL_x, UL_y, goban_step)


def verify_calibration_for_test_purposes(img, ob, x, y, r, b, c, i, j, ps):
    rgb = imageio.imread(img)
    rgb = src.rescale_pyhsical_goban_rgb(rgb, ob)
    print(f"Verifying a {c} stone at {src.convert_physical_board_ij_to_str(i,j)}...")
    assert src.is_this_stone_on_the_board(rgb, x, y, r, b, c, i, j, ps)
