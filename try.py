from multiprocessing import Process, Queue

import stream_video as sv
import time


global  capture

dect_on = sv.camera()
sv.sent_detection(dect_on[1])


print("capture = True , detection get  " ,dect_on )
