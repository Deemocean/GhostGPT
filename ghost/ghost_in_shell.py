import openai
import sys

from rich.console import Console
from rich.markdown import Markdown
console = Console()
import json

#Get options.
config_dict = {}
data_file_path = 'config/config.json'
try:
    with open (data_file_path) as config:
        config_dict = json.load(config)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    print("No valid config file found!\nRun either the shell script or the python script.")
    exit()

key = ""

try:
    key = config_dict["OPENAI_KEY"]
except KeyError:
    print("No openAI token found!")
    exit()
openai.api_key = key


TOKEN_REQUEST_LIMIT = 4096
chat_history = None
imprint = "GHOST"
imprint_path = None
try:
    imprint = sys.argv[1]
   

    imprint_path = "IMPRINTS/"+imprint+".ni"

    with open(imprint_path) as imprint_file:
        chat_history = eval(imprint_file.read())
    
    print("\nInjecting Nerual imprint: "+ str(imprint)+" ...")
    print("\n*Note: type [eject] to eject imprint <"+str(imprint)+"> from ghost")
except IndexError:
    print("\nContinuing without an imprint.\nNote: type [eject] to leave the ghost")
except FileNotFoundError:
    print("\nNo such imprint exists. Creating a new imprint.")
    imprint = sys.argv[1]
    imprint_path = "IMPRINTS/"+imprint+".ni"
    with open(imprint_path, 'w') as i:
        i.write("[]")
    print("*Note: type [eject] to eject imprint <"+str(imprint)+"> from ghost")

def token_est(history):
    return len(str(history))/1.2

def history_add(history, role, content):
    history.append({"role": role, "content": content})
    return history


def chat(history,content):
    response = None
    if history is not None:
        unanswered_history = history_add(history,"user",content)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=unanswered_history,
            temperature=0,
            stream=True)
        is_markdown = False
    else:
        unanswered_history = [{'role': 'user', 'content': content}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=unanswered_history,
            temperature=0,
            stream=True
        )
    is_markdown = False
    try:
        content.lower().index("markdown")
        is_markdown = True
    except ValueError:
        pass
    msg = ""
    if not is_markdown:
        for chunk in response:
            try:
                chunk_message = chunk['choices'][0]['delta']['content']
                msg = msg + chunk_message
                print(chunk_message, end='', flush=True)
            except KeyError:
                pass
    else:
        line = ""
        for chunk in response:
            try:
                chunk_message = chunk['choices'][0]['delta']['content']
                msg = msg + chunk_message
                line = line + chunk_message
                try:
                    line.index("\n")
                    console.print(Markdown(line), end='')
                    line = ""
                except ValueError:
                    pass
            except KeyError:

                pass
        
    print("\n")
    if history is not None:
        history_add(history, "assistant",(msg))
        save(history,imprint_path)

def save(history, path):
    nifile = open(path, "w")
    nifile.write(str(history))
    nifile.close()

def rm_history(history,path,n):
    shorter_history=history[n:]
    save(shorter_history,path)
    return shorter_history

token_outbound_count = 0
usr_input=""
while (usr_input!="eject"):
    usr_input=input('\033[38;5;33m' +"YOU"+ '\033[0;0m: ')
    if(usr_input!="eject"): 
        try:      
            if(token_est(chat_history)<TOKEN_REQUEST_LIMIT):
                token_outbound_count = 0
                print('\033[38;5;33m' +imprint.upper()+ '\033[0;0m: ', end="")
                chat(chat_history, usr_input)
            else:
                token_outbound_count = token_outbound_count + 1
                chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
                print('\033[38;5;33m' + imprint.upper() +"[MEM FADING]"+ '\033[0;0m: ', end="")
                chat(chat_history, usr_input)
        except:
            print("GHOST: -_- ERROR") #More useful messages in the future?

