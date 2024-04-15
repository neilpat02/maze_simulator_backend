def solve_maze():
    # While not all cells are visited
    while not all_cells_visited():
        # Prioritize moving right if there's no wall
        if not sense_WallRight():
            turn_right()
            move_forward()
        # If there's a wall on the right, try moving forward
        elif not sense_WallFront():
            move_forward()
        # If there's a wall in front and on the right, try turning left
        elif not sense_WallLeft():
            turn_left()
        # If surrounded by walls on the right, front, and left, turn around
        else:
            turn_left()
            turn_left()

# Call the function to start solving the maze
solve_maze()
