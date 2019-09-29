'''
Copyright: Zachary Lloyd (LloydApps) 9/28/19
Rachel v0.01
Known Bugs:
    Low performance on object recognition

Future Changes:
    Custom TF model for obj. detection -- most likely based on Microsoft COCO dataset
    Move inline running code to a Flask server to offload from raspberry pi
    Migrate to Raspberry Pi Zero

TODO:
    Implement Phone BT Functionality
        This needs a mobile counterpart.... Enlist someone?
    Lower Cam Quality
    Upgrade Wolfram API
    Accept user input for funtion choice

Future Features:
    Uber navigation through API
    Lyft navigation through API
    Walking/Driving directions
    Implement voice assisitant:
        Possibilities:
            Google Assistant
            Alexa
            Mine:
                Frank
                Bill
                Sydney
'''

import cv2 as cv
import numpy as np
import wolframalpha, cvlib

def searchQuery(query): #Query Wolfrom Alpha (a search engine) with the tag of the image
    wolfclient = wolframalpha.Client("VTHAHP-AQRU7QT7XY") #Wolfram API ID
    res = wolfclient.query(query) #Variable for the query
    return next(res.results).text #Return a text-response of the result with the tag 'Result'

def getObject(img): #Object Detection
    bbox, label, conf = cvlib.detect_common_objects(img) #Run the default TF model for object recognition
    output_image = draw_bbox(img, bbox, label, conf) #Create an output showing the changes
    plt.imshow(output_image) #Show the output
    plt.show() #Display the output

def run(): #Main function
    cam = cv.VideoCapture(0) #Capture output from the webcam (will likely need to changed for RPI)
    count = 0 #Amount of times loop has run since 0 start
    while True: #Runs in a  continuous loop ............ True will be removed for a var based on user input
        count += 1 #Loop has run once
        ret_val, img = cam.read() #Read the webcam
        img = cv.flip(img, 1) #Flip the image :)
        # cv.imshow('my webcam', img) #Show the image
        try: #In case it errors I don't want the program shutting down
            if(count == 15): #If the loop has run 15 times (15 frames... roughly)
                getObject(img) #Run object detection
                count = 0 #Reset count
            else: #If count != 15
                pass
            try:
                result = searchQuery(query) #string result will be set to the wolfram response
            except:
                result = "Could not connect to Wolfram! Retrying..." #Error msg
        except: 
            "Error with camera! Retrying..." #Error msg

        if cv.waitKey(1) == 27: #Quit the program.... THIS IS TEMPORARY
            break  # esc to quit
    cv.destroyAllWindows()


if name == "__main__":
    run()