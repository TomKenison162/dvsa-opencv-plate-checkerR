import cv2
import numpy as np
import imutils
from PIL import Image
import io
import easyocr
from test import api
# Open the video capture device


def convert_to_uppercase_no_spaces(text):
    # Remove spaces from the text
    text = text.replace(' ', '')
    # Convert the text to uppercase
    text = text.upper()
    return text
cap = cv2.VideoCapture(0)
reader = easyocr.Reader(['en'])
while True:
    # Read the frame
    ret, frame = cap.read()
    
    # Resize the frame
    #frame = cv2.resize(frame, None, fx=1.6, fy=1.55, interpolation=cv2.INTER_NEAREST)
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filter for noise reduction
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 
    cv2.imshow('car1', gray)
    # Detect edges
    edged = cv2.Canny(gray, 30, 200)
    
    # Find contours
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    screenCnt = None

    for c in contours:
        max_angle_deviation = 20 
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
            if 1 < aspect_ratio < 1.5:
                screenCnt = approx
                break

    if screenCnt is not None:
        cv2.drawContours(frame, [screenCnt], -1, (0, 0, 255), 3)
        
        # Extract license plate region
        (x, y, w, h) = cv2.boundingRect(screenCnt)
        Cropped = gray[y:y+h, x:x+w]
        Cropped = cv2.resize(Cropped, (400, 200))
        cv2.imshow('Cropped', Cropped)
        result = reader.readtext(Cropped)
        if not result  == []:
            print(result)
            text = result[0][1]
            print(text)
            result= convert_to_uppercase_no_spaces(text)
            print(result)
            api(result)
        
        
    # Resize frame for display
    frame = cv2.resize(frame, (500, 300))

    # Display the frame
    cv2.imshow('car', frame)
    
    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    img= cv2.resize(frame, None, fx=1.6,fy=1.55, interpolation= cv2.INTER_NEAREST)
    img = Image.fromarray(img)
    bio = io.BytesIO()  
    img.save(bio, format= 'PNG')  
    imgbytes = bio.getvalue()  
    
