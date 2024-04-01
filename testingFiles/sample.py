# Assuming sampleData.py is structured with algorithm_code and serializedMaze defined
from testingFiles.sampleData import algorithm_code, serializedMaze
# Mock imports for demonstration - you would replace these with actual implementations
import simulator.maze_simulation as maze_simulation




def run_simulation(algorithm_code, serializedMaze):
    # Call the function that handles execution within maze_simulation.py
    result = maze_simulation.execute_algorithm(algorithm_code, serializedMaze)
    return result

# Running the sample simulation with the mocked data
if __name__ == "__main__":
    result = run_simulation(algorithm_code, serializedMaze)
    if result is not None:
        print("Simulation completed successfully.")
        #print("Updated Maze:", result)
    else:
        print("Simulation failed.")
        print("Simulation failed.")
