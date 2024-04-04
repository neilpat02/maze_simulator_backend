import paho.mqtt.client as mqtt

class HardwareControl:
    def __init__(self):
        # Initialize the MQTT Client
        self.client = mqtt.Client()

        # Define the MQTT Broker Address (Replace with the actual address of your broker)
        self.mqtt_broker = 'test.mosquitto.org'

        # Set callback methods
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        # Connect to the MQTT Broker
        self.client.connect(self.mqtt_broker, 1883, 60)

        # Start the loop in the background (non-blocking)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT Broker")

    def publish_message(self, topic, message):
        # Publish a message to a given topic
        self.client.publish(topic, message)

    # Control and sensing functions with dummy return values
    def sense_WallLeft(self):
        self.publish_message("robot/control", "sense_WallLeft")
        print("Sent sense_WallLeft command")
        return False  # Dummy value

    def sense_WallRight(self):
        self.publish_message("robot/control", "sense_WallRight")
        print("Sent sense_WallRight command")
        return False  # Dummy value

    def sense_WallFront(self):
        self.publish_message("robot/control", "sense_WallFront")
        print("Sent sense_WallFront command")
        return False  # Dummy value

    def sense_WallBack(self):
        self.publish_message("robot/control", "sense_WallBack")
        print("Sent sense_WallBack command")
        return False  # Dummy value

    def turn_left(self):
        self.publish_message("robot/control", "turn_left")
        print("Sent turn_left command")

    def turn_right(self):
        self.publish_message("robot/control", "turn_right")
        print("Sent turn_right command")

    def move_forward(self):
        self.publish_message("robot/control", "move_forward")
        print("Sent move_forward command")

    def move_backward(self):
        self.publish_message("robot/control", "move_backward")
        print("Sent move_backward command")

## Example usage of the class
#if __name__ == "__main__":
#    hardware_control = HardwareControl()
#    # Test command to ensure setup is correct
#    hardware_control.move_forward()
#