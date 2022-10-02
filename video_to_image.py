import cv2
import os

face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

videos = ['Confused','Engaged','Not_interested','Thinking']
os.mkdir("test")
os.mkdir("train")
for video in videos:
    os.mkdir("test/"+video)
    os.mkdir("train/"+video)
    vidcap = cv2.VideoCapture( video + '.mov')
    success,image = vidcap.read()
    count = 0
    dim  = image.shape
    
    while success:
        if count%10==0:
            get_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            faces_detected = face_haar_cascade.detectMultiScale(get_image, 1.32, 5)
            for (x, y, w, h) in faces_detected:
                image = roi_gray = image[y:y + w, x:x + h] 
                try:
                    image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
                    image = cv2.resize(image, (224, 224))
                    if count%40 == 0:
                        cv2.imwrite("test/"+video+"/frame%d.jpg" % int(count/40), image)     # save frame as JPEG file      
                    elif count%10 == 0:
                        cv2.imwrite("train/"+video+"/frame%d.jpg" % int(count/10), image)     # save frame as JPEG file   
                except:
                    pass   
        success,image = vidcap.read()
        count += 1

for video in videos:
    vidcap = cv2.VideoCapture( video + '.mp4')
    success,image = vidcap.read()
    count = 0
    dim  = image.shape
    
    while success:
        if count%10==0:
            get_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            faces_detected = face_haar_cascade.detectMultiScale(get_image, 1.32, 5)
            for (x, y, w, h) in faces_detected:
                image = roi_gray = image[y:y + w, x:x + h] 
                try:
                    image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
                    image = cv2.resize(image, (224, 224))
                    if count%40 == 0:
                        cv2.imwrite("test/"+video+"/frame%d-2.jpg" % int(count/40), image)     # save frame as JPEG file      
                    elif count%10 == 0:
                        cv2.imwrite("train/"+video+"/frame%d-2.jpg" % int(count/10), image)     # save frame as JPEG file   
                except:
                    pass   
        success,image = vidcap.read()
        count += 1