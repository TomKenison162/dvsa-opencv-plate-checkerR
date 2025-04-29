import PySimpleGUI as sg
import random as r
from plate_checker.text_processing.text_to_speach import tts
from plate_checker.text_processing.location_services import find_location
from database_con_or_clos import alert_log
from database_con_or_clos import update_location
def alert(alert_level, reason, locate_or_save, user_id):
    
    # Assign colors and time intervals based on alert level
    if alert_level == 'Green alert':
        colour = '#36B22B'
        
        
        tick1, tick2 = 17, 19
    elif alert_level == 'Amber alert':
        alert_log(0, 1, 0, reason, '', user_id)
        colour = '#D0931E'
        
        tick1, tick2 = 7, 11
    elif alert_level == 'Red alert':
        colour = '#B22B3B' 
        alert_log(0, 0, 1, reason, '', user_id)
        
        tick1, tick2 = 2, 1
        
    count = 0

    

    # Define fonts
    font = ('@Yu Gothic UI Semibold', 10)
    button_font = ('@Yu Gothic', 12, 'underline')
    button_font2 = ('@Yu Gothic', 20)

   

    

    # Set the theme and default font options
    sg.theme('DarkAmber')
    sg.set_options(font=font)

    # Define the layout of the window
    layout = [  
        [sg.Button('❌', font=('@Yu Gothic UI Semibold', 20), pad=((905,30),(30,0)), button_color=('white', sg.theme_background_color()), border_width=0 )],  # Exit button
        
        [sg.Frame(
            '', layout=[
                    [sg.Frame('', layout=[
                    
                    [sg.Text(alert_level, font=("@Yu Gothic", 30), pad=((50,0),(20,20)), text_color = colour, key='1'), sg.Text('', font=("@Yu Gothic", 30), pad=((0, 55),(20,20)), text_color = 'white', key='2')],
                            ] 
                ,border_width=0, element_justification='center',pad=((2,2),(2,2)))]] # Inner frame with content
            , border_width=0, background_color=colour,element_justification='center')
    
                                            ],
        [sg.Frame(
            '', layout=[
                    [sg.Frame('', layout=[
                    
                    [sg.Text(reason, font=button_font2, pad=((20,600),(10,120)),text_color = 'white')],
                            ] 
                ,border_width=0, element_justification='center', pad=((2,2),(2,2)))]] # Inner frame with content
            , border_width=0, background_color=colour,element_justification='center',pad=((0,0),(50,50)))
                                            ],
        [sg.Frame(
            '', layout=[
                    [sg.Frame('', layout=[
                    
                    [sg.Button(locate_or_save, font=button_font, pad=((0,0),(0,0)), button_color=('white', sg.theme_background_color()), border_width=0)],
                            ] 
                ,border_width=0, background_color=colour, element_justification='center', pad=((2,2),(2,2)))]] 
             , border_width=0, background_color=colour,element_justification='center',pad=((0,0),(50,50)))
                ],# Inner frame with content
    ]

    # Create the Window
    window = sg.Window('Sign_up', layout, no_titlebar=True, size=(1000,600),font=font, element_justification='c')
    
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        
        # Process events and update the window
        event, values = window.read(timeout=50)

        # Handle events

        # Check for different events and handle them accordingly
        if event == '❌':
            return  # If the event is '❌', break out of the loop or function
            
        if count % tick1 == 0:
            window['1'].Update(alert_level)
            window['2'].Update('')
        elif count % tick2 == 0:
            window['1'].Update('')
            window['2'].Update(alert_level)
        count += 1
        
        if count == 5:
            # Text to speech for alert level and reason
            tts(alert_level)
            tts(reason)
        
        if locate_or_save == 'Save':
            alert_log(0, 1, 0, reason, '', user_id)
            
            
        elif event == 'Save location':
            # If the user clicks 'Save location', get the location using location_services module and speak it
            cords, location1, location2, location3 = find_location()
            print(location1, location2, location3)
            location_info=str(cords) + str(location1) + str(location2) + str(location3)
            update_location(user_id, location_info)

            tts('Your current location is: ')
            tts(location1)
            tts(location2)
            tts(location3)


#alert('Red alert', 'Vehicle is stolen.', 'Save location', 12)