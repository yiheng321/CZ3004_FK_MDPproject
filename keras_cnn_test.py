import time

import numpy as np
import cv2
from keras.models import load_model

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

Labels = {0: 'six',
          1: 'seven',
          2: 'eight',
          3: 'nine',
          4: 'zero',
          5: 'v',
          6: 'w',
          7: 'x',
          8: 'y',
          9:  'z',
          10:'left',
          11: 'right',
          12: 'up',
          13: 'down',
          14: 'circ',
          15: 'bull',

          }


########### PARAMETERS ##############
width = 640
height = 480
threshold = 0.90 # MINIMUM PROBABILITY TO CLASSIFY
cameraNo = 0
#####################################

#### CREATE CAMERA OBJECT
cap = cv2.VideoCapture(cameraNo)
cap.set(3,width)
cap.set(4,height)

#### LOAD THE TRAINNED MODEL
model = load_model("model_kera_3ch_80_labdata")
# pickle_in = open("model_trained","rb")
# model = pickle.load(pickle_in)

def Imgs_predictions(img):


    classIndex = Labels [int(model.predict_classes(img))]
    i = int(model.predict_classes(img))
    #print(classIndex)
    predictions = model.predict(img)
    #print(predictions)
    probVal= np.amax(predictions)
    # if probVal > 0.98:
    #     print( 'PRIDICTION : ', classIndex,'  Probability: ',probVal)

    return probVal ,classIndex,i


#### PREPORCESSING FUNCTION
def preProcessing(img):


    img = np.asarray(img)
    # print ( )

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = img / 255
    img = cv2.resize(img, (80, 80))
    # cv2.imshow("Processsed Image",img)
    img = img.reshape(1,80,80,1)
    return img


import cv2
import warnings
warnings.filterwarnings('ignore')

# cap = cv2.VideoCapture("http://10.193.49.112:8000/stream.mjpg")

# while True:
#
#     ret, frame = cap.read()
#     cv2.imshow('video', frame)
#
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:  # press 'ESC' to quit
#         break


def detection_kera(imgOriginal):
    img = np.asarray(imgOriginal)
    # print ( )
    time.sleep(0.1)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.equalizeHist(img)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # img = img / 255

    cols, rows,  nslice = img.shape
    print ( rows, cols,nslice)
    #time.sleep(0.1)

    # Img_cent = img[int(rows / 3):int(2 * rows / 3), int(cols / 3):int(2 * cols / 3)]
    first_tenth = int(rows / 10)
    last_tenth = int(rows*0.9)
    one_third = int(rows/3)
    two_third = int(rows/3*2)
    print (first_tenth, two_third,'  ', one_third,last_tenth)
    Img_cent_L = img[20 : int(cols / 8*7),first_tenth:two_third+2*first_tenth]
    Img_cent_R = img[20 : int(cols / 8*7),one_third-2*first_tenth:last_tenth]

    # cv2.imshow("CL Image", Img_cent_L)
    # cv2.imshow("CR Image", Img_cent_R)

    img_CL = preProcessing(Img_cent_L)
    img_CR = preProcessing(Img_cent_R)
    probVal_L, classIndex_L ,i_L= Imgs_predictions(img_CL)

    probVal_R, classIndex_R ,i_R= Imgs_predictions(img_CR)

    if probVal_L> threshold:
        cv2.putText(Img_cent_L,str(classIndex_L) + "   "+str(probVal_L),
                    (10,30),cv2.FONT_HERSHEY_COMPLEX,
                    1,(0,0,255),1)
        print('Img_cent_L : ', str(classIndex_L), i_L, ' probVal_L is ', probVal_L)

    if probVal_R> threshold:
        cv2.putText(Img_cent_R,str(classIndex_R) + "   "+str(probVal_R),
                    (10,280),cv2.FONT_HERSHEY_COMPLEX,
                    1,(0,255,25),1)
        print('Img_cent_R : ', str(classIndex_R),i_R, ' probVal_R is ', probVal_R)

    cv2.rectangle(imgOriginal, (first_tenth,20), (two_third+2*first_tenth,int(cols / 5*4)), (250,5,5), 2)
    cv2.rectangle(imgOriginal, (one_third-2*first_tenth,20), (last_tenth,int(cols / 5*4)), (10,10,250), 2)
    cv2.imshow("Original Image",imgOriginal)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyWindow()
    if probVal_L > threshold and probVal_R > threshold:
        if str(classIndex_L) == str (classIndex_R):

            result= [str(classIndex_L) , i_L]
        else:
            result = [str(classIndex_L),i_L] if probVal_L < probVal_R else [str(classIndex_R),i_R]
    else:
        result ='NONE'
    return (result)




def get_size(img):
    cols, rows,  nslice = img.shape
    print ( rows, cols,nslice)
    #time.sleep(0.1)

    # Img_cent = img[int(rows / 3):int(2 * rows / 3), int(cols / 3):int(2 * cols / 3)]
    first_tenth = int(rows / 10)
    last_tenth = int(rows*0.9)
    one_third = int(rows/3)
    two_third = int(rows/3*2)



## original detection function
# while True:
#
#     #if frame == None:
#     #success, imgOriginal = cap.read()
#     #else:
#     #    success,imgOrigin al=frame
#     success, imgOriginal = cap.read()
#
#
#     # BB = extract.extractBoundingBox (imgOriginal)
#     # cv2.imshow("extract", img)
#     # print (BB)
#     # imgOriginal= cv2.flip(imgOriginal,1)
#     # cv2.imshow("frame", imgOriginal)
#     img = np.asarray(imgOriginal)
#     # print ( )
#
#     # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # img = cv2.equalizeHist(img)
#     # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     # img = img / 255
#
#     cols, rows,  nslice = img.shape
#     print ( rows, cols,nslice)
#     #time.sleep(0.1)
#
#     # Img_cent = img[int(rows / 3):int(2 * rows / 3), int(cols / 3):int(2 * cols / 3)]
#     first_tenth = int(rows / 10)
#     last_tenth = int(rows*0.9)
#     one_third = int(rows/3)
#     two_third = int(rows/3*2)
#     print (first_tenth, two_third,'  ', one_third,last_tenth)
#     Img_cent_L = img[50 : int(cols / 5*4),first_tenth:two_third+2*first_tenth]
#     Img_cent_R = img[50 : int(cols / 5*4),one_third-2*first_tenth:last_tenth]
#
#
#     # Img_topL = img[ 50: int(2*rows / 3), 20: int(2* cols / 3)]
#     # # Img_top = img[80: int( 2* rows / 3), int(cols / 3):int(2 * cols / 3)]
#     # Img_topR = img[50: int( 2* rows / 3), int( cols / 3): cols-20]
#
#     #cv2.imshow("Original Imagesuccess,", imgOriginal)
#
#     # cv2.imshow("centralImg Image", Img_cent)
#     # cv2.imshow("CT Image", Img_top)
#     cv2.imshow("CL Image", Img_cent_L)
#     cv2.imshow("CR Image", Img_cent_R)
#     # cv2.imshow("TL Image", Img_topL)
#     # cv2.imshow("TR Image", Img_topR)
#
#     # img = preProcessing(img)
#     img_CL = preProcessing(Img_cent_L)
#     img_CR = preProcessing(Img_cent_R)
#     # img_cent = preProcessing(Img_cent_R)
#     # img_topL = preProcessing(Img_topL)
#     # # img_top = preProcessing(Img_top)
#     # img_topR = preProcessing(Img_topR)
#
#
#     #### PREDICT
#     # classIndex = Labels [int(model.predict_classes(img_CL))]
#     # classIndex = Labels [int(model.predict_classes(img_cent))]
#     # time.sleep(0.1)
#     # classIndex = Labels [int(model.predict_classes(img_CR))]
#     # classIndex = Labels [int(model.predict_classes(img_topL))]
#     # time.sleep(0.1)
#     # classIndex = Labels [int(model.predict_classes(img_top))]
#     # classIndex = Labels [int(model.predict_classes(img_topR))]
#
#     probVal_L,classIndex_L = Imgs_predictions(img_CL)
#     time.sleep(0.05)
#     probVal_R,classIndex_R = Imgs_predictions(img_CR)
#
#     # Imgs_predictions(img_CR)
#     # time.sleep(0.05)
#     # Imgs_predictions(img_cent)
#     # time.sleep(0.2)
#     # Imgs_predictions(img_top)
#     # time.sleep(0.1)
#     # Imgs_predictions(img)
#     # Imgs_predictions(img_topR)
#     # time.sleep(0.1)
#     # Imgs_predictions(img_topL)
#
#
#
#     # #print(classIndex)
#     # predictions = model.predict(img)
#     # #print(predictions)
#     # probVal= np.amax(predictions)
#     # print( classIndex,probVal)
#     #
#     if probVal_L> threshold:
#         cv2.putText(Img_cent_L,str(classIndex_L) + "   "+str(probVal_L),
#                     (50,50),cv2.FONT_HERSHEY_COMPLEX,
#                     1,(0,0,255),1)
#         # cv2.rectangle()
#     if probVal_R> threshold:
#         cv2.putText(Img_cent_R,str(classIndex_R) + "   "+str(probVal_R),
#                     (50,50),cv2.FONT_HERSHEY_COMPLEX,
#                     1,(0,0,255),1)
#
#
#     cv2.imshow("Original Image",imgOriginal)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
#
