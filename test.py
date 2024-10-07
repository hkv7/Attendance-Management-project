from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))#Code for th voice message to be heard.Dispatch function performs the action based on the type of object being passed
    speak.Speak(str1)
video=cv2.VideoCapture(0) # opens the built in web camera and video is a camera object
facedetect=cv2.CascadeClassifier('Data/haarcascade_frontalface_default.xml')
with open('data/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)
print('Shape of Faces matrix --> ', FACES.shape)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES,LABELS)
imgBackground=cv2.imread("bg for attendance1 (1).png")
COL_NAMES = ['NAME', 'TIME']#This creates the attendance file if it does not exists
while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :]
        resized_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
        output = knn.predict(resized_img)
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")#gets the date(in the format dd-mm-yy)
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")#gets the time (in the format hour-minute-seconds)
        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")#Checking if the attedance file already exists or not in attedance folder
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
        attendance = [str(output[0]), str(timestamp)]
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)
    k=cv2.waitKey(1)
    if k==ord('o'):
        speak("Attendance Taken..")
        time.sleep(0.5)#Freezes the frame for 2 seconds
        if exist :
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
              writer = csv.writer(csvfile)
              writer.writerow(attendance)
        else :
            with open("Attendance/Attendance_" + date + ".csv" ,"+a") as csvfile:
                writer = csv.writer(csvfile)#creating an object to call the writer method to write content into csv file
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()

