import simulator.mazeAPI as mazeAPI

def execute_algorithm(algorithm_code, serializedMaze, socketio):
    # Prepare the local context for exec, including API functions and the maze
    maze_simulator = mazeAPI.MazeSimulator(serializedMaze, socketio)
    print("Maze simulator object created")
    local_context = {
        "sense_WallLeft": maze_simulator.sense_WallLeft,
        "sense_WallRight": maze_simulator.sense_WallRight,
        "sense_WallFront": maze_simulator.sense_WallFront,
        "sense_WallBack": maze_simulator.sense_WallBack,
        "turn_left": maze_simulator.turn_left,
        "turn_right": maze_simulator.turn_right,
        "move_forward": maze_simulator.move_forward,
        "move_backward": maze_simulator.move_backward,
        "all_cells_visited": maze_simulator.all_cells_visited,
    }

    # Execute the algorithm code within the provided context
    exec(algorithm_code, local_context, local_context)

    # After execution, the maze_simulator.serializedMaze holds the updated state
    return maze_simulator.serializedMaze