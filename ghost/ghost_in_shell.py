import openai
import sys
from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich import box
import ghost_helper

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

DEBUG = False
TOKEN_REQUEST_LIMIT = 4096-200

imprint = sys.argv[1]
print("\nInjecting Nerual imprint: "+ str(imprint)+" ...")
print("\n*Note: type [eject] to eject imprint <"+str(imprint)+"> from ghost")

imprint_path = "IMPRINTS/"+imprint+".ni"

imprint_file =open(imprint_path)
chat_history = eval(imprint_file.read())
imprint_file.close()


def history_add(history, role, content):
    history.append({"role": role, "content": content})
    return history


def chat(history,content):
    unanswered_history = history_add(history,"user",content)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=unanswered_history,
        temperature=0,
        stream=True)
    print('\033[38;5;33m' +"GHOST"+ '\033[0;0m: ', end='')

    with Live(auto_refresh=False, vertical_overflow="visible") as live:
        print('',end='\n') #maybe a rich bug, can't update the first token
        msg = ""
        for chunk in response:
            try:
                chunk_message = chunk['choices'][0]['delta']['content']
                msg += chunk_message

                table = Table(show_header=False, box=box.ROUNDED)
                table.add_row(Markdown(msg))
                live.update(table, refresh=True)
            except KeyError:
                pass

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
        if(DEBUG):
            print("Total token:", ghost_helper.token_est(chat_history))

            if(ghost_helper.token_est(chat_history)<TOKEN_REQUEST_LIMIT):
                token_outbound_count = 0
                chat(chat_history, usr_input)
            else:
                token_outbound_count = token_outbound_count + 1
                chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
                chat(chat_history, usr_input)
        else:
            try:      
                if(ghost_helper.token_est(chat_history)<TOKEN_REQUEST_LIMIT):
                    token_outbound_count = 0
                    chat(chat_history, usr_input)
                else:
                    token_outbound_count = token_outbound_count + 1
                    chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
                    chat(chat_history, usr_input)
            except:
                print("GHOST: -_- ERROR") #More useful messages in the future?




