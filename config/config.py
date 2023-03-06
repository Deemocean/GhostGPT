import os
import sys
import json

options = ["OPENAI_KEY", "TELEGRAM_TOKEN"]
config_path = 'config/config.json'
old_config = {}

command = sys.argv[1]

blue = '\033[38;5;33m'
no_color = '\033[0m'


def config_keys(): 
    #Get old options.
    try:
        with open (config_path) as config:
            old_config = json.load(config)
    except FileNotFoundError:
        pass
    except json.decoder.JSONDecodeError:
        pass


    new_config = {}
    print("Press the [return]/[enter] key to skip a preference.\nEnter 'delete' to remove data.\n")
    with open (config_path, 'w') as config:
        for option in options:
            is_filled = False
            try:
                #See if field has been previously filled.
                old_val = old_config[option]
                is_filled = True
            except KeyError:
                pass

            if not is_filled:
                #New value not in config file.
                opt = input("INPUT NEW " + option +  ": ")

                if opt == "" or opt.lower() == "delete":
                    print("Value ignored.\n")
                else:
                    new_config[option] = opt
                    print("New value registered!\n")
            else:
                #Value previously in config file.
                print("PREV VALUE: " + blue+old_config[option]+no_color)
                opt = input("UPDATE " + option +  ": ")

                if opt == 'delete':
                    #Field to not be included.
                    print("Field deleted.\n")
                elif opt != "":
                    #Value updated.
                    new_config[option] = opt
                    print("Change successful!\n")
                else:
                    #No change wanted.
                    new_config[option] = old_config[option]
                    print("No change made.\n")
        json.dump(new_config, config, indent=6)
    os.chmod(config_path, 0o600)       

def print_keys():
    open_ai_key = ""
    telegram_token= ""

    try:
        with open (config_path) as config:
            config_dict = json.load(config)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        pass

    try:
        open_ai_key  = config_dict[options[0]]
    except KeyError:
        pass

    try:
        telegram_token = config_dict[options[1]]
    except KeyError:
        pass

    print("OpenAI KEY: "+'\033[38;5;33m' +open_ai_key+ '\033[0;0m', end='\n')
    print("Telegram TOKEN: "+'\033[38;5;33m'+telegram_token+ '\033[0;0m', end='\n')


if(command=="config"):
    config_keys()
elif(command=="print_keys"):
    print_keys()