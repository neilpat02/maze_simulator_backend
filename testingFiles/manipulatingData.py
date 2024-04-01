from sampleData import serializedMaze
import sys

# THIS SCRIPT IS SIMPLY FOR UNDERSTANDING HOW TO ACCESS AND MANIPULATE PARTS OF THE SERIALIZED MAZE DATA

#def main():
#
#    serializedMazeCopy = serializedMaze #for manipulating data w/o actually tampering the original test dataset 
#
#    """The following 3 lines are accessing data via index in the serialized Maze """
#    indexValue = 0
#    cellByIndex = serializedMazeCopy[indexValue]
#    #print(cellByIndex)
#
#
#    """ The following lines is how to call the serializedMaze data via an index"""
#    i_value = 14
#    j_value = 12
#    cell_by_ij = None
#    for cell in serializedMaze:
#        if cell["i"] == i_value and cell["j"] == j_value:
#            cell_by_ij = cell
#            break
#    #print(cell_by_ij)
#
#    """ The following lines is how to find the exact cell where "isRobotHere" is true in serializedMaze """
#    robot_cell = None
#    for cell in serializedMaze:
#        if cell["isRobotHere"]:
#            robot_cell = cell
#            break   
#    print(robot_cell)
#
#    "The following is how to access the various data within each cell"
#    getWalls = robot_cell["walls"]
#    getRobotVisited = robot_cell["robotVisited"]
#    getRobotDirection = robot_cell["robotDirection"]
#    print(getWalls)
#    print(getRobotVisited)
#    print(getRobotDirection)
#
#
#    """ The following lines is how to find the cells where either robotVisited is true or false"""
#    visited_true = []
#    visited_false = []
#    for cell in serializedMaze:
#        if cell["robotVisited"]:
#            visited_true.append(cell)
#        else:
#            visited_false.append(cell)
#
#    #print(visited_false)
#    #print(visited_true)
#
#    return 0







def sense_WallFront(serializedMaze):
    robot_cell = find_robot_cell(serializedMaze)
    if not robot_cell:
        return None
    
    # Mapping of directions to wall index
    direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    wall_index = direction_to_index.get(robot_cell["robotDirection"], None)
    print(wall_index)

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

def sense_WallBack(serializedMaze):
    robot_cell = find_robot_cell(serializedMaze)
    if not robot_cell:
        return None
    
    # Mapping of directions to wall index
    direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

    if wall_index is not None:
        if wall_index == 0: 
            print(robot_cell["walls"][2])
        elif wall_index == 1:
            print(robot_cell["walls"][3])
        elif wall_index == 2:
            print(robot_cell["walls"][0])
        elif wall_index == 3:
            print(robot_cell["walls"][1])
    
    return None

def sense_WallRight(serializedMaze):
    robot_cell = find_robot_cell(serializedMaze)
    if not robot_cell:
        return None
    
    # Mapping of directions to wall index
    direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

    if wall_index is not None:
        if wall_index == 0: 
            print(robot_cell["walls"][1])
        elif wall_index == 1:
            print(robot_cell["walls"][2])
        elif wall_index == 2:
            print(robot_cell["walls"][3])
        elif wall_index == 3:
            print(robot_cell["walls"][0])
    
    return None

def sense_WallLeft(serializedMaze):
    robot_cell = find_robot_cell(serializedMaze)
    if not robot_cell:
        return None
    
    # Mapping of directions to wall index
    direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

    if wall_index is not None:
        if wall_index == 0: 
            print(robot_cell["walls"][3])
        elif wall_index == 1:
            print(robot_cell["walls"][2])
        elif wall_index == 2:
            print(robot_cell["walls"][1])
        elif wall_index == 3:
            print(robot_cell["walls"][0])
    
    return None


def move_forward(serializedMaze):
    robot_cell = find_robot_cell(serializedMaze)
    if sense_WallFront(serializedMaze):
        sys.exit("Wall here cannot move forward")
    i_value = robot_cell["i"]
    j_value = robot_cell["j"]

    for cell in serializedMaze:
        if cell["i"] == i_value and cell["j"] == j_value:
            cell["isRobotHere"] = False
            break

    direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    wall_index = direction_to_index.get(robot_cell["robotDirection"])
    print(wall_index)
    if wall_index is not None:
        if wall_index == 0:
            j_value -= 1
        elif wall_index == 1:
            i_value -= 1
        elif wall_index == 2:
            j_value += 1
        elif wall_index == 3:
            i_value += 1



    for cell in serializedMaze:
        if cell["i"] == i_value and cell["j"] == j_value:
            cell["isRobotHere"] = True
            cell["robotVisited"] = True
            cell["robotDirection"] = robot_cell["robotDirection"]

            break
    

    if not robot_cell:
        return None
    
    #print(robot_cell["robotDirection"])


def move_backward(serializedMaze):
    robot_cell = find_robot_cell(serializedMaze)
    if not robot_cell:
        return None
    
    # The opposite direction to sense_WallBack since we're moving backward.
    if sense_WallBack(serializedMaze):
        sys.exit("Wall here cannot move backward")

    i_value = robot_cell["i"]
    j_value = robot_cell["j"]

    # Clear current robot position
    for cell in serializedMaze:
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
    for cell in serializedMaze:
        if cell["i"] == i_value and cell["j"] == j_value:
            cell["isRobotHere"] = True
            cell["robotVisited"] = True
            cell["robotDirection"] = robot_cell["robotDirection"]
            break

def turn_left(serializedMaze):
    robot_cell = find_robot_cell(serializedMaze)
    if not robot_cell:
        return None
    
    direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

    if wall_index is not None:
        if wall_index == 0: 
            for cell in serializedMaze:
                if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                    cell["robotDirection"] = 'W'
                    break
        elif wall_index == 1:
            for cell in serializedMaze:
                if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                    cell["robotDirection"] = 'N'
                    break
        elif wall_index == 2:
            for cell in serializedMaze:
                if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                    cell["robotDirection"] = 'E'
                    break
        elif wall_index == 3:
            for cell in serializedMaze:
                if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                    cell["robotDirection"] = 'S'
                    break
    
def turn_right(serializedMaze):
    robot_cell = find_robot_cell(serializedMaze)
    if not robot_cell:
        return None
    
    direction_to_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    wall_index = direction_to_index.get(robot_cell["robotDirection"], None)

    if wall_index is not None:
        if wall_index == 0: 
            for cell in serializedMaze:
                if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                    cell["robotDirection"] = 'E'
                    break
        elif wall_index == 1:
            for cell in serializedMaze:
                if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                    cell["robotDirection"] = 'S'
                    break
        elif wall_index == 2:
            for cell in serializedMaze:
                if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                    cell["robotDirection"] = 'W'
                    break
        elif wall_index == 3:
            for cell in serializedMaze:
                if cell["i"] == robot_cell["i"] and cell["j"] == robot_cell["j"]:
                    cell["robotDirection"] = 'N'
                    break


def find_robot_cell(serializedMaze):
    return next((cell for cell in serializedMaze if cell["isRobotHere"]), None)

if __name__ == '__main__':
    serializedMazeCopy = serializedMaze
    #sense_WallFront(serializedMazeCopy)
    turn_left(serializedMazeCopy)
    print(serializedMazeCopy[0])
    turn_right(serializedMazeCopy)
    print(serializedMazeCopy[0])
    turn_left(serializedMazeCopy)
    print(serializedMazeCopy[0])
    turn_right(serializedMazeCopy)
    print(serializedMazeCopy[0])
#    i_value = 0
#    j_value = 1
#    cell_by_ij = None
#    for cell in serializedMaze:
#        if cell["i"] == i_value and cell["j"] == j_value:
#            cell_by_ij = cell
#            break
#    print(cell_by_ij)

