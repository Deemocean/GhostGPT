from ghost import imprint
import openai
import sys
from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich import box
import ghost_helper
import os 

import json
#Get options.
config_dict = {}
data_file_path = 'config/config.json'
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
    # if(usr_input!="eject"):
    #     if(DEBUG):
    #         print("Total token:", ghost_helper.token_est(chat_history))

    #         if(ghost_helper.token_est(chat_history)<TOKEN_REQUEST_LIMIT):
    #             token_outbound_count = 0
    #             chat(chat_history, usr_input)
    #         else:
    #             token_outbound_count = token_outbound_count + 1
    #             chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
    #             chat(chat_history, usr_input)
    #     else:
    #         try:      
    #             if(ghost_helper.token_est(chat_history)<TOKEN_REQUEST_LIMIT):
    #                 token_outbound_count = 0
    #                 chat(chat_history, usr_input)
    #             else:
    #                 token_outbound_count = token_outbound_count + 1
    #                 chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
    #                 chat(chat_history, usr_input)
    #         except:
    #             print("GHOST: -_- ERROR") #More useful messages in the future?




