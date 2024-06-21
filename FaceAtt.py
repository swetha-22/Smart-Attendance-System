import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
import pyttsx3


password="CVRCE"
# from PIL import ImageGrab
path = 'C:/Users/DELL/Desktop/20_6233/Training_Images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)        



def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)         
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')


def markAttendance(name):
    t=dt.now()
    d = t.strftime('%d/%m/%Y %H:%M:%S')
    i=0
    f = open("C:/Users/DELL/Desktop/20_6233/att1.csv","r")
    myDataList = f.readlines()
    nameList = []
    for line in myDataList:
        entry = line.split(',')
        print(entry)
        nameList.append(entry[0])
        #print(nameList)
        f.close()
        if name in nameList:
               
            now = int(entry[4])+1
            if(now%2!=0):
                entry[2]=d
                
            elif(now==2):
                t2=dt.strptime(entry[2], "%d/%m/%Y %H:%M:%S")
                t0 =t-t2
                #entry[3]= t0.strftime("%H:%M:%S")
                entry[3]= str(t0)
                    
                
            else :
                t2=dt.strptime(entry[2], "%d/%m/%Y %H:%M:%S")
                t0 =t-t2
                print('entry[3]:',entry[3])
                x=entry[3].split(".")[0]
                #b=x.split(" ")
                #z=b[1]
                print("mark attendence t_time :",x)
                t3=dt.strptime(x,"%H:%M:%S")
                y=t3+t0
                entry[3] = y.strftime("%H:%M:%S")
            t=analysis(name)
            if(t<50):
                engine.say(f"{name} your attendance is less than 50 please attend regularly")
                engine.runAndWait()
                
                
            now = str(now)
            x=entry[9].replace('\n','')
            myDataList[i]=(',').join([entry[0],entry[1],entry[2],entry[3],now,entry[5],entry[6],entry[7],entry[8],x,"\n"])
            f = open("C:/Users/DELL/Desktop/20_6233/att1.csv","w")
            f.writelines(myDataList)
            f.close()
            t2=dt.strptime(d, "%d/%m/%Y %H:%M:%S")
            break
        i+=1

        
        
def time_Calc(w):
    f = open("C:/Users/DELL/Desktop/20_6233/att1.csv","r")
    myDataList = f.readlines()
    i=0
    for line in myDataList:
        if(i==0):
            entry = line.split(',')
            v=entry[w+4].split('-')[1]
            v=int(v)+1
            entry[4+w]='week'+str(w)+'-'+str(v)
            myDataList[i]=(',').join([entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6],entry[7],entry[8],entry[9]])
        else:
            entry = line.split(',')
            x=entry[3].split(".")[0]
            #b=x.split(" ")
            #z=b[0]
            t=dt.strptime(x,"%H:%M:%S")
            if t > dt.strptime('00:00:10',"%H:%M:%S"):
                now = int(entry[1])+1
                now=str(now)
                x=entry[9].replace('\n','')
                v=int(entry[w+4])+1
                v=str(v)
                li=list(entry[w+4])
                li.pop()
                li.append(v)
                v=str(li[0])
                entry[w+4]=v
                myDataList[i]=(',').join([entry[0],now,entry[2],entry[3],entry[4],entry[5],entry[6],entry[7],entry[8],x,"\n"])

            x=entry[9].replace('\n','')
            int_x = int(x)+1
            x=str(int_x)
            t_time=dt.strptime(entry[3],"%H:%M:%S")
            tym = dt.strptime(entry[2],"%d/%m/%Y %H:%M:%S")
            d1 = t_time.replace(hour = 0,minute = 0,second = 0)
            d1 = d1.strftime("%H:%M:%S")
            d2 = tym.replace(day = 1,month =1, year =2021,hour = 0,minute = 0,second = 0)
            d2 = d2.strftime("%d/%m/%Y %H:%M:%S")
            myDataList[i]=(',').join([entry[0],entry[1],d2,d1,entry[4],entry[5],entry[6],entry[7],entry[8],x,"\n"])
        i+=1

    f.close()
    f = open("C:/Users/DELL/Desktop/20_6233/att1.csv","w")
    f.writelines(myDataList)
    f.close()

    

def analysis(name):
    f = open("C:/Users/DELL/Desktop/20_6233/att1.csv","r")
    myDataList = f.readlines()
    nameList = []
    for line in myDataList:
        entry = line.split(',')
        nameList.append(entry[0])
        f.close()
        if name in nameList:
            att=int(entry[1])
            m=entry[9].replace('\n','')
            work_day=int(m)
            per=att/work_day*100
            return per
        
            
            
            
def weekAnalysis(name):
    f = open("C:/Users/DELL/Desktop/20_6233/att1.csv","r")
    myDataList = f.readlines()
    i=0
    nameList = []
    Tw=[] #total number of days in week in a month
    Sw=[] #total number of days Student is present in week in a month
    for line in myDataList:
        entry = line.split(',')
        print(entry)
        nameList.append(entry[0])
        if(i==0):
            for w in range(1,5):
                entry = line.split(',')
                v=entry[w+4].split('-')[1]
                v = int(v)
                Tw.append(v)
        i +=1
        if name in nameList:
            for w in range(1,5):
                Sw.append(int(entry[4+w]))
            break
    per = analysis(name)
    print("ATTENDANCE PERCENTAGE :",round(per,2)," %")
    Tw = np.array(Tw)
    Sw = np.array(Sw)
    x = ['week 1','week 2','week 3','week 4']
    X_axis = np.arange(len(x))
    plt.bar(X_axis - 0.2,Tw,0.4,label = 'Total',color ='blue')
    plt.bar(X_axis + 0.2,Sw,0.4,label = 'Present',color ='orange')
    plt.xticks(X_axis,x)
    plt.title(f'WEEKLY ANALYSIS OF {name}')
    plt.ylabel('NO. OF DAYS')
    plt.xlabel('WEEK NUMBER')
    plt.legend()
    plt.show()



def MonEdit():
    f = open("C:/Users/DELL/Desktop/20_6233/att1.csv","r")
    myDataList = f.readlines()
    i=0
    for line in myDataList:
        entry = line.split(',')
        if(i==0):
            for w in range(1,5):
                entry[4+w]='week'+str(w)+'-0'
                myDataList[i]=(',').join([entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6],entry[7],entry[8],entry[9]])
        else:
            myDataList[i]=(',').join([entry[0],entry[1],entry[2],entry[3],entry[4],'0','0','0','0',entry[9]])
        i += 1
    f.close()
    f = open("C:/Users/DELL/Desktop/20_6233/att1.csv","w")
    f.writelines(myDataList)
    f.close()
            

        

        
def main(p):
    success, img = cap.read()
    
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
# print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img,name,(x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            print(name)
            engine.setProperty("voice",'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
            engine.say(f"{name} you are captured")
            engine.runAndWait()
            return name
        else:
            return "XXX"
            #markAttendance(name)
        

engine = pyttsx3.init()
engine.setProperty('rate',150)



#OBJECT TO USE WEBCAM CAPTURING METHOD
cap = cv2.VideoCapture(0)
i=0
while(i==0): 
    pwd=input("enter password :")
    if(pwd==password):
        engine.say("SYSTEM IS ON")
        engine.runAndWait()
        print(" 1 : same month   2 : new month")
        month=int(input("Enter month position: "))
        if(month == 2):
            MonEdit()
        w=int(input("Enter week:"))
        cap = cv2.VideoCapture(0)
        i=i+1
#INFINTE LOOP FOR CAPTURING AND NECESSITIES
        while True:
            #CHOICES FOR PERSON
            p=int(input("Enter\n1:Take Attendance\t2:Check your Analysis\t3:Off  : "))
            if(p==1): #method for time recording and counting how many times captured
                name = main(p)
                #cv2.imshow('webcam',img)
                markAttendance(name)
                
            elif(p==2):#method to show the analysis of the person
                name = main(p)
                weekAnalysis(name)
                
            elif(p==3):# reseting of total day's data and making it ready for next day
                pwd=input("Enter Password :")
                if(pwd==password):
                    engine.say("SYSTEM IS OFF")
                    engine.runAndWait()
                    cap.release()
                    time_Calc(w)
                    engine.setProperty("voice",'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
                    engine.say("Attendance updated")
                    engine.runAndWait()
                    break
                    
                else:
                    engine.say("Incorrect password , try again")
                    engine.runAndWait()
            cv2.waitKey(1)
    else:
        engine.say("Incorrect password , try again")
        engine.runAndWait()
    
