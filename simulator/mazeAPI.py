import sys
import threading
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
        return None


    def all_cells_visited(self, robot_id): #TODO: still need to work on for 2 robots
        return all(cell.get("robotVisited", False) for cell in self.serializedMaze)
    
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
                        # The robot's direction remains the same
                        print(f"move_forward - new cell: {i_value}, {j_value}, direction: {direction}")
                        break

            # Emit the updated serialized maze state to the frontend
            self.socketio.emit('update_maze', {'updatedMaze': self.serializedMaze})


    def move_backward(self):
        robot_cell = self.find_robot_cell()
        #print("move_backward - original cell: {robot_cell}", robot_cell)
        if not robot_cell:
            return None
        
        # The opposite direction to sense_WallBack since we're moving backward.
        if self.sense_WallBack():
            sys.exit("Wall here cannot move backward")

        i_value = robot_cell["i"]
        j_value = robot_cell["j"]

        # Clear current robot position
        for cell in self.serializedMaze:
            if cell["i"] == i_value and cell["j"] == j_value:
                cell["isRobotHere"] = False
                break

        direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        wall_index = direction_to_index.get(robot_cell["robotDirection"])

        # Adjust i or j value based on the robot's direction to move backward
        if wall_index is not None:
            if wall_index == 0:  # If facing North, move South
                j_value += 1
            elif wall_index == 1:  # If facing East, move West
                i_value -= 1
            elif wall_index == 2:  # If facing South, move North
                j_value -= 1
            elif wall_index == 3:  # If facing West, move East
                i_value += 1

        # Set the new position of the robot
        for cell in self.serializedMaze:
            if cell["i"] == i_value and cell["j"] == j_value:
                cell["isRobotHere"] = True
                cell["robotVisited"] = True
                cell["robotDirection"] = robot_cell["robotDirection"]
                print("move_backward - new cell: {cell}", cell)
                break
        

        self.socketio.emit('update_maze', {'updatedMaze': self.serializedMaze})

    def turn_left(self):
        robot_cell = self.find_robot_cell()
        if not robot_cell:
            return None
        
        direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

        if wall_index is not None:
            if wall_index == 0: 
                for cell in self.serializedMaze:
                    if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                        cell["robotDirection"] = 'W'
                        print("facing west: " + cell["robotDirection"])
                        break
            elif wall_index == 1:
                for cell in self.serializedMaze:
                    if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                        cell["robotDirection"] = 'N'
                        print("facing north: " + cell["robotDirection"])
                        break
            elif wall_index == 2:
                for cell in self.serializedMaze:
                    if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                        cell["robotDirection"] = 'E'
                        print("facing east: " + cell["robotDirection"])
                        break
            elif wall_index == 3:
                for cell in self.serializedMaze:
                    if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                        cell["robotDirection"] = 'S'
                        print("facing south: " + cell["robotDirection"])
                        break

        self.socketio.emit('update_maze', {'updatedMaze': self.serializedMaze})

    def turn_right(self):
        
        robot_cell = self.find_robot_cell()
        if not robot_cell:
            return None
        
        direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

        if wall_index is not None:
            if wall_index == 0: 
                for cell in self.serializedMaze:
                    if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                        cell["robotDirection"] = 'E'
                        #print("facing east: " + cell["robotDirection"])
                        break
            elif wall_index == 1:
                for cell in self.serializedMaze:
                    if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                        cell["robotDirection"] = 'S'
                        #print("facing south: " + cell["robotDirection"])
                        break
            elif wall_index == 2:
                for cell in self.serializedMaze:
                    if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                        cell["robotDirection"] = 'W'
                        #print("facing west: " + cell["robotDirection"])
                        break
            elif wall_index == 3:
                for cell in self.serializedMaze:
                    if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                        cell["robotDirection"] = 'N'
                        #print("facing north: " + cell["robotDirection"])
                        break


        self.socketio.emit('update_maze', {'updatedMaze': self.serializedMaze})


        