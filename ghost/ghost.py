import openai
from rich.console import Console
from rich.markdown import Markdown
import os
import sys
console = Console()
class imprint:
    path = ""
    name = ""
    history = []
    forget = True
    telegram = False
    TOKEN_REQUEST_LIMIT = 4096
    token_factor = 1.2
    token_outbound_count = 0
    printing = True

    def log(self, str, **kwargs):
        if self.printing:
            print(str, **kwargs)
    
    def markdown(self, obj, **kwargs):
        if self.printing:
            console.print(obj, **kwargs)

    def within_tokens(self):
        return len(str(self.history))/self.token_factor < self.TOKEN_REQUEST_LIMIT
    
    def __init__(self, name, printing= True):
        self.printing = printing
        self.name = name.upper()
        self.path = os.path.join("IMPRINTS" , name + ".ni")
        try:
            self.log("\nInjecting Nerual imprint: " + self.name + " ...") 
            self.read()
        except FileNotFoundError:
            self.wipe()
            self.log("\nCreating a new imprint: " + self.name + " ...")
       
        self.log("*Note: type [eject] to eject imprint <"+str(self.name)+"> from ghost")
        self.log("Type [delete] to delete the last entry and response from memory.\n")

    def generate(printing = True):
        temp_num = 0
        temp_name = "temp"
        imprints = os.listdir("IMPRINTS")
    
        while temp_name in imprints:
            temp_num = temp_num + 1
            temp_name = "temp" + str(temp_num)
        return imprint(temp_name, printing=printing)
    
    def get(printing = True):
        try:
            name = sys.argv[1]
            imp = imprint(name, printing= printing)
        except IndexError:
            imp = imprint.generate(printing = printing)
        try:    
            imp.forget = os.environ["FORGET"] == "True"
        except KeyError:
            pass
        return imp

    def wipe(self):
        self.history = []
        self.save()
        
    def save(self):
        with open(self.path, "w") as nifile:
            nifile.write(str(self.history))

    def read(self):
        with open(self.path) as imprint_file:
            self.history = eval(imprint_file.read())
    
    def history_add(self, role, content):
        if self.history is not None:
            self.history.append({"role": role, "content": content})
            self.save()
        return self.history

    def rm_history(self,n):
        init_size = len(self.history)
        for entry in self.history:
            if n > 0 and entry["role"] != "training":
                i = self.history.index(entry)
               
                try:
                    entry_after = self.history[i + 1]
                    if entry_after["role"] == "assistant":
                        self.history.remove(entry_after)
                        n = n - 1
                except:
                    pass
                self.history.remove(entry)
                n = n - 1
        self.save()
        return init_size - len(self.history)
    
    def delete(self):
        try:
            self.history = self.history[0:(len(self.history) -1)]
            self.history = self.history[0:(len(self.history) -1)]
        except IndexError:
            pass
        self.save()

    def chat(self, content):
        head = ""
        mode = "user" if self.forget else "training"
        self.history_add(mode,content)
        if (self.within_tokens()):
            self.log('\033[38;5;33m' + self.name + '\033[0;0m: ', end="")
            self.token_outbound_count = 0
        else:
            self.token_outbound_count = self.token_outbound_count + 1
            d = self.rm_history(self.token_outbound_count)
            if (d > 0):
                self.log('\033[38;5;33m' + self.name +"[MEM FADING]"+ '\033[0;0m: ', end="")
                msg = "[MEM FADING]: "
            else:
                self.log('\033[38;5;33m' + self.name +"[MEM FULL]"+ '\033[0;0m: ', end="")
                msg = "[MEM FULL]: "

        unanswered_history = []
        if self.history is not None:
            mode = "user" if self.forget else "training"
            unanswered_history = self.history_add(mode, content)
        else:
            unanswered_history = [{'role': 'user', 'content': content}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=list(map(lambda entry: entry if entry["role"] == "user" else {'role':'user', 'content':entry['content']}, unanswered_history)),
            temperature=0,
            stream=not self.telegram
        )
        msg = ""
        is_markdown = False
        if not self.telegram:
            try:
                content.lower().index("markdown")
                is_markdown = True
            except ValueError:
                pass
        if not is_markdown:
            for chunk in response:
                try:
                    chunk_message = chunk['choices'][0]['delta']['content'] 
                    msg = msg + chunk_message 
                    if not self.telegram:
                        self.log(chunk_message, end='', flush=True)
                except KeyError:
                    pass
            if not self.telegram:
                self.log("\n")
        elif not self.telegram:
            line = ""
            for chunk in response:
                try:
                    chunk_message = chunk['choices'][0]['delta']['content']
                    msg = msg + chunk_message
                    line = line + chunk_message
                    try:
                        line.index("\n")
                        self.markdown(Markdown(line), end='')
                        line = ""
                    except ValueError:
                        pass
                except KeyError:
                    pass
            self.log("\n")
        self.history_add("assistant",msg)
        return head + msg
    
