import pzgram
import request
import urllib

bot = pzgram.Bot("893309177:AAHTL0ODM-2k-8KFN3kM1u46KdYZbFoMGWs"")


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
    chat.send(str(round(sum(altitudine)/len(altitudine),2))+ " Metri")

def LaunchBot():
    bot.set_query({"temperatura": sendTemperatura, "pressione": sendPressione,"luce": sendLuce, "altitudine": sendAltitudine})
    bot.set_commands({"stats": SetBot})
    bot.run()
