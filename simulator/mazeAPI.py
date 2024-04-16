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
        # Acquire a lock to ensure thread safety when accessing shared serializedMaze
        with self.lock:
            # Find the cell and robot using the updated find_robot_cell method
            robot_cell, robot = self.find_robot_cell(robot_id)
            
            if not robot_cell or not robot:
                print("Robot not found or missing robot cell")
                return
            
            if self.sense_WallFront(robot_id):
                print("Wall here, cannot move forward")
                return

            # Calculate the new position based on the robot's direction
            direction = robot["direction"]
            i_value, j_value = robot_cell["i"], robot_cell["j"]
            if direction == 'N':
                j_value -= 1
            elif direction == 'E':
                i_value += 1
            elif direction == 'S':
                j_value += 1
            elif direction == 'W':
                i_value -= 1

            # Find the new cell based on the new position and update the robot's location
            new_cell = next((cell for cell in self.serializedMaze if cell["i"] == i_value and cell["j"] == j_value), None)
            if new_cell:
                # Remove robot from current cell
                for r in robot_cell["robots"]:
                    if r["id"] == robot_id:
                        r["isHere"] = False
                        break

                # Update robot in new cell
                for r in new_cell["robots"]:
                    if r["id"] == robot_id:
                        r["isHere"] = True
                        r["visited"] = True
                        r["direction"] = direction
                        # The robot's direction remains the same
                        print(f"move_forward - new cell: {i_value}, {j_value}, direction: {direction}")
                        break

            # Emit the updated serialized maze state to the frontend
            print("Final maze data before emit:", self.serializedMaze)
            time.sleep(0.05)
            self.socketio.emit('update_maze', {'updatedMaze': self.serializedMaze})


    def move_backward(self, robot_id):
        # Lock the method to ensure thread safety
        with self.lock:
            # Find the robot and its cell
            robot_cell, robot = self.find_robot_cell(robot_id)
            if not robot_cell or not robot:
                return None
            
            # Check for a wall in the opposite direction to where the robot is facing
            if self.sense_WallBack(robot_id):
                print("Wall here, cannot move backward")
                return
            
            # Determine the new position based on the direction the robot is facing
            direction = robot['direction']
            i_value, j_value = robot_cell['i'], robot_cell['j']
            if direction == 'N':
                j_value += 1
            elif direction == 'E':
                i_value -= 1
            elif direction == 'S':
                j_value -= 1
            elif direction == 'W':
                i_value += 1

            # Update the robot's position in the maze
            for cell in self.serializedMaze:
                if cell['i'] == i_value and cell['j'] == j_value:
                    # Move the robot to the new cell
                    robot['isHere'] = False  # Set the current cell's robot presence to False
                    cell['robots'][robot_id-1]['isHere'] = True  # Update the new cell's robot presence
                    cell['robots'][robot_id-1]['visited'] = True  # Mark the new cell as visited
                    cell["direction"] = direction

                    print(f"move_backward - new cell: {cell}")
                    break
            
            # Emit the updated serialized maze to the frontend
            time.sleep(0.05)
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



        