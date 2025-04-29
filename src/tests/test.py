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


import cv2 
#import imutils
import numpy as np
from PIL import Image
import io
import easyocr

import time as t
import cv2
import numpy as np




def number_plate1():

    cap = cv2.VideoCapture(0)
    reader = easyocr.Reader(['en'])
    while True:

        ret,frame = cap.read()
        # Load the image
        

        # Convert the image to grayscale
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #min_val = np.min(gray)
        #max_val = np.max(gray)
        #print(min_val)
        # Perform contrast stretching
        
        #streched = cv2.convertScaleAbs(frame, alpha=1, beta=-10)

        # Apply a Gaussian blur to reduce noise 
        #blurred = cv2.GaussianBlur(frame, (5, 5), 0)

        # Use Hough transform to detect rectangles
        edges = cv2.Canny(frame, 70, 100, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, 3.14 / 180, threshold=180, minLineLength=70, maxLineGap=3)

        # If there are lines detected
        if lines is not None:
            # Initialize variables for the bounding rectangle
            x_min = min(min(line[0][0], line[0][2]) for line in lines)
            y_min = min(min(line[0][1], line[0][3]) for line in lines)
            x_max = max(max(line[0][0], line[0][2]) for line in lines)
            y_max = max(max(line[0][1], line[0][3]) for line in lines)
            
            # Crop the image based on the rectangle coordinates
            cropped_image = frame[y_min:y_max, x_min:x_max]
            height, width, channels = cropped_image.shape
            

            if height >30 and width >30:
                # Crop the image based on the rectangle coordinates
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                #x, y, w, h = cv2.boundingRect(lines)
                #cropped_image = frame[y:y+h, x:x+w]
                
                
                # Save or display the cropped image
                #cv2.imwrite('cropped_image.jpg', cropped_image)
                #t.sleep(10)
                cv2.imshow('Cropped Image', cropped_image)
                
                result = reader.readtext(cropped_image)
                print(result)
            
        else:
            print("No rectangle detected in the image.")
        cv2.imshow('Cropped Image 2', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break






def number_plate12():
    cap = cv2.VideoCapture(0)
    reader = easyocr.Reader(['en'])
    while True:
        # Capture frame-by-frame
        ret,frame = cap.read()
        
        # Convert frame to grayscale
        
# Convert the image to grayscale
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur with larger kernel size
        #blurred_image = cv2.GaussianBlur(gray_image, (1, 1), 100)
        #cv2.imshow('License Plate Detection1', blurred_image)
        # Apply Canny edge detection with adjusted thresholds
       
       # edges = cv2.Canny(gray_image, 30, 80)
       # adaptive_thresholded_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 1.7)
        cv2.imshow('License Plate Detectio2n', gray_image)
        # Find contours
        edges = cv2.Canny(gray_image, 10, 80)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

        # Filter contours based on area and aspect ratio
        license_plate_candidates = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            area = cv2.contourArea(contour)
            if aspect_ratio >3 and  aspect_ratio <7 and area > 1200:
                license_plate_candidates.append(contour)

        # Draw bounding boxes around detected license plate candidates
        for contour in license_plate_candidates:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('License Plate Detection', frame)
        cropped_image = frame[x:x+ w, y: y+ h]
        
        result = reader.readtext(cropped_image)
        print(result)

       # reader = easyocr.Reader(['en'])
        
        # Wait for key press and exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

# Call the function

number_plate1()

    
