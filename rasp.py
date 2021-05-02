import cv2
import numpy as np
import spidev
from time import sleep

count = 0
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 152000

def write_pot(input):
    msb = input >> 8
    lsb = input & 0xFF
    spi.xfer([msb,lsb])

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    sleep(0.025)  
    ret,frame =cap.read()
    Lower = np.array([180,180,180])
    Upper = np.array([255,255,255])
    dst = cv2.inRange(frame,Lower,Upper)
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #retval,dst = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)
    dst = cv2.dilate(dst,None,iterations=2)
    dst = cv2.erode(dst,None,iterations=2)
    cv2.imshow("dst",dst)
    color = dst[460]
    try:
        white_count=np.sum(color == 255)
        white_index=np.where(color==255)
        #if count >= 50:
        if white_count == 0:
            white_count = 1
        center = (white_index[0][white_count-1]+white_index[0][0]) / 2
        if 50 < center < 250:
            write_pot(0x32)
            print(center)
        elif center > 350:
            write_pot(0x31)
            print(center)
        #elif center <= 150:
            #write_pot(0x35)
            #print(center)
        #elif center >= 450:
            #write_pot(0x34)
            #print(center)
        else:
            write_pot(0x33)
            print(center)
            #count = 0
    except:
        pass
    if cv2.waitKey(1)&0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
