import pzgram
import paho.mqtt.client as mqtt
import threading

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


def SetBot(chat):
    button1 = pzgram.create_button("Temperatura", data="temperatura")
    button2 = pzgram.create_button("Pressione", data="pressione")
    button3 = pzgram.create_button("Luce", data="luce")
    button4 = pzgram.create_button("Altitudine", data="altitudine")

    k = [[button1, button2,button3,button4]]

    keyboard = pzgram.create_inline(k)

    chat.send("Bot per il controllo remoto dei dati dei sensori della scuola Calvino: ")
    chat.send("Seleziona un dato da controllare: ", reply_markup=keyboard)


def sendTemperatura(chat):
    chat.send(str(round(sum(temperatura)/len(temperatura),2))+" °C")

def sendPressione(chat):
    chat.send(str(round(sum(pressione)/len(pressione),2))+" Pa")

def sendLuce(chat):
    chat.send(str(round(sum(luce)/len(luce),2))+" Lux")

def sendAltitudine(chat):
    chat.send(str(round(sum(altitudine) / len(altitudine), 2)) + " Metri")


def LaunchBot():
    bot.set_query(
        {"temperatura": sendTemperatura, "pressione": sendPressione, "luce": sendLuce, "altitudine": sendAltitudine})
    bot.set_commands({"stats": SetBot})
    bot.run()


if __name__ == '__main__':
    bot = pzgram.Bot("893309177:AAHTL0ODM-2k-8KFN3kM1u46KdYZbFoMGWs")
    firstRun = True
    mqttThread = threading.Thread(target=mqttStart)
    mqttThread.setDaemon(True)
    mqttThread.start()
    botThread = threading.Thread(target=LaunchBot)
    botThread.start()
