from multiprocessing import Process, Queue
from time import sleep
from AppletComms import AppletComm
import os
from datetime import datetime


def connect(commsList):
    for comms in commsList:
        comms.connect()

def disconnect(commsList):
    for comms in commsList:
        comms.disconnect()

def listen(msgQueue, com):
    while True:
        msg = com.read()
        msgQueue.put(msg)

def sent(message):
    ap = AppletComm()
    ap.connect()
    ap.write(message)

def listening():
    ## Initialisation - RPi Comms
    commsList = []
    #commsList.append(AndroidComm())
    commsList.append(AppletComm())
    connect(commsList)

    #ANDROID = 1
    APPLET = 0

    msgQueue = Queue()
    #androidListener = Process(target=listen, args=(msgQueue, commsList[ANDROID]))
    appletListener = Process(target=listen, args=(msgQueue, commsList[APPLET]))

    #androidListener.start()
    appletListener.start()
    ## Initialise variables
    running = True
    exploring = False

    try:
        while running:
            message = msgQueue.get()

            if message == None:
                continue
            msgSplit = message.split(';')  # Try without semi-colon
            print ('message ',message)
            print ("msgSplit " , msgSplit)
            com = message
            ## W, A, D: From Android or Applet
            if com == 'W':
                # Move forward
                print ("ahha")
            elif com == 'A':
                # Turn left
                print ("ahha")

            elif com == 'Q':
                # Turn right

                print ("ahha")
                commsList[APPLET].disconnect()
                break

    except Exception as e:
        print("[MAIN_ERROR] Error. Prepare to shutdown...")



if __name__ == '__main__':
    ## Set up message logs
    run_timestamp = datetime.now().isoformat()
    os.makedirs('logs', exist_ok=True)

#     while True:
#         sent("hjaahah")

    sleep(1)
    listening()

