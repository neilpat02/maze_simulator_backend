import sys
import threading
import time

class ControlFlag:
    stop_threads = False

class MazeSimulator:

    def __init__(self, serializedMaze, socketio):
        self.serializedMaze = serializedMaze
        self.socketio = socketio
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.score = 600  # Initial Time Score (ITS)
        self.visited_cells = set()
        self.emit_score()

    def emit_score(self):
        """Emit the current score to all connected clients."""
        self.socketio.emit('update_score', {'score': self.score})

    def update_score_for_time(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 60:  # After the first 60 seconds
            reduction_periods = (elapsed_time - 60) // 5
            self.score -= 12.5 * reduction_periods
            self.start_time = time.time()  # Reset start time for next period
        self.emit_score()

    def find_robot_cell(self, robot_id):
        for cell in self.serializedMaze:
            for robot in cell["robots"]:
                if robot["id"] == robot_id and robot["isHere"]:
                    return cell, robot
        return None, None


    def all_cells_visited(self):
        # Check if all cells have been visited by at least one robot
        for cell in self.serializedMaze:
            if not any(robot['visited'] for robot in cell['robots']):
                return False
        return True

    
    def sense_WallFront(self, robot_id):
        # Use the modified find_robot_cell to accept a robot_id and find the cell for the specified robot
        robot_cell, robot = self.find_robot_cell(robot_id)
        if not robot_cell or not robot:
            return None
        
        # Mapping of directions to wall index
        direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        wall_index = direction_to_index.get(robot["direction"], None)  # Use robot's direction from the updated structure

        if wall_index is not None:
            print(robot_cell["walls"][wall_index])
            return robot_cell["walls"][wall_index]
        
        return None

    def sense_WallBack(self, robot_id):
        # Use the modified find_robot_cell to accept a robot_id and find the cell for the specified robot
        robot_cell, robot = self.find_robot_cell(robot_id)
        if not robot_cell or not robot:
            return None
        
        # Mapping of directions to wall index and their opposites
        direction_to_index = {'N': 2, 'E': 3, 'S': 0, 'W': 1}  # Directly map to opposite wall index
        wall_index = direction_to_index.get(robot["direction"], None)

        if wall_index is not None:
            print(robot_cell["walls"][wall_index])
            return robot_cell["walls"][wall_index]
        
        return None

    def sense_WallLeft(self, robot_id):
        # Use the modified find_robot_cell to accept a robot_id and find the cell for the specified robot
        robot_cell, robot = self.find_robot_cell(robot_id)
        if not robot_cell or not robot:
            return None
        
        # Mapping of directions to their left wall index
        direction_to_index = {'N': 3, 'E': 0, 'S': 1, 'W': 2}  # Maps each direction to the left wall index
        wall_index = direction_to_index.get(robot["direction"], None)

        if wall_index is not None:
            print(robot_cell["walls"][wall_index])
            return robot_cell["walls"][wall_index]
        
        return None

    def sense_WallRight(self, robot_id):
        # Use the modified find_robot_cell to accept a robot_id and find the cell for the specified robot
        robot_cell, robot = self.find_robot_cell(robot_id)
        if not robot_cell or not robot:
            return None
        
        # Mapping of directions to their right wall index
        direction_to_index = {'N': 1, 'E': 2, 'S': 3, 'W': 0}  # Maps each direction to the right wall index
        wall_index = direction_to_index.get(robot["direction"], None)

        if wall_index is not None:
            print(robot_cell["walls"][wall_index])
            return robot_cell["walls"][wall_index]
        
        return None


    def move_forward(self, robot_id):
            with self.lock:
                robot_cell, robot = self.find_robot_cell(robot_id)
                if not robot_cell or not robot:
                    print(f"Robot {robot_id} not found or missing robot cell")
                    return

                if self.sense_WallFront(robot_id):
                    print(f"Robot {robot_id} at {robot_cell['i']}, {robot_cell['j']} cannot move forward due to wall")
                    return

                direction = robot["direction"]
                movement_offsets = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
                i_offset, j_offset = movement_offsets[direction]
                new_i, new_j = robot_cell["i"] + i_offset, robot_cell["j"] + j_offset

                new_cell = next((cell for cell in self.serializedMaze if cell["i"] == new_i and cell["j"] == new_j), None)
                if not new_cell:
                    print(f"New cell at {new_i}, {new_j} does not exist for Robot {robot_id}")
                    return

                robot["isHere"] = False
                new_robot = next((r for r in new_cell["robots"] if r["id"] == robot_id), None)
                if new_robot:
                    if not new_robot["isHere"]:
                        new_robot["isHere"] = True
                        new_robot["direction"] = direction
                        if not new_robot["visited"]:
                            new_robot["visited"] = True
                            if (new_i, new_j) not in self.visited_cells:  # Check if cell is visited for the first time
                                self.visited_cells.add((new_i, new_j))  # Add cell to visited set
                                self.score += 2  # Add score for visiting a new cell
                                self.emit_score()
                                print(f"Robot {robot_id} visited new cell {new_i}, {new_j} for the first time")
                print(f"Moved forward to {new_i}, {new_j}, direction: {direction}")
                self.socketio.emit('update_maze', {'updatedMaze': self.serializedMaze})



    def move_backward(self, robot_id):
        with self.lock:
            robot_cell, robot = self.find_robot_cell(robot_id)
            if not robot_cell or not robot:
                print(f"Robot {robot_id} not found or missing robot cell")
                return

            if self.sense_WallBack(robot_id):
                print(f"Robot {robot_id} at {robot_cell['i']}, {robot_cell['j']} cannot move backward due to wall")
                return

            direction = robot['direction']
            movement_offsets = {'N': (0, 1), 'E': (-1, 0), 'S': (0, -1), 'W': (1, 0)}
            i_offset, j_offset = movement_offsets[direction]
            new_i, new_j = robot_cell["i"] + i_offset, robot_cell["j"] + j_offset

            new_cell = next((cell for cell in self.serializedMaze if cell["i"] == new_i and cell["j"] == new_j), None)
            if not new_cell:
                print(f"New cell at {new_i}, {new_j} does not exist for Robot {robot_id}")
                return

            robot["isHere"] = False
            new_robot = next((r for r in new_cell["robots"] if r["id"] == robot_id), None)
            if new_robot:
                if not new_robot["isHere"]:
                    new_robot["isHere"] = True
                    new_robot["direction"] = direction
                    if not new_robot["visited"]:
                        new_robot["visited"] = True
                        if (new_i, new_j) not in self.visited_cells:  # Check if cell is visited for the first time
                            self.visited_cells.add((new_i, new_j))  # Add cell to visited set
                            self.score += 2  # Add score for visiting a new cell
                            self.emit_score()
                            print(f"Robot {robot_id} visited new cell {new_i}, {new_j} for the first time")
                print(f"Robot {robot_id} moved backward to new cell {new_i}, {new_j}")

            self.socketio.emit('update_maze', {'updatedMaze': self.serializedMaze})




    def turn_left(self, robot_id):
        # Locking to ensure thread safety during the update
        with self.lock:
            # Find the specific robot and its cell
            robot_cell, robot = self.find_robot_cell(robot_id)
            if not robot_cell or not robot:
                return None
            
            # Current direction of the robot
            current_direction = robot['direction']
            
            # Mapping to find the new direction when turning left
            left_turn_map = {'N': 'W', 'E': 'N', 'S': 'E', 'W': 'S'}
            new_direction = left_turn_map.get(current_direction, current_direction)  # Stay in current direction if undefined
            
            # Update the robot's direction in the maze
            robot['direction'] = new_direction
            print(f"Robot {robot_id} now facing: {new_direction}")
            
            # Emit the updated serialized maze to the frontend
            time.sleep(0.05)
            self.socketio.emit('update_maze', {'updatedMaze': self.serializedMaze})

    def turn_right(self, robot_id):
        # Locking to ensure thread safety during the update
        with self.lock:
            # Find the specific robot and its cell
            robot_cell, robot = self.find_robot_cell(robot_id)
            if not robot_cell or not robot:
                return None
            
            # Current direction of the robot
            current_direction = robot['direction']
            
            # Mapping to find the new direction when turning right
            right_turn_map = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
            new_direction = right_turn_map.get(current_direction, current_direction)  # Stay in current direction if undefined
            
            # Update the robot's direction in the maze
            robot['direction'] = new_direction
            print(f"Robot {robot_id} now facing: {new_direction}")
            
            # Emit the updated serialized maze to the frontend
            time.sleep(0.05)
            self.socketio.emit('update_maze', {'updatedMaze': self.serializedMaze})



        