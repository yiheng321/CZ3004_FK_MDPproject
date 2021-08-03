# import requests
# url = 'http://10.193.49.112:8000/stream.mjpg'
# r = requests.get(url,stream=True)
#
# print(r.headers.get('content-type'))
# print(r.content)
# # with open('facebook.mjpg', 'wb') as f:
# #     print(r.content)
# #     f.write(r.content)
#
#
import cv2
import warnings
import keras_cnn_test as kera_detect
import time
warnings.filterwarnings('ignore')
global  capture
# global WAIT_TIME
import socket
import time
PORT = 1234
IP = '192.168.7.176'
HEADERSIZE = 10


Labels = {0: ['six',6],
          1: ['seven',7],
          2: ['eight',8],
          3: ['nine',9],
          4: ['zero',10],
          5: ['v',11],
          6: ['w',12],
          7: ['x',13],
          8: ['y',14],
          9:  ['z',15],
          10:['left',4],
          11: ['right',3],
          12: ['up',1],
          13: ['down',2],
          14: ['circ',5],
          15: ['bull',16]
          }



def start_detect(wait_time):
    wait_time =+ 1
    global WAIT_TIME
    WAIT_TIME = wait_time
    print("WAIT_TIME ", WAIT_TIME)
    if wait_time >=30:
        capture = True




def camera ():
    cap = cv2.VideoCapture("http://192.168.7.176:8000/stream.mjpg")
    Img_count =0
    count =0
    capture = False
    resultlist=[]
    shots =5
    WAIT_TIME_start = 0
    WAIT_TIME_end = 10

    while (count <=shots ):
        Img_count = Img_count + 1
        ret, img = cap.read()
        #img=cv2.resize(frame,(640,480))
        cv2.imshow('video', img)


        # kera_detect.detection_kera(img)


        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('t'):
            capture = True
        list_result =[]

        print("WAIT_TIME ", WAIT_TIME_start)
        WAIT_TIME_start += 1
        if WAIT_TIME_start >= WAIT_TIME_end:
            capture = True

        if capture == True and Img_count %3 ==0:
            print( f"cnt/CAPTURE_{count}")
            # time.sleep(0.01)
            cv2.imshow(f"cnt/CAPTURE_{count}", img)
            cv2.imwrite(f"cnt/CAPTURE_{count}.jpg", img)
            result = kera_detect.detection_kera(img)
            if result == 'NONE':
                shots  =+ 1
            else:
                resultlist.append(result)
            time.sleep(0.01)
            count += 1

            if count >=shots:
                capture = False
                count = 0
                print ("resultlist ", resultlist)
                item = max(resultlist,key=resultlist.count)
                print ("ITEM IS: ", item)
                return  item

result = camera()
sent_to_pi.sent(result[1])

# def sent_detection(msg):
#
#     # msg sender
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((IP, PORT))
#     s.listen(5)
#
#     while True:
#         # now our endpoint knows about the OTHER endpoint.
#         clientsocket, address = s.accept()
#         print(f"Connection from {address} has been established.")
#
#         # msg = "Welcome to the server!"
#         # msg = f"{len(msg):<{HEADERSIZE}}" + msg
#
#         clientsocket.send(bytes(msg, "utf-8"))
#
#         while True:
#             time.sleep(3)
#             msg = f"The time is {time.time()}"
#             msg = f"{len(msg):<{HEADERSIZE}}" + msg
#
#             print(msg)
