import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the variables
broker_url = os.getenv('MQTT_BROKER_URL')
port = int(os.getenv('MQTT_PORT'))
username = os.getenv('MQTT_USERNAME')
password = os.getenv('MQTT_PASSWORD')

# MQTT Callbacks
def on_connect(client, userdata, flags, rc, properties=None):  # Add properties=None
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("/student_group/light_control")  # Subscribe to the topic
    else:
        print(f"Failed to connect, return code: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if payload == "ON":
        print("💡 Light is TURNED ON")
    elif payload == "OFF":
        print("💡 Light is TURNED OFF")
    else:
        print(f"Received unknown payload: {payload}")

# Use latest callback API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set authentication
client.username_pw_set(username, password)

# Use TLS (required for HiveMQ Cloud)
client.tls_set(certfile=None, keyfile=None, cert_reqs=mqtt.ssl.CERT_NONE)  # Disable certificate validation

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message

# Try connecting
try:
    print("Connecting to broker...")
    client.connect(broker_url, port, 60)
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)  # Exit the script if connection fails

# Keep the script running
client.loop_forever()