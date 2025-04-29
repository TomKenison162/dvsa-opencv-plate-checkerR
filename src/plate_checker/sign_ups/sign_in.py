import PySimpleGUI as sg
import random as r
from sign_ups.validation_page import validate_input
from sign_ups._2FA_auth import  send_code_via_email
from db.database_con_or_clos import sign_up_log
from db.database_con_or_clos import login_check

def sign_up1():
   
    # Define fonts
    font = ('@Yu Gothic UI Semibold', 10)
    Font = (('@Yu Gothic', 40, 'underline'))
    button_font=('@Yu Gothic', 12, 'underline')
    # Get a list of installed fonts
    fontlist = []
    for i in sg.Text.fonts_installed_list():
        fontlist.append(i)

    # Set the theme and default font options
    sg.theme('DarkAmber')
    sg.set_options(font=font)

    # Define the layout of the window
    layout = [  
        [sg.Button('❌', font=('@Yu Gothic UI Semibold', 20), pad=((905,30),(30,0)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0 )],  # Exit button
        [sg.Text('Sign up', font=Font, pad=((30,70),(0,50)), key='-text-', size=(0, 1))],

        [sg.Text('Username generation: ', font=("@Yu Gothic", 18), pad=((70,0),(0,20))), sg.InputText(background_color=sg.theme_background_color(), border_width=0)],

        [sg.Text('First name: ', font=("@Yu Gothic", 12), pad=((100,0),(25,25))), sg.InputText(background_color=sg.theme_background_color(), border_width=0),
         sg.Text('', font=("@Yu Gothic", 9), pad=((10,0),(25,25)),  key='-first-')],

        [sg.Text('VIN chassis no: ', font=('@Yu Gothic', 12), pad=((100,0),(25,25))), sg.InputText(background_color=sg.theme_background_color(), border_width=0),
          sg.Text('', font=("@Yu Gothic", 9), pad=((10,0),(25,25)),  key='-vin-')],
        
        [sg.Text('Your user name will be: ', font=("@Yu Gothic", 18), pad=((70,70),(25,20)), key='-user-')],

        [sg.Button('Next.', font=button_font, pad=((885,30),(10,20)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0)]
    ]

    # Create the Window
    window = sg.Window('Sign_up', layout, no_titlebar=True, size=(1000,600), font=font)
    #j = 0

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        #if j > 300:
            #j = 0
        #j += 4

        # Process events and update the window
        event, values = window.read(timeout=10)
        if values[1] != '':
            state, message = validate_input(values[1], 10, False, str, False)
            if state:
                # If validation is successful, clear the message
                message = ''
            window['-first-'].update(message)

        # Update Vin  input field 
            
            
                
            if values[2].isnumeric() and len(values[2]) ==17:
                message=''
            elif not values[2].isnumeric():
                message='Vin must be a number'
            elif len(values[2]) !=17:  
                message='Vin must be 17 characters long'
            
                    
            window['-vin-'].update(message) 

            

    # Check for 'Next.' event and return concatenated values
        if event == 'Next.':
            if window['-vin-'].Get() == '' and window['-first-'].Get() == '':
                sign_up2(values[1], values[2])
                # If Vin, first name fields are empty, return concatenated values
                return str(values[1]) + str(values[2])
            
        
        
        # Handle events
        if event == '❌':
            login()
            break
        elif values[1] != '':
            text = 'Your user name will be: ' + str(values[1]) + str(values[2])
            window['-user-'].update(text)
            
# Call the function to run the GUI

def sign_up2(first_name, VIN):
    



    code=None 
    # Define fonts
    font = ('@Yu Gothic UI Semibold', 10)
    Font = (('@Yu Gothic', 40, 'underline'))
    button_font=('@Yu Gothic', 12, 'underline')
    # Get a list of installed fonts
    fontlist = []
    for i in sg.Text.fonts_installed_list():
        fontlist.append(i)

    # Set the theme and default font options
    sg.theme('DarkAmber')
    sg.set_options(font=font)

    # Define the layout of the window
    layout = [  
        [sg.Button('❌', font=('@Yu Gothic UI Semibold', 20), pad=((905,30),(30,0)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0 )],  # Exit button
        [sg.Text('Sign up', font=Font, pad=((30,70),(0,50)), key='-text-', size=(0, 1))], 
        [sg.Text('Password generation and 2FA: ', font=("@Yu Gothic", 18), pad=((70,0),(0,20))), sg.InputText(background_color=sg.theme_background_color(), border_width=0)],
        
        [sg.Text('Desired password: ', font=("@Yu Gothic", 12), pad=((100,0),(25,25))), sg.InputText(background_color=sg.theme_background_color(), border_width=0),
        

        sg.Text('', font=("@Yu Gothic", 9), pad=((10,0),(25,25)),  key='-pass-')],
        
        [sg.Text('Email address: ', font=('@Yu Gothic', 12), pad=((100,0),(5,5))), sg.InputText(background_color=sg.theme_background_color(), border_width=0),
       
         sg.Button('2FA.', font=button_font, pad=((20,30),(10,20)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0)],
        [sg.Text('', font=("@Yu Gothic", 9), pad=((100,0),(0,0)), key='-email-')],
        
        [sg.Text('Code: ', font=('@Yu Gothic', 12), pad=((100,0),(25,25))), sg.InputText(background_color=sg.theme_background_color(), border_width=0),
         sg.Text('', font=("@Yu Gothic", 9), pad=((10,0),(0,0)), key='-code-'),
         ],
        
        [sg.Button('Back.', font=button_font, pad=((20,30),(10,20)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0),
         sg.Button('Finish.', font=button_font, pad=((785,30),(10,20)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0)]
    ]

    # Create the Window
    window = sg.Window('Sign_up', layout, no_titlebar=True, size=(1000,600),font=font)
    

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        

        # Process events and update the window
        event, values = window.read(timeout=100)

        pass_attempt, email_attempt, code_attempt =values[1], values[2], values[3]
        
        # Handle events

        
        # Check for different events and handle them accordingly
        if event == '❌':
            # If the event is '❌', break out of the loop or function
            login()
            break
        elif event == 'Back.':
            # If the event is 'Back.', call the sign_up1() function and break
            sign_up1()
            break

        # Validate and update password input field
        if values[1] != '':
            state, message = validate_input(values[1], 20, False, int, True)
            if state:
                # If validation is successful, clear the message
                message = ''
            window['-pass-'].update(message)

        # Validate and update email input field
        if values[2] != '':
            state, message = validate_input(values[2], 35, True, int, False)
            if state:
                # If validation is successful, clear the message
                message = ''
                if event == '2FA.':
                    code = r.randint(111111, 999999)
                    send_code_via_email(values[2],code)
                    
            window['-email-'].update(message)
            

        # Update code input field 
        if values[3] != '':
            if values[3].isnumeric():  
                if int(code_attempt) != int(code):  
                    message='Incorrect code'
                else:
                    message=''
            else:
                message='Must be a number'
            window['-code-'].update(message) 

        # Check for 'Finish.' event and return concatenated values
            if event == 'Finish.':
                if window['-pass-'].Get() == '' and window['-email-'].Get() == '' and window['-code-'].Get() == '':
                    # If password, email, and code fields are empty, return concatenated values
                    username= first_name + VIN
                    sign_up_log(values[2], values[1], username, VIN, first_name)
                    return str(values[1]) + str(values[2])

        # Check for '2FA.' event and generate a random code
        
            
            # Uncomment the line below to send the generated code via 2FA_code_send() function
            # 2FA_code_send()
import PySimpleGUI as sg
import random as r




def login():

    code=None 
    # Define fonts
    font = ('@Yu Gothic UI Semibold', 10)
    Font = (('@Yu Gothic', 30, 'underline'))
    button_font=('@Yu Gothic', 12, 'underline')
    # Get a list of installed fonts
    fontlist = []
    for i in sg.Text.fonts_installed_list():
        fontlist.append(i)

    # Set the theme and default font options
    sg.theme('DarkAmber')
    sg.set_options(font=font)

    # Define the layout of the window
    layout = [  
        [sg.Button('❌', font=('@Yu Gothic UI Semibold', 20), pad=((905,30),(30,0)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0 )],  # Exit button
        [sg.Text('Welcome! Please login', font=Font, pad=((30,70),(0,20)), key='-text-', size=(0, 1))], 
        [sg.Button('or sign up here. ', font=("@Yu Gothic", 18, 'underline'), pad=((120,0),(0,20)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0 )],
        
        [sg.Text('Username: ', font=("@Yu Gothic", 16), pad=((100,0),(25,25))), sg.InputText(background_color=sg.theme_background_color(), border_width=0)],
        
        [sg.Text('Password: ', font=('@Yu Gothic', 16), pad=((100,0),(50,50))), sg.InputText(background_color=sg.theme_background_color(), border_width=0),
        sg.Text('', font=("@Yu Gothic", 9), pad=((10,0),(0,0)), key='-error-'),
         ],                                                                                     
                                                                                             
                                                                                             
       

        [sg.Button('Login.', font=button_font, pad=((885,30),(90,20)), button_color=(sg.theme_text_color(), sg.theme_background_color()), border_width=0)],
    ]

    # Create the Window
    window = sg.Window('Sign_up', layout, no_titlebar=True, size=(1000,600), font=font)
    

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        

        # Process events and update the window
        event, values = window.read(timeout=10)
        
       # successful, user_id = login_check()
        
        # Handle events

        
        # Check for different events and handle them accordingly
        if event == '❌':
            # If the event is '❌', break out of the loop or function
            break
        elif event== 'or sign up here. ':
            print(2)
            
            sign_up1()
            break
        elif event== 'Login.' and values[0]!='' and values[1]!='':
            successful, user_id = login_check(values[0], values[1])
            if successful:

                return user_id
            else:
                
                window['-error-'].update('Incorrect username or password')
                
        
      

             
# Call the function to run the GUI
