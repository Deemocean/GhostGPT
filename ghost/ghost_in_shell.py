from ghost import imprint
import openai
import os 
#Get options.
try:
    openai.api_key = os.environ["OPENAI_KEY"]
except KeyError:
    print("No openAI token found!")
    exit()
imp = imprint.get()
usr_input=input('\033[38;5;33m' +"YOU"+ '\033[0;0m: ')

while (usr_input!="eject"): 
    if(usr_input=="delete"):
        imp.delete()
    else:
        imp.chat(usr_input)
    usr_input=input('\033[38;5;33m' +"YOU"+ '\033[0;0m: ')