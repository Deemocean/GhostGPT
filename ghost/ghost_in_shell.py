import openai
import sys
import os

from rich.console import Console
from rich.markdown import Markdown

console = Console()

key = ""
openai.api_key = None
try:
    openai.api_key = os.environ["OPENAI_KEY"]
except KeyError:
    print("No openAI token found!")
    exit()

forget = os.environ["FORGET"] == "True"

TOKEN_REQUEST_LIMIT = 4096
chat_history = []
imprint = "GHOST"
imprint_path = None

def new_imprint(name):
    imprint_path = "IMPRINTS/"+name+".ni"
    print(imprint_path)
    with open(imprint_path, 'w') as i:
        i.write("[]")
    
try:
    imprint = sys.argv[1]
   

    imprint_path = "IMPRINTS/"+imprint+".ni"

    with open(imprint_path) as imprint_file:
        chat_history = eval(imprint_file.read())
    
    print("\nInjecting Nerual imprint: "+ str(imprint)+" ...")
except IndexError:
    temp_num = 0
    temp_name = "temp"
    imprints = os.listdir("IMPRINTS")
    
    while temp_name in imprints:
        temp_num = temp_num+1
        temp_name = "temp" + str(temp_num)

    new_imprint(temp_name)
    imprint = temp_name
    print("\nContinuing with a temporary imprint.")

except FileNotFoundError:
    print("\nNo such imprint exists. Creating a new imprint.")
    imprint = sys.argv[1]
    new_imprint(imprint)
print("*Note: type [eject] to eject imprint <"+str(imprint)+"> from ghost")
print("Type [delete] to delete the last entry and response from memory.")
   

def token_est(history):
    return len(str(history))/1.2

def history_add(history, role, content):
    history.append({"role": role, "content": content})
    return history


def chat(history,content, path, telegram=False):
    unanswered_history = None
    if history is not None:
        mode = "user" if forget else "training"
        unanswered_history = history_add(history,mode,content)
    else:
        unanswered_history = chat_history + [{'role': 'user', 'content': content}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=list(map(lambda entry: entry if entry["role"] == "user" else {'role':'user', 'content':entry['content']}, unanswered_history)),
        temperature=0,
        stream=True
    )

    is_markdown = False
    if not telegram:
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
                if not telegram:
                    print(chunk_message, end='', flush=True)
            except KeyError:
                pass
        if not telegram:
            print("\n")
    elif not telegram:
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
        save(history,path)
    return msg

def save(history, path):
    with open(path, "w") as nifile:
        nifile.write(str(history))

def rm_history(history,path,n):
    for entry in history:
        if n > 0 and entry["role"] == "user":
            i = history.index(entry)
            try:
                entry_after = history[i + 1]
                if entry_after["role"] == "assistant":
                    history.remove(entry_after)
                    n = n - 1
            except:
                pass
            history.remove(entry)
            n = n - 1
    
    save(history,path)
    return history
def shell_chat(chat_history):
    token_outbound_count = 0
    usr_input=""
    while (usr_input!="eject"):
        usr_input=input('\033[38;5;33m' +"YOU"+ '\033[0;0m: ')
        if(usr_input!="eject"): 
            #try:      
                if(usr_input=="delete"):
                    try:
                        chat_history = chat_history[0:(len(chat_history) -1)]
                        chat_history = chat_history[0:(len(chat_history) -1)]
                    except IndexError:
                        pass
                    
                elif(token_est(chat_history)<TOKEN_REQUEST_LIMIT):
                    token_outbound_count = 0
                    print('\033[38;5;33m' +imprint.upper()+ '\033[0;0m: ', end="")
                    chat(chat_history, usr_input, imprint_path)
                else:
                    token_outbound_count = token_outbound_count + 1
                    initial_length = len(chat_history)
                    chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
                    if initial_length - len(chat_history) > 0:
                        print('\033[38;5;33m' + imprint.upper() +"[MEM FADING]"+ '\033[0;0m: ', end="")
                        chat(chat_history, usr_input, imprint_path)
                    else:
                        print('\033[38;5;33m' + imprint.upper() +"[MEM FULL]"+ '\033[0;0m: ', end="")
                        chat(None, usr_input, imprint_path)


            #except:
              #  print("GHOST: -_- ERROR") #More useful messages in the future?
if sys.argv[0] == "ghost/ghost_in_shell.py":
    shell_chat(chat_history)
 