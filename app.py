from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import simulator.maze_simulation as maze_simulation  # Assuming maze_simulation.py will handle the execution of the algorithm.
import simulator.mazeAPI as mazeAPI
from simulator.mazeAPI import ControlFlag  # This will contain the maze-specific API functions.
import hardware.execution as hardware_execution  # This will contain the hardware-specific execution

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True, async_mode='gevent')

@app.route('/run', methods=['POST'])
def run_simulation():
    data = request.json
    algorithm_code = data['algorithm_code']
    serialized_maze = data['serializedMaze']
    
    print("Received algorithm code:", algorithm_code)
    print("Received serialized maze data")

    updatedSerializedMaze = maze_simulation.execute_algorithm(algorithm_code, serialized_maze, socketio)
 
    socketio.emit('update_maze', {'updatedMaze': updatedSerializedMaze})

    return jsonify({"message": "Simulation is running", "updatedMaze": updatedSerializedMaze})

@app.route('/reset', methods=['POST'])
def reset_simulation():
    ControlFlag.stop_threads = True
    return jsonify({"message": "Simulation reset initiated"}), 200

@app.route('/upload_to_bot', methods=['POST'])
def upload_to_bot():
    data = request.json
    algorithm_code = data.get('algorithm_code')
    
    if not algorithm_code:
        return jsonify({"error": "Algorithm code is missing"}), 400
    
    print(algorithm_code)

    hardware_execution.send_code_to_robot(algorithm_code)
    print("Uploading algorithm code to bot")
    
    return jsonify({"message": "Algorithm code uploaded to bot successfully"})

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('0.0.0.0', 5001), app, handler_class=WebSocketHandler)
    server.serve_forever()
