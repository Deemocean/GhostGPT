import os
import json

options = ["API_KEY", "TELEGRAM_TOKEN"]

config_path = '../config.json'
old_config = {}
#Get old options.
try:
    with open (config_path) as config:
        old_config = json.load(config)
except FileNotFoundError:
    pass
except json.decoder.JSONDecodeError:
    pass



new_config = {}
print("Welcome to the configurer!\nPress return/enter to not change a preference.\n")
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
            if opt != "":
                new_config[option] = opt
                print("New value registered!\n")
            else:
                print("Value ignored.\n")
        else:
            #Value previously in config file.
            print("PREV VALUE: " + old_config[option])
            opt = input("UPDATE " + option +  ": ")
            if opt != "":
                #Value updated.
                new_config[option] = opt
                print("Change Successful!\n")
            else:
                #No change wanted.
                new_config[option] = old_config[option]
                print("No change made.\n")
    json.dump(new_config, config, indent=6)
os.chmod(config_path, 0o600)       

