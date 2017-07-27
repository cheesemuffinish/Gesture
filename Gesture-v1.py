import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import win32api, win32con
import time

#time.sleep(5)

#Sets the cursor position to a certain point
def point(x,y):
    win32api.SetCursorPos((x,y))
    
#Finds the center of the tracking box
def average(pts):
    avg = []
    avg.append((pts[1][0]+pts[3][0])/2)
    avg.append((pts[1][1]+pts[3][1])/2)
    return(avg)

#I think this checks to see the standard deviation of tm
def check(tm):
    x = []
    y = [] 
    for item in tm:
        x.append(item[0])
        y.append(item[1])
    return [np.std(x), np.std(y)]
 
#This checks to see if the object is inside of the borders of the projected image
def checkClick(pointer, border):
    #print(border)
    #print(pointer)
    if pointer[0][1] > border[0] and pointer[0] [1] < border[1] and pointer [0][0] > border [2] and  pointer[0][0] < border[3]:
        return(1)


#Function for getting sides
def cornerCount(tot, start, val):
    i = 0
    init = np.sum(image[start][np.abs(i-val)])
    for x in range(int(tot)):
        p_array = image[start][np.abs(i-val)]
        #print(p_array)
        #if p_array[1] - p_array[0] > 20 and p_array[1] - p_array[2] > 85:
        sum = int(np.sum(p_array))
        #print(p_array)
        #print(np.sum(image[start][np.abs(i-val+1)]))
        if np.abs(init - sum) > 150:
	        i += 1
	        loc.append(np.abs(i-val))
	        break
        else:
	        i+=1
            
cap = cv2.VideoCapture(0)
cam = cv2.VideoCapture(0)
s, im = cam.read() # captures image
cv2.imshow("Test Picture", im) # displays captured image
cv2.imwrite("C:/Users/Somokai/Documents/Gesture/test.bmp",im) # writes image test.bmp to disk

#turn image into array, print array to console
image = cv2.imread("test.bmp")


#terminate the cameras

cap.release()
        
height = len(image)/2
length = len(image[0])/2

print(length)
print(height)

loc=[]

#getting four corners
cornerCount(length*2 - 1, height, 0)
cornerCount(length*2 - 1, height, length*2 - 1)
cornerCount(height*2 - 1, length, 0)
cornerCount(height*2 - 1, length, height*2 - 1)

cap = cv2.VideoCapture(0)
# take first frame of the video
ret,frame = cap.read()
# setup initial location of window
r,h,c,w = 100,100,100,100  # simply hardcoded the values
track_window1 = (c,r,w,h)
r,h,c,w = 100,150,150,100 
track_window2 = (c,r,w,h)
# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((110., 30., 30.)), np.array((130.,200.,200.)))
#mask2 = cv2.inRange(hsv_roi, np.array((110., 50.,50.)), np.array((130.,255.,255.)))

#this is finding the box for tracking, I don't like the way it works though so it needs fixed
roi_hist1 = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
roi_hist2 = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist1,roi_hist1,0,255,cv2.NORM_MINMAX)
cv2.normalize(roi_hist2,roi_hist2,0,255,cv2.NORM_MINMAX)
#print(roi_hist)
# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
j = 0
tm = [] 
tmi = 0
timp = 0
timi = lambda:int(round(time.time()*1000))
timei = timi()
while(1):
    ret ,frame = cap.read()    
    pts_tot = [[0,0],[0,0],[0,0],[0,0]]
    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst1 = cv2.calcBackProject([hsv],[0],roi_hist1,[0,180],1)
        dst2 = cv2.calcBackProject([hsv],[0],roi_hist2,[0,180],1)
        #Apply meanshift to get the new location
        ret1, track_window1 = cv2.CamShift(dst1, track_window1, term_crit)
        ret2, track_window2 = cv2.CamShift(dst2, track_window2, term_crit)
        # Draw it on image
        pts1 = cv2.boxPoints(ret1)
        pts1 = np.int0(pts1)
        
        pts2 = cv2.boxPoints(ret2)
        pts2 = np.int0(pts2)
        
        #print(pts2)
        
        if j == 2:
            avg1 = average(pts1*3)
            tm.append(avg1)
            avg2 = average(pts2*3)
            tm.append(avg2)
            if avg1[0]!=0:
                if 1 == 1: 
                    print(timei)
                    print(timp)
                    deltat = timei-timp
                    #print(np.abs(np.sum(avg1) - np.sum(avg2)))
                    print(deltat)
                    if np.abs(np.sum(avg1) - np.sum(avg2)) <125 and deltat > 2:
                        print('click')
                        chk = check(tm)
                        print(chk)
                        timp = timei
                        timei = timi()
                        x = int(chk[0])
                        y = int(chk[1])
                        #clicks the mouse
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
                        if chk[0] < 6 and chk[1] < 6:
                            tm.pop()
                else: 
                    point(320, 240)
            j = 0
            #print(avg)
            point(int(avg1[0]),int(avg1[1]))
            point(int(avg2[0]),int(avg2[1]))
            tmi += 1
        else:
            #print(j)
            pts_tot += pts2
            j  += 1
       
        
       
        img2 = cv2.polylines(frame,[pts1],True, 255,2)
        img3 = cv2.polylines(frame,[pts2],True, 255,2)
        cv2.imshow('img2',img2)
        cv2.imshow('img3',img3)
        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg",img2)
    else:
        break
cv2.destroyAllWindows()
cap.release()