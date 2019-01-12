from pynput.mouse import Button, Controller
import src
import time

def get_goban_corners():
    # Obtain mouse controller
    mouse = Controller()

    # Ask the user to define goban corners
    print('Move cursor to upper-left (A19) corner of Goban and keep it there five seconds')
    time.sleep(5)
    (UL_x, UL_y) = mouse.position
    print(f"Upper-Left: ({UL_x},{UL_y})")
    print()

    print('Move cursor to bottom-right (T1) corner of Goban and keep it there five seconds')
    time.sleep(5)
    (BR_x, BR_y) = mouse.position
    print(f"Bottom-Right: ({BR_x},{BR_y})")
    print()

    # Compute goban step sizes
    goban_step =  0.5 * (BR_x - UL_x) * 1/18 + 0.5 * (BR_y - UL_y) * 1/18
    print(f"Goban-steps is {goban_step}")

    return UL_x, UL_y, goban_step

def make_the_move(mouse, x, y, no_click=False):
    (cx, cy) = mouse.position
    time.sleep(0.5)
    mouse.move(x - cx, y - cy)
    time.sleep(0.2)
    if not no_click:
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

def int_coords_to_str(i, j):
    # Upper-lef corner is 1,1 and Bottom-right corner is 19,19
    # Goban boards skip the letter I
    if i <= ord('I') - ord('A'):
        return chr(ord('A') + i-1) + f"{20-j}"
    else:
        return chr(ord('A') + i) + f"{20-j}"
