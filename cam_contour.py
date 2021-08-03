import time
import keras_cnn_test
import cv2
import imutils
import numpy as np
import keras_cnn_test as kera_detect

frameWidth = 640
frameHeight = 480
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("http://192.168.5.5:8000/stream.mjpg")

cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",440,440)
cv2.createTrackbar("Threshold1","Parameters",100,255,empty)
cv2.createTrackbar("Threshold2","Parameters",60,255,empty)
cv2.createTrackbar("AreaMin","Parameters",1480,5000,empty)
cv2.createTrackbar("AreaMax","Parameters",12000,30000,empty)
cv2.createTrackbar("Point","Parameters",13,20,empty)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    counterBox=[]
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("AreaMin", "Parameters")
        areaMax = cv2.getTrackbarPos("AreaMax", "Parameters")
        Point = cv2.getTrackbarPos("Point", "Parameters")
        if area > areaMin and area < areaMax:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print(len(approx))
            if 6 < len(approx) < Point :
                x , y , w, h = cv2.boundingRect(approx)
                # print (x , y , w, h )
                cv2.rectangle(imgContour, (x-int(w/4) , y-int(h/4) ), (x + int(1.2*w) , y + int(1.2*h) ), (0, 255, 0), 5)
                # keras_cnn_test.preProcessing(im)
                # keras_cnn_test.Imgs_predictions(img)
                # cut = imgContour[x-int(w/4) :x + int(1.2*w),y-int(h/4): y + int(1.2*h)]
                # cv2.imwrite(f'cnt/cnt_{cnt}', cnt)

                cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)
                # counterBox.append ([x-int(w/4),x + int(1.2*w),y-int(h/4),int(1.2*h)])
                counterBox.append([y,y+h, x,x+w])
            #crop_img = img[y:y+h, x:x+w]
            #cut = img[x-int(w/4) :x + int(1.2*w),y-int(h/4): y + int(1.2*h)]
            #cv2.imwrite(f'cnt/cnt_{cnt}', cut)
            #cv2.imshow('video', cut)
            #kera_detect.detection_kera(cut)
    # print (counterBox)
    return counterBox
#
Img_count =0
count =0

capture = False

while True:
    Img_count = Img_count+1
    success, img = cap.read()
    # img = cv2.flip(img, 1)
    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    smooth = cv2.medianBlur(imgContour, 5)
    imgBlur = cv2.GaussianBlur(smooth, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    counterBox=[]
    counterBox = getContours(imgDil, imgContour)
    #if not counterBox :
        #print ("empty ?!",counterBox )
    #elif len(counterBox)>1:
        #     a,b,c,d=counterBox
        # if count%2 ==0:
        #print ("More counterBox !",counterBox)
        #cv2.imwrite(f"counterBox_{count} ",img[a:b,c:d])

    imgStack = stackImages(0.8,([img,imgCanny],
                                [imgDil,imgContour]))
    #cv2.imshow("Result", imgStack)
    kera_detect.detection_kera(img)
    time.sleep(0.05)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('t'):
        capture = True
    list_result =[]
    if capture == True and Img_count %5 ==0:
        print( f"cnt/CAPTURE_{count}")
        cv2.imshow(f"cnt/CAPTURE_{count}", img)
        cv2.imwrite(f"final/cnt/CAPTURE_{count}.jpg", img)
        time.sleep(0.05)

        count = count +  1
        if count >=10:
            capture = False
            count = 0


# path
# path = 'test_6.jpg'
# image = cv2.imread(path)
# image = imutils.resize(image, width=800)
# imgContour = image.copy()
# imgBlur = cv2.GaussianBlur(image, (7, 7), 1)
# imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
# threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
# threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
# imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
# kernel = np.ones((5, 5))
# imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
# getContours(imgDil,imgContour)
# imgStack = stackImages(0.8,([image,imgCanny],
#                             [imgDil,imgContour]))
# cv2.imshow("Result", imgStack)
#
# cv2.waitKey(0) # waits until a key is pressed
# cv2.destroy