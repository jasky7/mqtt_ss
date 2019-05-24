import paho.mqtt.client as mqtt

global temperatura,altitudine,pressione,luce

def on_connect(client, userdata, flags, rc):
	print('Connessione al server Calvino...: {}'.format(mqtt.connack_string(rc)))
	client.subscribe('/#', qos = 0)

def on_subscribe(client, userdata, mid, granted_qos):
	print('Avviato con QoS: {}'.format(granted_qos[0]))

def on_message(client, userdata, msg):
    global temperatura, altitudine, pressione, luce, firstRun, i
    if firstRun==True:
        i=0
        temperatura =[]
        altitudine=[]
        pressione=[]
        luce=[]
        firstRun=False
    if msg.topic == "/calvino-05/temperatura":
        temperatura.append(float(msg.payload.decode()))
        i += 1
    elif msg.topic == "/calvino-05/altitudine":
        altitudine.append(float(msg.payload.decode()))
        i += 1
    elif msg.topic == "/calvino-05/pressione":
        pressione.append(float(msg.payload.decode()))
        i += 1
    elif msg.topic == "/calvino-05/luce":
        luce.append(float(msg.payload.decode()))
        i += 1
    if i == 250:
        print('reset variabili avvenuto')
        firstRun=True

def mqttStart():
	client = mqtt.Client(protocol = mqtt.MQTTv311)
	client.on_connect = on_connect
	client.on_subscribe = on_subscribe
	client.on_message = on_message
	client.username_pw_set("calvino00","0123456789")

	client.connect(host = 'broker.shiftr.io', port = 1883, keepalive = 60)

	try:
		client.loop_forever()
	except KeyboardInterrupt:
		print()


if __name__ == '__main__':
	mqttStart()