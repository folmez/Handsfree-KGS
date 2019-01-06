from pynput.mouse import Button, Controller
import time

def get_goban_corners():
    # Obtain mouse controller
    mouse = Controller()

    # Ask the user to define goban corners
    print('Move cursor to upper-left (A19) corner of Goban and keep it there five seconds')
    time.sleep(5)
    (UL_x, UL_y) = mouse.position
    print(f"Upper-Left: ({UL_x},{UL_y})")

    print('Move cursor to bottom-right (T1) corner of Goban and keep it there five seconds')
    time.sleep(5)
    (BR_x, BR_y) = mouse.position
    print(f"Bottom-Right: ({BR_x},{BR_y})")

    # Compute goban step size
    goban_step = 0.5*(BR_x - UL_x)*1/18 + 0.5*(BR_y - UL_y)*1/18
    print(f"Goban-step is {goban_step}")

    return UL_x, UL_y, goban_step

def make_the_move(mouse, x, y):
    (cx, cy) = mouse.position
    time.sleep(3)
    mouse.move(x - cx, y - cy)
    time.sleep(1)
    mouse.click(Button.left, 1)

def int_coords_to_screen_coordinates(UL_x, UL_y, i, j, goban_step):
    x = UL_x + (i-1) * goban_step
    y = UL_y + (j-1) * goban_step
    return x, y

def str_to_integer_coordinates(str):
    # Upper-lef corner is 1,1 and Bottom-right corner is 19,19
    # Goban boards skip the letter I
    j = 19 - int(str[1:3]) + 1
    if ord(str[0]) < ord('I'):
        i = ord(str[0]) - ord('A') + 1
    else:
        i = ord(str[0]) - ord('A')
    return i,j
