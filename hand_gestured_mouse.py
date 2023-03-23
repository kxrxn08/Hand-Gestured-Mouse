import threading
import time
import cvzone.HandTrackingModule as HD
import cv2
import matplotlib
import mouse
import numpy as np
import pyautogui

def l_clk_delay():
    global l_delay
    global l_clk_thread
    time.sleep(0.5)
    l_delay=0
    l_clk_thread=threading.Thread(target=l_clk_delay)
def r_clk_delay():
    global r_delay
    global r_clk_thread
    time.sleep(0.5)
    r_delay=0
    r_clk_thread=threading.Thread(target=r_clk_delay)
def d_clk_delay():
    global d_delay,d_clk_thread
    time.sleep(0.5)
    d_delay=0
    d_clk_thread=threading.Thread(target=d_clk_delay)
r_delay=0
r_clk_thread=threading.Thread(target=r_clk_delay)
d_delay=0
d_clk_thread=threading.Thread(target=d_clk_delay)
matplotlib.use('TkAgg')

detector=HD.HandDetector(detectionCon=0.9,maxHands=2)

cap = cv2.VideoCapture(0)
cam_h=640
cam_w=480
cap.set(3, cam_w)
cap.set(4, cam_h)
frameR=100
l_delay=0
l_clk_thread = threading.Thread(target=l_clk_delay)
# Loop over frames
while True:
    success, img = cap.read()
    img=cv2.flip(img, 1)
    hands,img=detector.findHands(img, flipType=False)
    cv2.rectangle(img,(frameR,frameR),(cam_h-frameR,cam_w-frameR),(255,0,255),2)
    if hands:
        lmlist=hands[0]['lmList']
        ind_x,ind_y=lmlist[8][0], lmlist[8][1]
        mid_x,mid_y=lmlist[12][0], lmlist[12][1]
        thumb_x,thumb_y=lmlist[4][0],lmlist[4][1]
        cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 255), 2)
        cv2.circle(img, (thumb_x, thumb_y), 5, (0, 255, 255), 2)    
        fingers=detector.fingersUp(hands[0])

        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 1:
            conv_x = int(np.interp(ind_x, (frameR, cam_h - frameR), (0, 1366)))
            conv_y = int(np.interp(ind_y, (frameR, cam_w - frameR), (0, 768)))
            mouse.move(conv_x, conv_y)


        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1 and fingers[3]==0:

            if abs(ind_x-mid_x) < 25:

                if fingers[4]==0 and l_delay==0:
                    pyautogui.click(button="left")
                    l_delay=1
                    l_clk_thread.start()
        
                if fingers[4]==1 and r_delay==0:
                    pyautogui.click(button="right")
                    r_delay=1
                    r_clk_thread.start()


        if fingers[1]==1 and fingers[2]==1 and fingers[0]==0 and fingers[4]==0:
            if abs(ind_x-mid_x)<25:
                pyautogui.scroll(-1)


        if fingers[1]==1 and fingers[2]==1 and fingers[0]==0 and fingers[4]==1:
            if abs(ind_x-mid_x)<25:
                pyautogui.scroll(1)


        if fingers[1]==1 and fingers[2]==1 and fingers[3]==1:
            if abs(ind_x-mid_x)<15:
                pyautogui.mouseDown()
                conv_x = int(np.interp(ind_x, (frameR, cam_h - frameR), (0, 1366)))
                conv_y = int(np.interp(ind_y, (frameR, cam_w - frameR), (0, 768)))
                mouse.move(conv_x, conv_y)
        
            
        if fingers[1]==1 and fingers[0]==0:
            if d_delay==0:
                pyautogui.doubleClick(button="left")

                d_delay=1
                d_clk_thread.start()
    if not success:
        break   


    cv2.imshow("live-feed", img)


    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()