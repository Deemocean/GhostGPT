import openai
import sys

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

imprint = sys.argv[1]
print("\nInjecting Nerual imprint: "+ str(imprint)+" ...")
print("\n*Note: type [eject] to eject imprint <"+str(imprint)+"> from ghost")

imprint_path = "IMPRINTS/"+imprint+".ni"

imprint_file =open(imprint_path)
chat_history = eval(imprint_file.read())
imprint_file.close()


def token_est(history):
    return len(str(history))/1.2

def history_add(history, role, content):
    history.append({"role": role, "content": content})
    return history


def chat(history,content):
    unanswered_history = history_add(history,"user",content)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=unanswered_history)
    msg = response['choices'][0]['message']['content']
    history_add(history, "assistant",msg)
    save(history,imprint_path)
    return msg

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
    usr_input=input("YOU: ")
    if(usr_input!="eject"):
        print("GHOST:"+chat(chat_history, usr_input))
        # try:      
        #     if(token_est(chat_history)<TOKEN_REQUEST_LIMIT):
        #         token_outbound_count = 0
        #         print("GHOST:"+chat(chat_history, usr_input))
        #     else:
        #         token_outbound_count = token_outbound_count + 1
        #         chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
        #         print("GHOST[MEM FADING]:"+chat(chat_history, usr_input))
        # except:
        #     print("GHOST: -_- ERROR")

