import cv2
import numpy as np
import imutils
def adjust_contrast_and_brightness(cap, contrast=1.5, brightness=0):
    # Set the width and height of the video stream
    width = 640
    height = 480

    # Set the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Adjust the contrast and brightness
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        gray = cv2.addWeighted(gray, factor, np.zeros(gray.shape, gray.dtype), 0, brightness)

        # Write the modified frame
        out.write(gray)
        image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

    # Invert the colors
        image = cv2.bitwise_not(image)
        # Display the resulting frame
        cv2.imshow('Grayscale Video', image)
        #edged = cv2.Canny(gray, 30, 50)
        #cv2.imshow('Cropped', edged)
        #cv2.imshow('car1', grey)
        
        # Find contours
        contours = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:20]
        
        screenCnt = None

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            area = cv2.contourArea(c)
            
            # Filter contours based on area
            if area < 0 or area > 2000:
                continue
            
            # Filter contours based on number of vertices (approximation)
            if len(approx) != 4:
                continue
            
            # Calculate aspect ratio and filter contours based on it
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if aspect_ratio < 3 or aspect_ratio > 5:
                continue
            
            # Calculate angles and filter contours based on angle deviation
            angles = []
            for i in range(4):
                pt1 = approx[i][0]
                pt2 = approx[(i + 1) % 4][0]
                pt3 = approx[(i + 2) % 4][0]
                v1 = pt1 - pt2
                v2 = pt3 - pt2
                angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                angles.append(np.degrees(angle))
            
            # Filter contours based on angle deviation
            if not all(abs(90 - angle) < 20 for angle in angles):
                continue
            
        
            screenCnt = approx
            break
            
                    
                        

        if screenCnt is not None:
            
            
            # Extract license plate region
            (x, y, w, h) = cv2.boundingRect(screenCnt)
            if y >20 and x>20 :
                cropped = frame[y:y+h, x:x+w]
                grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cropped = cv2.resize(cropped, (400, 130))
                cv2.imshow('Cropped', cropped)
                cv2.drawContours(frame, [screenCnt], -1, (0, 0, 255), 3)
                cv2.imshow('Cropped1', frame)
            
        # Exit the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Open the webcam
cap = cv2.VideoCapture(0)

# Set the width and height of the video stream
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Call the function
adjust_contrast_and_brightness(cap, contrast=1.5, brightness=10)