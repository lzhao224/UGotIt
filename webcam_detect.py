# camera and image processing code: https://github.com/dhruvpandey662/Emotion-detection

import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
import warnings
warnings.filterwarnings("ignore")
from tensorflow.keras.utils import img_to_array, load_img
from keras.models import  load_model
import matplotlib.pyplot as plt
import numpy as np

# load model
model = load_model("my_model1.h5") #change to our model
background = cv2.imread('background.png')



face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)

while True:
    ret, test_img = cap.read()  # captures frame and returns boolean value and captured image
    if not ret:
        continue
    gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

    emotions_cnt = {'Confused':0, 'Engaged':0, 'Not_interested':0, 'Thinking':0}
    total_score = 0
    for (x, y, w, h) in faces_detected:
        cv2.rectangle(test_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
        roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
        roi_gray = cv2.resize(roi_gray, (224, 224))
        img_pixels = image.img_to_array(roi_gray)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels /= 255

        predictions = model.predict(img_pixels)

        # find max indexed array
        max_index = np.argmax(predictions[0])

        emotions = ('Confused', 'Engaged', 'Not_interested', 'Thinking')
        predicted_emotion = emotions[max_index]
        emotions_cnt[predicted_emotion] += 1
        cv2.putText(test_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    resized_img = cv2.resize(test_img, (1000, 700))

    numFaces = len(faces_detected)

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,665)
    fontScale              = 0.7
    fontColor              = (30,255,255)
    thickness              = 2
    lineType               = 2

    cv2.putText(resized_img,'Student Count: '+str(numFaces)+ " Not Interested: "+str(emotions_cnt['Not_interested']) +" Confused: "+str(emotions_cnt['Confused']) + " Thinking: "+str(emotions_cnt['Thinking']) + " Engaged: "+str(emotions_cnt['Engaged']), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        thickness,
        lineType)
    cv2.imshow('Facial emotion analysis ', resized_img)


    xpos = 20
    stats = cv2.resize(background, (300, 200))
    cv2.putText(stats,'Student Count: '+str(numFaces), 
        (xpos, 30), 
        font, 
        0.7,
        (0, 0, 0),
        2,
        1)

    cv2.putText(stats,'Engaged: '+str(emotions_cnt['Engaged']), 
        (xpos, 60), 
        font, 
        0.7,
        (100, emotions_cnt['Engaged']/(numFaces if numFaces else 1)*255, 255-emotions_cnt['Engaged']/(numFaces if numFaces else 1)*255),
        2,
        1)

    cv2.putText(stats,'Thinking: '+str(emotions_cnt['Thinking']), 
        (xpos, 90), 
        font, 
        0.7,
        (100, emotions_cnt['Thinking']/(numFaces if numFaces else 1)*255, 255-emotions_cnt['Thinking']/(numFaces if numFaces else 1)*255),
        2,
        1)

    cv2.putText(stats,'Confused: '+str(emotions_cnt['Confused']), 
        (xpos, 120), 
        font, 
        0.7,
        (100, 255-emotions_cnt['Confused']/(numFaces if numFaces else 1)*255, emotions_cnt['Confused']/(numFaces if numFaces else 1)*255),
        2,
        1)

    cv2.putText(stats,'Not Interested: '+str(emotions_cnt['Not_interested']), 
        (xpos, 150), 
        font, 
        0.7,
        (100, 255-emotions_cnt['Not_interested']/(numFaces if numFaces else 1)*255, emotions_cnt['Not_interested']/(numFaces if numFaces else 1)*255),
        2,
        1)
    cv2.imshow('Engagement Stats', stats)

    if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
        break

cap.release()
cv2.destroyAllWindows
