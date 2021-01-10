import paho.mqtt.client as mqtt
import sys


if(len(sys.argv)<3):
    print("first argument mqtt server, second topic")
    quit

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(sys.argv[2])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
print(sys.argv[1])
client.connect(sys.argv[1], 1883, 60)
client.loop_forever()