import cv2
import numpy as np
import time
#Creating a VideoCapture object
# This will be used for image acquisition later in the code.
cap = cv2.VideoCapture(0)
 

 
# We give some time for the camera to warm-up!
time.sleep(3)
count =0
background=0

for i in range(60):
    ret,background = cap.read()
 
# Laterally invert the image / flip the image.
background = np.flip(background,axis=1)



# Capturing the live frame
#ret, img = cap.read()

while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count+=1
    img = np.flip(img,axis=1)



        # Laterally invert the image / flip the image
        #img  = np.flip(img, axis=1)
         
        # converting from BGR to HSV color space
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
         
        # Range for lower red
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
         
        # Range for upper range
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)
         
        # Generating the final mask to detect red color
    mask1 = mask1+mask2
        
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
         
         
        #creating an inverted mask to segment out the cloth from the frame
    mask2 = cv2.bitwise_not(mask1)
         
         
        #Segmenting the cloth out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(img,img,mask=mask2)
        
        
        
        # creating image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(background, background, mask = mask1)
         
         
        #Generating the final output
    final_output = cv2.addWeighted(res1,1,res2,1,0)
    cv2.imshow("magic",final_output)
        
    k = cv2.waitKey(10)
    if k == 27:
       	sys.exit()
        
        