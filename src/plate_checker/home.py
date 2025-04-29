import PySimpleGUI as sg
from plate_checker.sign_ups.validation_page import validate_input
from plate_checker.sign_ups._2FA_auth import  send_code_via_email
import cv2 as cv
from PIL import Image
import io
from plate_checker.sign_ups.sign_in import login
import cv2
import imutils
import numpy as np
#from number_plate_scan import number_plate
import easyocr
from plate_checker.apis.dvsa_api import api
from plate_checker.text_processing.stolen_check import stolen
from plate_checker.apis.power_check import find_power
from alerts import alert
import pytesseract
from pytesseract import Output
from PIL import Image
import cv2
from plate_checker.text_processing.text_to_speach import tts
from plate_checker.text_processing.correction import retry
from plate_checker.text_processing.correction import format_correct



def convert_to_uppercase_no_spaces(text):
    # Remove spaces from the text
    text = text.replace(' ', '')
    # Convert the text to uppercase
    text = text.upper()
    return text


def home():
    reader = easyocr.Reader(['en'], gpu=True)
    resultlist=[] 
    user_id = login()  # Execute login function
    font = ('@Yu Gothic UI Semibold', 10)  # Define font style
    sg.theme('DarkAmber')  # Set PySimpleGUI theme
    sg.set_options(font=font)  # Set font options for PySimpleGUI elements
    count=1
    # Define the layout of the window
    col_layout=[
        [sg.Button('❌', font=('@Yu Gothic UI Semibold', 25), pad=((355,0),(0,55)), button_color=(sg.theme_text_color(),sg.theme_background_color()), border_width=0)],
        #[sg.Text('', pad=((0,0),(50,0)))],
        [sg.Text('', pad=((23,0),(0,0))),sg.Frame(
            '',
            [
                [sg.Text('Last three scanned plates: ', font=("@Yu Gothic", 16), pad=((33,33),(5,5)), border_width=3)]
            ],
            border_width=3
        )],
        [sg.Text('', pad=((23,0),(0,0))),sg.Frame(
            '',
            [
                [sg.Text('xxxxxxxx', font=("@Yu Gothic", 18), pad=((120,120),(0,0)),key='1')]
            ],
            border_width=3
        )],

        [sg.Text('', pad=((23,0),(0,0))), sg.Frame(
            '',
            [
                [sg.Text('xxxxxxxx', font=("@Yu Gothic", 18), pad=((120,120),(0,0)), key='2')]
            ],
            border_width=3
        )],

        [sg.Text('', pad=((23,0),(0,0))),sg.Frame(
            '',
            [
                [sg.Text('xxxxxxxx', font=("@Yu Gothic", 18), pad=((120,120),(0,0)), key='3')]
            ],
            border_width=3
        )],
        [sg.Text('', pad=((23,0),(0,0))), sg.Text('', pad=((23,0),(0,0))),sg.Text('', pad=((0,0),(20,0)))],
        [sg.Text('', pad=((23,0),(0,0))),sg.Frame(
            '',
            [
                [sg.Text('Most recent scan:', font=("@Yu Gothic", 15), pad=((10,0),(0,0)), key='-recent_model-')]
            ],
            border_width=3
        )],

        [sg.Text('', pad=((23,0),(0,0))),sg.Frame(
            '',
            [
                [sg.Text('No scans yet', font=("@Yu Gothic", 14), pad=((30,30),(50,50)), key='-recent_info-')]
            ],
            border_width=3
        )],
        [sg.Text('', pad=((23,0),(0,0))),sg.Text('', pad=((0,0),(0,10)))],
        
        [sg.Text('', pad=((23,0),(0,0))),sg.Frame(
            '',
            [
                [sg.Text('Red alerts:', font=("@Yu Gothic", 20), text_color='dark red', pad=((10,11),(0,0)))]
            ],
            border_width=3
        )],

        [sg.Text('', pad=((23,0),(0,0))),sg.Frame(
            '',
            [
                [sg.Text('No red alerts yet', font=("@Yu Gothic", 18), pad=((50,50),(50,70)), text_color='dark red', key='-red-')]
            ],
            border_width=3
        )],
        [sg.Text('', pad=((23,0),(0,0))),sg.Text('', pad=((0,0),(0,10)))],
    ]
    
    layout = [  
        [sg.Frame(
            '',
            [
                [sg.Image(filename='',  key='image', pad=((35,35),(35,35)))]
            ],
            border_width=3
        ),
        sg.Column(col_layout, element_justification='left')],
        [sg.Text('', pad=((0,0),(800,800)))],        
    ]
    
    # Create window
    window = sg.Window('Sign_up', layout, no_titlebar=True, size=(1000,600), font=font).Finalize()
    window.maximize()  # Maximize window
    
    cap = cv2.VideoCapture(0)
    
    while True:
        button, values = window.read(timeout=1)
        
        # Exit loop if exit button is pressed
        if button == '❌':
            break
        
        imgbytes=main_loop(window, cap, reader,user_id, count)
 
        
        window['image'].Update(data=(imgbytes))
    
def main_loop(window, cap, reader, user_id, count):
       # Main loop
        
        
        # Read the frame
        
        resultlist=[]
        
        # Read frame
        ret, frame = cap.read()
        frame_for_crop= frame
        frame =cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Adjust contrast   
        factor = (259 * (1.5 + 255)) / (255 * (259 - 10))
        grey = cv2.addWeighted(grey, factor, np.zeros(grey.shape, grey.dtype), 0, 10)

        # Thresholding and inverting colors
        image = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
        image = cv2.bitwise_not(image)

        # Find contours
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:20]

        screenCnt = None
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            area = cv2.contourArea(c)
            
            # Filter contours based on area, vertices, aspect ratio, and angles
            if 0 < area < 2000 and len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                angles = []
                for i in range(4):
                    pt1 = approx[i][0]
                    pt2 = approx[(i + 1) % 4][0]
                    pt3 = approx[(i + 2) % 4][0]
                    v1 = pt1 - pt2
                    v2 = pt3 - pt2
                    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                    angles.append(np.degrees(angle))
                if 3 < aspect_ratio < 5 and all(abs(90 - angle) < 20 for angle in angles):
                    screenCnt = approx
                    break

        if screenCnt is not None:
            
            
            # Extract license plate region
            (x, y, w, h) = cv2.boundingRect(screenCnt)
            if y >20 and x>20 :
                cropped = frame_for_crop[y:y+h, x:x+w]
                grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cropped = cv2.resize(cropped, (400, 130))
                cv2.imshow('Cropped', cropped)
                cv2.drawContours(frame, [screenCnt], -1, (0, 0, 255), 3)
            
                result = reader.readtext(cropped,detail=5, paragraph=False, adjust_contrast=1)
                
                if not result  == []:
                    print(result)
                    text = result[0][1]
                    print(text)
                    result= convert_to_uppercase_no_spaces(text)
                    
                    if not result in resultlist:
                        resultlist.append(result)
                        if len(resultlist)>1000:
                            resultlist=[]
                        print(result)
                        
                        api_data, api_code = api(str(result))
                        if api_code == 400:
                            if not result in resultlist:
                                resultlist.append(result)
                        if len(resultlist)>1000:
                            resultlist=[]
                        print(result)
                        
                        api_data, api_code = api(str(result))
                        if api_code == 400:
                            print(result)
                            result=format_correct(result)
                            api_data, api_code=api(result)
                            if api_code == 400:
                                    for i in range(6):
                                            print(result)
                                            if not result == None:    
                                                result=retry(result, i)
                                                if result == 'break':
                                                    break
                                                api_data, api_code=api(result)
                                                if api_code == 200:
                                                    print(10101010)
                                                    break
                        if api_code ==200:
                        
                            
                            make, model, power, max_torque, zero_to_60 = find_power(result)
                            window['-recent_model-'].Update(f"Most recent model: {make} {model}")
                            window['-recent_info-'].Update(f"""The horse power is {power} 
and it has {max_torque}. 
The acceleration is {zero_to_60}
from 0-60 time.""")
                            window.refresh()
                            tts(f"Most recent model: {make} {model}")
                            tts(f"The horse power is {power} and it has {max_torque}. The acceleration is {zero_to_60} from 0-60.")
                            confirmed_reg = api_data['registrationNumber']
                            if count ==1:
                            
                                window['1'].Update(confirmed_reg)
                                count+=1
                            elif count ==2:
                                window['2'].Update(confirmed_reg)
                                count+=1
                            elif count ==3:
                                window['2'].Update(confirmed_reg)
                                count=1
                            
                           
                            if api_data['taxStatus'] =='Untaxed':
                                alert('Green alert', 'Vehicle is untaxed', 'Save', user_id )
                                pass
                            if api_data['motStatus'] == 'Invalid':
                                alert('Amber alert', 'Invalid mot', 'Save location',user_id)
                                pass
                            if stolen(result):
                                window['-red-'].Update('This car may be stolen. Please take action')
                                
                                alert('Red alert', 'Vehcile may be stolen.', 'Save location', user_id)
                                pass
                            
        #cv2.imshow('frame', frame)
       
        img= cv2.resize(frame, None, fx=1.6,fy=1.55, interpolation= cv2.INTER_NEAREST)
        img = Image.fromarray(img)
        bio = io.BytesIO()  
        img.save(bio, format= 'PNG')  
        imgbytes = bio.getvalue()
        return imgbytes
            
                # Convert frame to PIL image

