import os
import numpy as np
import cv2
import screenshot




def onTrack1(val):
    global hueLow
    hueLow=val
    print('Hue Low',hueLow)
def onTrack2(val):
    global hueHigh
    hueHigh=val
    print('Hue High',hueHigh)
def onTrack3(val):
    global satLow
    satLow=val
    print('Sat Low',satLow)
def onTrack4(val):
    global satHigh
    satHigh=val
    print('Sat High',satHigh)
def onTrack5(val):
    global valLow
    valLow=val
    print('Val Low',valLow)
def onTrack6(val):
    global valHigh
    valHigh=val
    print('Val High',valHigh)


width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 60)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

cv2.namedWindow('myTracker')
cv2.moveWindow('myTracker',width,0)

hueLow=10
hueHigh=20
satLow=10
satHigh=250
valLow=10
valHigh=250

cv2.createTrackbar('Hue Low','myTracker',10,179,onTrack1)
cv2.createTrackbar('Hue High','myTracker',20,179,onTrack2)
cv2.createTrackbar('Sat Low','myTracker',10,255,onTrack3)
cv2.createTrackbar('Sat High','myTracker',250,255,onTrack4)
cv2.createTrackbar('Val Low','myTracker',10,255,onTrack5)
cv2.createTrackbar('Val High','myTracker',250,255,onTrack6)

windowId = None

while True:
    ignore,  frame = cam.read()
    if frame is None:
        while windowId is None or windowId == False:
            windowId = screenshot.findWindowId()
        frame=screenshot.takeScreenshot(windowId)
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    #myMask=cv2.bitwise_not(myMask)
    myObject=cv2.bitwise_and(frame,frame,mask=myMask)
    myObjectSmall=cv2.resize(myObject,(int(width/2),int(height/2)))
    cv2.imshow('My Object',myObjectSmall)
    cv2.moveWindow('My Object',int(width/2),int(height))
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    cv2.imshow('My Mask',myMaskSmall)
    cv2.moveWindow('My Mask',0,height)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()
