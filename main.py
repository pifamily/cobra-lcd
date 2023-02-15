
import yaml
import paho.mqtt.client as mqtt
import sys
import json

config = yaml.safe_load(open("./config.yaml"))
drivers = config['drivers']
sys.path.append(drivers)

import drivers

display = drivers.Lcd()

broker_address=config['broker_address']
mqtt_port=config['mqtt_port']
client_name=config['client_name']
topic=config['topic']

#Callback
def on_message(client, userdata, message):
    try:
        display_msg = json.loads(message.payload.decode("utf-8"))
        line1 = display_msg['line1']
        line2 = display_msg['line2']
        display.lcd_clear()  
        display.lcd_display_string(line1, 1)
        display.lcd_display_string(line2, 2)
    except:
        print('Could not handle that message')
    

client = mqtt.Client(client_name) 
client.on_message=on_message
client.connect(broker_address, port=mqtt_port) 
client.subscribe(topic)

client.loop_forever()