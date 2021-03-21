from inky.inky_uc8159 import Inky, CLEAN
import time
import paho.mqtt.client as mqtt
import sys
from PIL import Image, ImageDraw, ImageFont

if(len(sys.argv)<3):
    print("first argument mqtt server, second topic")
    quit

inky = Inky()



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(sys.argv[2])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    array=msg.payload.split(";",10)
    cmd=array[0]
    print(cmd)
    if(cmd=="cls"):
	clean()
    if(cmd=="showbuffer"):
	show_buffer()
    if(cmd=="helloworld"):
        write_text("Hello world!",0,0,(0,0,0,255))
    if(cmd=="writetext"):
        write_text(array[1],int(array[2]),int(array[3]),(int(array[4]),int(array[5]),int(array[6]),255))

def clean():
    global buffer
    buffer = Image.new("RGB",(inky.width,inky.height),(255,255,255))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
print(sys.argv[1])
buffer = Image.new("RGB",(inky.width,inky.height),(255,255,255))
font = ImageFont.truetype("whitrabt.ttf", 25)

def show_buffer():
    inky.set_image(buffer,1)
    inky.show()

def write_text(text, x, y, color):
    d = ImageDraw.Draw(buffer)
    d.text((x, y), text, fill=color,font=font)

client.connect(sys.argv[1], 1883, 60)
client.loop_forever()
