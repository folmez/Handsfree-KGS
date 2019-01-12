import pytest
import imageio
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src

# stones - upper-left corner is (1,1), lower-left corner is (19,1)
IMG_PATH = ['images/pyshical_goban_pic1.png', 'images/pyshical_goban_pic2.png', \
            'images/pyshical_goban_pic3.png', 'images/pyshical_goban_pic4.png', \
            'images/pyshical_goban_pic5.png']
bxy0, wxy0 = [(4,4), (16,4)], [(4,16),(16,16)]
bxy1, wxy1 = [(1,9), (16,8)], [(10,1),(13,19)]
bxy2, wxy2 = [(1,19), (17,3)], [(1,3),(19,19)]
bxy3, wxy3 = [(1,19), (19,1), (5,4), (6,16), (12,8), (14,6), (16,10), (19,13)], \
            [(1,1), (4,10), (7,7), (10,4), (10,10), (12,11), (15,7), (19,19)]
bxy4, wxy4 = [(1,1), (19,19), (1,19), (19,1)], [(10,10)]
UL_outer_x0, UL_outer_y0 = 315, 24
UR_outer_x0, UR_outer_y0 = 999, 40
BL_outer_x0, BL_outer_y0 = 3, 585
BR_outer_x0, BR_outer_y0 = 1273, 621

UL_outer_x3, UL_outer_y3 = 321, 235
UR_outer_x3, UR_outer_y3 = 793, 244
BL_outer_x3, BL_outer_y3 = 92, 603
BR_outer_x3, BR_outer_y3 = 933, 608

UL_outer_x4, UL_outer_y4 = 414, 256
UR_outer_x4, UR_outer_y4 = 962, 269
BL_outer_x4, BL_outer_y4 = 217, 659
BR_outer_x4, BR_outer_y4 = 1211, 679

@pytest.mark.skip
def test_board_outer_corner():
    UL_outer_x0_click, UL_outer_y0_click, _, _, _, _, _, _ = \
        src.get_pyhsical_board_outer_corners(IMG_PATH[0])
    assert abs(UL_outer_x0_click - UL_outer_x0) < 5 # five pixels
    assert abs(UL_outer_y0_click - UL_outer_y0) < 5

def test_board_state_detection_from_camera_picture():
    assert_board_state(IMG_PATH[4], bxy4, wxy4, 'black', bxy4[0], \
                            UL_outer_x4, UL_outer_y4, UR_outer_x4, UR_outer_y4, \
                            BL_outer_x4, BL_outer_y4, BR_outer_x4, BR_outer_y4, \
                            plot_stuff=False)
    assert_board_state(IMG_PATH[0], bxy0, wxy0, 'black', bxy0[1], \
                            UL_outer_x0, UL_outer_y0, UR_outer_x0, UR_outer_y0, \
                            BL_outer_x0, BL_outer_y0, BR_outer_x0, BR_outer_y0)
    assert_board_state(IMG_PATH[1], bxy1, wxy1, 'white', wxy1[0], \
                            UL_outer_x0, UL_outer_y0, UR_outer_x0, UR_outer_y0, \
                            BL_outer_x0, BL_outer_y0, BR_outer_x0, BR_outer_y0, \
                            plot_stuff=True)
    assert_board_state(IMG_PATH[2], bxy2, wxy2, 'black', bxy2[0], \
                            UL_outer_x0, UL_outer_y0, UR_outer_x0, UR_outer_y0, \
                            BL_outer_x0, BL_outer_y0, BR_outer_x0, BR_outer_y0)
    assert_board_state(IMG_PATH[3], bxy3, wxy3, 'white', wxy3[6], \
                            UL_outer_x3, UL_outer_y3, UR_outer_x3, UR_outer_y3, \
                            BL_outer_x3, BL_outer_y3, BR_outer_x3, BR_outer_y3)

def assert_board_state(IMG_PATH, bxy, wxy, color, ij_pair, \
                        UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
                        BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y, \
                        plot_stuff=False):
    # Get RGB matrix of the picture with goban
    rgb = imageio.imread(IMG_PATH)

    # Remove non-goban part from the RGB matrix and make it a square matrix
    rgb = src.rescale_pyhsical_goban_rgb(rgb, \
                            UL_outer_x, UL_outer_y, UR_outer_x, UR_outer_y, \
                            BL_outer_x, BL_outer_y, BR_outer_x, BR_outer_y)

    # Find the indices of board points in the new square RGB matrix
    x_idx, y_idx = src.find_board_points(rgb, plot_stuff=plot_stuff)

    # Find color thresholds for stone detection
    red_scale_th, blue_scale_th = src.calibrate(rgb, x_idx, y_idx, bxy, wxy)

    # Refind stones using the above thresholds
    bxy_new, wxy_new = src.mark_stones(rgb, x_idx, y_idx, \
                                red_scale_th, blue_scale_th, plot_stuff=plot_stuff)

    assert set(bxy) == set(bxy_new)
    assert set(wxy) == set(wxy_new)
    assert src.is_this_stone_on_the_board(rgb, x_idx, y_idx, \
                red_scale_th, blue_scale_th, color, ij_pair[0], ij_pair[1], \
                plot_stuff=True)
