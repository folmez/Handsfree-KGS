import src
import time

UL_x, UL_y, goban_step = src.get_goban_corners()

prev_stone_set = set()
print("Started scanning the board for moves every 5 seconds...")
while True:
    # wait between screenshots
    time.sleep(5)
    # get board screenshot
    board_rgb_screenshot = src.KGS_goban_rgb_screenshot(UL_x, UL_y, goban_step)
    # find the stones on the board
    current_stone_set = src.get_goban_state(board_rgb_screenshot)
    # is there a new stone on the board?
    if current_stone_set > prev_stone_set:
        # find the new stone
        stone = current_stone_set - prev_stone_set
        # IN THE FUTURE, ALLOW FOR OPPONENT TO MAKE A QUICK MOVE!!!
        assert len(stone) == 1
        # say the new moves on the board
        player = list(stone)[0][0] # 1-black, 2-white
        i, j = list(stone)[0][1], list(stone)[0][2]
        pos = src.int_coords_to_str(i,j)
        if player==1:
            update_msg = "Black played at " + pos
        elif player==2:
            update_msg = "White played at " + pos
        print(update_msg)
        prev_stone_set = current_stone_set
    else:
        print("No moves made!")
