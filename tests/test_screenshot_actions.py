from scipy import misc
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src

def test_get_goban_state():
    rgb_pix = misc.imread('images/digital_goban.png')

    # Process KGS goban grayscale and find the stones
    assert src.get_goban_state(rgb_pix) == \
                set([(1,1,1), (1, 14, 1), (2,19,19)])
