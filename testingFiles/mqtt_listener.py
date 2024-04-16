#Test file to listen to the 'robot/control' and ensure correct data is being transmitted / handled


import paho.mqtt.client as mqtt

# Configuration for MQTT
MQTT_BROKER = 'test.mosquitto.org'
MQTT_PORT = 1883
MQTT_TOPIC = 'robot/control'



code_accumulator = []

# Callback when connecting to the MQTT server
def on_connect(client, userdata, flags, rc):
    #subscribe
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    if message == "EOF":
        # When EOF is received, write the accumulated code to a file
        with open('received_code.py', 'w') as code_file:
            for line in code_accumulator:
                code_file.write(line + '\n')
        print("Code has been written to received_code.py")
        client.disconnect()
    else:
        # Replace '^' with tabs and add to accumulator
        code_accumulator.append(message.replace('^', '\t'))

# Set up and start the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()