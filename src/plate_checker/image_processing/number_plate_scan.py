
import cv2
import numpy as np
import imutils
from PIL import Image
import io
import easyocr
from plate_checker.apis.dvsa_api import api
from plate_checker.text_processing.stolen_check import stolen

# Open the video capture device

resultlist=[]
def convert_to_uppercase_no_spaces(text):
    # Remove spaces from the text
    text = text.replace(' ', '')
    # Convert the text to uppercase
    text = text.upper()
    return text



def number_plate():
    resultlist=[]
    cap = cv2.VideoCapture(0)
    
    reader = easyocr.Reader(['en'])
    while True:
        # Read the frame
        ret, frame = cap.read()
        
        # Convert frame to grayscale
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter for noise reduction
        grey = cv2.bilateralFilter(grey, 13, 15, 15) 
        
        # Detect edges
        edged = cv2.Canny(grey, 30, 200)

        #cv2.imshow('car1', grey)
        
        # Find contours
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        
        screenCnt = None

        for c in contours:
            max_angle_deviation = 40
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            if cv2.contourArea(c) > 500:
                if len(approx) == 4:
                    angles = []
                    for i in range(4):
                        pt1 = approx[i][0]
                        pt2 = approx[(i + 1) % 4][0]
                        pt3 = approx[(i + 2) % 4][0]
                        v1 = pt1 - pt2
                        v2 = pt3 - pt2
                        angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                        angles.append(np.degrees(angle))
                
                # Check if all angles are approximately 90 degrees
                    if all(abs(90 - angle) < max_angle_deviation for angle in angles):
                        # If all conditions are met, consider this contour as the car
                        screenCnt = approx
                        break
                    
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 1 < aspect_ratio < 3:
                    screenCnt = approx
                    break

        if screenCnt is not None:
            cv2.drawContours(frame, [screenCnt], -1, (0, 0, 255), 3)
            
            # Extract license plate region
            (x, y, w, h) = cv2.boundingRect(screenCnt)
            cropped = grey[y:y+h, x:x+w]
            cropped = cv2.resize(cropped, (400, 200))
            #cv2.imshow('Cropped', cropped)
            result = reader.readtext(cropped)
            if not result  == []:
                print(result)
                text = result[0][1]
                print(text)
                result= convert_to_uppercase_no_spaces(text)
                
                if not result in resultlist:
                    resultlist.append(result)
                    if len(resultlist)>30:
                        resultlist=[]
                    print(result)
                    api_data, api_code = api(result)
                    if api_code ==200:
                        stolen(result)

            
            
        

        # Display the frame
        cv2.imshow('car', frame)
        
        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            
        #img= cv2.resize(frame, None, fx=1.6,fy=1.55, interpolation= cv2.INTER_NEAREST)
        #img = Image.fromarray(img)
        #bio = io.BytesIO()  
        #img.save(bio, format= 'PNG')  
        #imgbytes = bio.getvalue()   
            return frame

        
number_plate()
