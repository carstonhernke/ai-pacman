# grid.py

# grid size is 152x x 168y (19x14)
# start at 170, 5 as 0,0
# rectangles that are 12 tall and 8 wide

def find_grid_coordinates(old_coordinates):
    new_x = (old_coordinates[0]-6) / 8
    new_y = (170-old_coordinates[1]) / 12
    return (new_x, new_y)
