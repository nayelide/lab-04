"""EE 250L Lab 04 Starter Code
Run vm_pub.py in a separate terminal on your VM.
https://github.com/nayelide/lab-04 """

import paho.mqtt.client as mqtt

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """

def on_connect(client, userdata, flags, rc):
    """Once our client has successfully connected, it makes sense to subscribe to
    all the topics of interest. Also, subscribing in on_connect() means that, 
    if we lose the connection and the library reconnects for us, this callback
    will be called again thus renewing the subscriptions"""

    print("Connected to server (i.e., broker) with result code "+str(rc))
    #replace user with your USC username in all subscriptions
    client.subscribe("nayelide/ping")
    
    
   #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add("nayelide/pong", on_message_from_ping)

"""This object (functions are objects!) serves as the default callback for 
messages received when another node publishes a message this client is 
subscribed to. By "default,"" we mean that this callback is called if a custom 
callback has not been registered using paho-mqtt's message_callback_add()."""

#Custom message callback: ip address
def on_message_from_ping(client, userdata, message):
   num = int(message.payload.decode())
   num = num+1
   print("Custom callback  - integer +1 : "+f"{num}")
   newNum = num
   client.publish("nayelide/pong", newNum)
   print("new integer +1:"+f"{newNum}")  


if __name__ == '__main__':
    
    #create a client object
    client = mqtt.Client()
    #attach a default callback which we defined above for incoming mqtt messages
    #client.on_message = on_message
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python. For example:
    
    `client.connect("eclipse.usc.edu", 11000, 60)` 
    
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""    
    client.connect(host="68.181.32.115", port=11000, keepalive=60)

    """In our prior labs, we did not use multiple threads per se. Instead, we
    wrote clients and servers all in separate *processes*. However, every 
    program with networking involved generally requires multiple threads to
    make coding simpler. Using MQTT is no different. If you are doing nothing 
    in this thread, you can run 
    
    `client.loop_forever()`
    
    which will block forever. This function processes network traffic (socket 
    programming is used under the hood), dispatches callbacks, and handles 
    reconnecting."""
    client.loop_forever()