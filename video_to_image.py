import cv2
import os
#train
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
    left = int((dim[1]-dim[0])/2)
    right = int((dim[1]-dim[0])/2 + dim[0])
    while success:
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        image = image[:, left:right]
        image = cv2.resize(image, (224, 224))
        if count%40 == 0:
            cv2.imwrite("test/"+video+"/frame%d.jpg" % int(count/40), image)     # save frame as JPEG file      
        elif count%10 == 0:
            cv2.imwrite("train/"+video+"/frame%d.jpg" % int(count/10), image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1