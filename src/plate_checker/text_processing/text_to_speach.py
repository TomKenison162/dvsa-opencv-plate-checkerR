from gtts import gTTS 
import pygame
import time
import os
# This module is imported so that we can  
 
def tts(text):
# The text that you want to convert to audio 
    
    os.remove('welcome2.mp3')
    # Language in which you want to convert 
    language = 'en'
    
    # Passing the text and language to the engine,  
    # here we have marked slow=False. Which tells  
    # the module that the converted audio should  
    # have a high speed 
    myobj = gTTS(text=text, lang=language, slow=False) 
    
    # Saving the converted audio in a mp3 file named 
    # welcome  
    myobj.save("welcome2.mp3") 
    


    # Initialize pygame
    pygame.init()


    
    pygame.mixer.music.load('welcome2.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

# Wait until the music finishes playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)  # You can adjust the sleep duration if needed
    pygame.mixer.music.stop()

    # Uninitialize pygame
    pygame.quit()   
        

