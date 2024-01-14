import datetime
from tkinter import font
import face_recognition
import cv2
import numpy as np
import csv

from datetime import datetime

Video_Capture = cv2.VideoCapture(0)

# load known faces

sudhanshu_image =face_recognition.load_image_file("faces/sudhanshu.jpg")
sudhanshu_encoding = face_recognition.face_encodings(sudhanshu_image)[0]

deepak_image =face_recognition.load_image_file("faces/deepak.jpg")
deepak_encoding = face_recognition.face_encodings(deepak_image)[0]

mitthu_image =face_recognition.load_image_file("faces/mitthu.jpg")
mitthu_encoding = face_recognition.face_encodings(mitthu_image)[0]

known_face_encodings = [sudhanshu_encoding, deepak_encoding, mitthu_encoding]
known_face_names =["sudhanshu","Deepak","Mitthu"]

#list of expected students
students = known_face_names.copy()

face_locations =[]
known_face_encodings=[]

# Get the current date and time 
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(f"{current_date}.csv", "w+" , newline ="")
lnwriter = csv.writer(f)

while True:
    _, frame = Video_Capture.read()
    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)

    # recognize faces
    face_locations= face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index=np.argmin(face_distance)

        if(matches[best_match_index]):
            name = known_face_encodings[best_match_index]

            # Add the text of a person is present 
            if name in known_face_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 1.5
                fontColor =(255, 0, 0)
                thickness = 3
                LineType = 2
                cv2.putText_(frame,name +" Present ", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, LineType)

        if name in students:
            students.remove(name)
            current_time = now.strftime("%Y-%M-%D,%H-%M-%S")
            lnwriter.writerow([name, current_time])

        cv2.imshow("Attendence", frame)
        if cv2.waitkey(1) &  0xFF == ord("q"):
            break

    Video_Capture.release() 
    cv2.destroyAllWindows() 
    f.close()          


