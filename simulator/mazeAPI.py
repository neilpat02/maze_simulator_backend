import sys
class MazeSimulator:

    def __init__(self, serializedMaze, socketio):
        self.serializedMaze = serializedMaze
        self.socketio = socketio

    def find_robot_cell(self):
        return next((cell for cell in self.serializedMaze if cell["isRobotHere"]), None)

    def all_cells_visited(self):
        return all(cell.get("robotVisited", False) for cell in self.serializedMaze)
    
    def sense_WallFront(self):
        robot_cell = self.find_robot_cell()
        if not robot_cell:
            return None
        
        # Mapping of directions to wall index
        direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        wall_index = direction_to_index.get(robot_cell["robotDirection"], None)
        #print(wall_index)

        if wall_index is not None:
            if wall_index == 0: #That means it is North facing so that it needs to return the wall from index 0
                #print(robot_cell["walls"][0])
                return robot_cell["walls"][0]
            elif wall_index == 1: #That means it is East facing so that it needs to return the wall from index 1
                #print(robot_cell["walls"][1])
                return robot_cell["walls"][1]
            elif wall_index == 2: #That means it is South facing so that it needs to return the wall from index 2
                #print(robot_cell["walls"][2])
                return robot_cell["walls"][2]
            elif wall_index == 3: #That means it is West facing so that it needs to return the wall from index 3
                #print(robot_cell["walls"][3])
                return robot_cell["walls"][3]
            
        return None

    def sense_WallBack(self):
        robot_cell = self.find_robot_cell()
        if not robot_cell:
            return None
        
        # Mapping of directions to wall index
        direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

        if wall_index is not None:
            if wall_index == 0: 
                #print(robot_cell["walls"][2])
                return robot_cell["walls"][2]
            elif wall_index == 1:
                #print(robot_cell["walls"][3])
                return robot_cell["walls"][3]
            elif wall_index == 2:
                #print(robot_cell["walls"][0])
                return robot_cell["walls"][0]
            elif wall_index == 3:
                #print(robot_cell["walls"][1])
                return robot_cell["walls"][1]
        
        return None

    def sense_WallLeft(self):
        robot_cell = self.find_robot_cell()
        if not robot_cell:
            return None
        
        # Mapping of directions to wall index
        direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

        if wall_index is not None:
            if wall_index == 0: 
                #print(robot_cell["walls"][3])
                return robot_cell["walls"][3]
            elif wall_index == 1:
                #print(robot_cell["walls"][2])
                return robot_cell["walls"][2]
            elif wall_index == 2:
                #print(robot_cell["walls"][1])
                return robot_cell["walls"][1]
            elif wall_index == 3:
                #print(robot_cell["walls"][0])
                return robot_cell["walls"][0]
        
        return None

    def sense_WallRight(self):
        robot_cell = self.find_robot_cell()
        if not robot_cell:
            return None
        
        # Mapping of directions to wall index
        direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

        if wall_index is not None:
            if wall_index == 0: 
                #print(robot_cell["walls"][1])
                return robot_cell["walls"][1]
            elif wall_index == 1:
                #print(robot_cell["walls"][2])
                return robot_cell["walls"][2]
            elif wall_index == 2:
                #print(robot_cell["walls"][3])
                return robot_cell["walls"][3]
            elif wall_index == 3:
                #print(robot_cell["walls"][0])
                return robot_cell["walls"][0]
        
        return None

    def move_forward(self):
        robot_cell = self.find_robot_cell()
        print("move_forward - original cell: {robot_cell}", robot_cell)
        if self.sense_WallFront():
            sys.exit("Wall here cannot move forward")
        i_value = robot_cell["i"]
        j_value = robot_cell["j"]

        for cell in self.serializedMaze:
            if cell["i"] == i_value and cell["j"] == j_value:
                cell["isRobotHere"] = False
                break

        direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        wall_index = direction_to_index.get(robot_cell["robotDirection"])
        #print(wall_index)
        if wall_index is not None:
            if wall_index == 0:
                j_value -= 1
            elif wall_index == 1:
                i_value += 1
            elif wall_index == 2:
                j_value += 1
            elif wall_index == 3:
                i_value -= 1



        for cell in self.serializedMaze:
            if cell["i"] == i_value and cell["j"] == j_value:
                cell["isRobotHere"] = True
                cell["robotVisited"] = True
                cell["robotDirection"] = robot_cell["robotDirection"]
                print("move_forward - new cell: {cell}", cell)

                break
        
        #print(self.serializedMaze)
    
        if not robot_cell:
            return None
        

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


        