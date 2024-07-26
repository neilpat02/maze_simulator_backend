import threading
import simulator.mazeAPI as mazeAPI
import time 
from simulator.mazeAPI import ControlFlag
import sys

def trace_func(frame, event, arg):
    if ControlFlag.stop_threads:
        raise SystemExit("Terminating thread.")
    return trace_func

def execute_algorithm_for_robot(robot_id, algorithm_code, maze_simulator):
    # Create a copy of local context specific to this thread and robot
    local_context = {
        "sense_WallLeft": lambda: maze_simulator.sense_WallLeft(robot_id),
        "sense_WallRight": lambda: maze_simulator.sense_WallRight(robot_id),
        "sense_WallFront": lambda: maze_simulator.sense_WallFront(robot_id),
        "sense_WallBack": lambda: maze_simulator.sense_WallBack(robot_id),
        "turn_left": lambda: maze_simulator.turn_left(robot_id),
        "turn_right": lambda: maze_simulator.turn_right(robot_id),
        "move_forward": lambda: maze_simulator.move_forward(robot_id),
        "move_backward": lambda: maze_simulator.move_backward(robot_id),
        "all_cells_visited": maze_simulator.all_cells_visited  # Assuming this checks globally, not per robot
        # No need to pass "find_robot_cell" unless used directly in algorithm code
    }
    sys.settrace(trace_func)
    try:
        exec(algorithm_code, local_context, local_context)
    except SystemExit:
        print(f"Thread {robot_id} forcefully stopped.")
    finally:
        sys.settrace(None)

def execute_algorithm(algorithm_code, serializedMaze, socketio):
    ControlFlag.stop_threads = False
    maze_simulator = mazeAPI.MazeSimulator(serializedMaze, socketio)
    print("Maze simulator object created")

    threads = []
    # Extend the range to include robots 1 to 4
    for robot_id in [1, 2, 3, 4]:
        t = threading.Thread(target=execute_algorithm_for_robot, args=(robot_id, algorithm_code, maze_simulator))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return maze_simulator.serializedMaze
