from flask import Flask, request, jsonify
from flask_cors import CORS
from testingFiles.sampleData import serializedMaze , algorithm_code
import simulator.maze_simulation as maze_simulation  # Assuming maze_simulation.py will handle the execution of the algorithm.
import simulator.mazeAPI as mazeAPI  # This will contain the maze-specific API functions.
import hardware.execution as hardware_execution # This will contain the hardware-specific execution
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

@app.route('/run', methods=['POST'])
def run_simulation():
    # Extract the algorithm code and serialized maze from the request.

    data = request.json
    #algorithm_code = data['algorithm_code']
    #serialized_maze = data['serializedMaze']
    
    # Debug print statements to check the received data.
    print("Received algorithm code")
    print("Received serialized maze data")
    serialized_maze = serializedMaze
    # This will be integrated in future steps.
    result = maze_simulation.execute_algorithm(algorithm_code, serialized_maze)
    
    # Send back a placeholder response for now.

    #print(result)
    #return jsonify({"message": "Simulation run successfully", "updatedMaze": result})
    return jsonify({"message": "Simulation run successfully"})


@app.route('/upload_to_bot', methods=['POST'])
def upload_to_bot():
    data = request.json
    algorithm_code = data.get('algorithm_code')
    
    if not algorithm_code:
        return jsonify({"error": "Algorithm code is missing"}), 400
    
    print(algorithm_code)

    # Upload the algorithm code to the bot.
    hardware_execution.send_code_to_robot(algorithm_code)
    print("Uploading algorithm code to bot")
    
    return jsonify({"message": "Algorithm code uploaded to bot successfully"})


if __name__ == '__main__':
    app.run(debug=True)
