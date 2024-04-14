import hardware.hardwareAPI as hardAPI

def send_code_to_robot(algorithm_code):
    # Initialize the hardware API or any necessary setup for the robot control
    hardware_control = hardAPI.HardwareControl()  # Assuming HardwareControl is a class in hardwareAPI

    # Prepare the local context for exec, including API functions for robot control
    local_context = {
        "sense_WallLeft": hardware_control.sense_WallLeft,
        "sense_WallRight": hardware_control.sense_WallRight,
        "sense_WallFront": hardware_control.sense_WallFront,
        "sense_WallBack": hardware_control.sense_WallBack,
        "turn_left": hardware_control.turn_left,
        "turn_right": hardware_control.turn_right,
        "move_forward": hardware_control.move_forward,
        "move_backward": hardware_control.move_backward,
        
    }

   ## Split the algorithm code into individual lines
   #code_lines = algorithm_code.split('\n')

   ## Execute each line of the algorithm within the local context
   #for line in code_lines:
   #    if line.strip():  # Ignore empty lines
   #        try:
   #            exec(line, local_context, local_context)
   #        except Exception as e:
   #            print(f"Error executing line: {line}\nError: {e}")
   #            # Handle any errors that occur during execution
    
    exec(algorithm_code, local_context, local_context)