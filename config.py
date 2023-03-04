import csv
import os

options = ["API_KEY", "TELEGRAM_TOKEN"]
old_fields = []
old_contents=[]
config_path = '../config.txt'
#Get old options.
try:
    with open (config_path, 'r') as config:
        config_reader = csv.reader(config)
        old_config = [opt for opt in config_reader]
        old_fields = [entry[0] for entry in old_config]
        old_contents=[entry[1] for entry in old_config]
except FileNotFoundError:
    pass

print("Welcome to the configurer!\nPress return/enter to not change a preference.\n")
with open (config_path, 'w') as config:
    for option in options:
        ind = -1
        try:
            #See if field has been previously filled.
            ind = old_fields.index(option)
        except ValueError:
            pass

        if ind == -1:
            #New value not in config file.
            opt = input("INPUT NEW " + option +  ": ")
            if opt != "":
                config.write(option + ", " + opt + "\n")
                print("New value registered!\n")
            else:
                print("Value ignored.\n")
        else:
            #Value previously in config file.
            print("PREV VALUE: " + old_contents[ind])
            opt = input("UPDATE " + option +  ": ")
            if opt != "":
                #Value updated.
                config.write(option + ", " + opt + "\n")
                print(" Change Successful!\n")
            else:
                #No change wanted.
                config.write(option + ", " + old_contents[ind] + "\n")
                print(" No change made.\n")
os.chmod(config_path, 0o600)       

