from pynput.mouse import Button, Controller
import time
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src

def test_str_to_integer_coordinates():
    assert src.str_to_integer_coordinates('A19') == (1, 1)
    assert src.str_to_integer_coordinates('D16') == (4, 4)
    assert src.str_to_integer_coordinates('D10') == (4, 10)
    assert src.str_to_integer_coordinates('T1') == (19, 19)
    assert src.str_to_integer_coordinates('K10') == (10, 10)

def test_integer_coordinates_to_str():
    assert src.int_coords_to_str(1, 1) == 'A19'
    assert src.int_coords_to_str(4, 4) == 'D16'
    assert src.int_coords_to_str(4, 10) == 'D10'
    assert src.int_coords_to_str(19, 19) == 'T1'
    assert src.int_coords_to_str(10, 10) == 'K10'

@pytest.mark.slow
def test_place_stones_on_all_stars():
    print()
    # Get goban corners
    UL_x, UL_y, goban_step = src.get_goban_corners()

    # Obtain mouse controller
    mouse = Controller()

    # Place stones on stars
    print('\n', 41*'-')
    print(5*'-', 'Placing stones on all stars', 5*'-')
    print(41*'-', '\n')
    for str in ['D16', 'K16', 'Q16', 'D10', 'K10', 'Q10', 'D4', 'K4', 'Q4']:
        i, j = src.str_to_integer_coordinates(str)
        x, y = src.int_coords_to_screen_coordinates(UL_x, UL_y, i, j, goban_step)
        src.make_the_move(mouse, x, y)

    # Get KGS goban as a square grayscale
    rgb_pix = src.KGS_goban_grayscale(UL_x, UL_y, goban_step)
