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
    TOKEN_REQUEST_LIMIT = 4096
    token_factor = 0.5
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
        if self.history is not None:
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
        else:
            return 0
    
    def delete(self):
        try:
            self.history = self.history[0:(len(self.history) -1)]
            self.history = self.history[0:(len(self.history) -1)]
        except IndexError:
            pass
        self.save()

    def chat(self, content=None, head=""):
        msg = ""
        if content is None:
            content = self.history[len(self.history) -1]["content"]
        else:
            self.history_add("user" if self.forget else "training",content)

        if (self.within_tokens()):
            self.token_outbound_count = 0
        else:
            self.token_outbound_count = self.token_outbound_count + 1
            D = self.rm_history(self.token_outbound_count)
            if D == 0:
                head = "[MEM FULL]: "

        unanswered_history = self.history if self.history is not None else [{'role': 'user', 'content': content}]
        response = None
        try: 
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=list(map(lambda entry: entry if entry["role"][0] != "t" else {'role':'user', 'content':entry['content']}, unanswered_history)),
                temperature=0,
                stream=True
            )
        except openai.error.InvalidRequestError:
            if self.history is not None:
                self.token_outbound_count = self.token_outbound_count + 1
                diff = self.rm_history(self.token_outbound_count)
                if diff == 0:
                    self.log("[MEM OVER CAPACITY]: Has much training data!")
                    return "[MEM OVER CAPACITY]: Has much training data!"
                else:
                    return self.chat(content=None, head = head)
            else:
                self.log("Request too long!")
                return "Request too long!"
        self.log('\033[38;5;33m' + self.name + head + '\033[0;0m: ', end="")
        is_markdown = "markdown" in content.lower()
        line = ""
        for chunk in response:
            try:
                chunk_message = chunk['choices'][0]['delta']['content']
                msg = msg + chunk_message
                line = line + chunk_message
                if not is_markdown:
                    self.log(chunk_message, end = '', flush = True) 
                elif "\n" in line:
                    self.markdown(Markdown(line), end='')
                    line = ""
            except KeyError:
                pass
        self.log("\n")
        self.history_add("assistant",msg)
        return head + msg