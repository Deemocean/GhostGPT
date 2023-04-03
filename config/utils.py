import rich
import os
from rich.prompt import Prompt
from rich.console import Console
from rich.columns import Columns
from rich import print
from rich.table import Table
from rich import box
from rich.align import Align
console = Console()

current_programs = ["shell", "telegram"]
options = [("OPENAI_KEY", "Paste your Open AI key here", ["Key"]),
 ("TELEGRAM_TOKEN","Paste your telegram token here", ["Key"]),
 ("DEFAULT_SCRIPT", "Pick one of the following to set your default interface", ["Shell", "Telegram", "None"]), 
 ("SAVE_SESSION", "Enter true/false if you want Ghost to remember your last session", ["True", "False"]) ]
options_list = map(lambda x: x[0], options)
options_exp = [""]

blue = '\033[38;5;33m'
b = "#0087FF"
no_color = '\033[0m'
def format_list(sl):
    s = ""
    i = 1;
    for o in sl:
        s = str(i) + ") " + o + ", "
    return s[0:end - 2]

def blue_print(s):
    console.print(s, style=b)

def line_break(s):
    console.rule(s, style = b)

def options_print():
    line_break("Settings")
    blue_print(", ".join(map(lambda x: x[0], options)))

def config_options():
    options_print()

    
def prompt_key(s, o):
    if (len(o[2]) == 0) or o[2][0] == "Key":
        return Prompt.ask(blue + s + " " + o[1] + no_color)
    else:
         return Prompt.ask(blue + s + " " + o[1] + no_color, choices = o[2])

def blue_print_fancy(s):
    console.print(s)

def options_print_fancy():
    columns = Columns(" ".join(map(lambda x: x[0], options)))
    print(columns)


table = Table(box=box.ASCII, show_lines=True)
cols = ["Option", "Current Value"]
for c in cols:
    table.add_column(c, justify="center")

def fill_options_table(current_vals):
    for option in options:
        prev_val = "None"
        try:
            prev_val = os.environ[option[0]]
        except:
            pass
        prev_val = "[Hidden]" if option[2][0] == "Key" and prev_val != "None" else prev_val
        table.add_row(option[0], prev_val)

def options_table_print():
    line_break ("Environment")
    print(Align.center(table, vertical="middle"))
    line_break ("Available imprints:")
    #os.system("ls IMPRINTS/*.ni | xargs -n 1 basename | sed -e 's/\.ni$//'")
    dir = os.listdir("IMPRINTS")

    opts = []
    for i in dir:
        opts.append("\[" + i[0:len(i)-3] + "]")

    opts = " ".join(opts)
    print(Align.center(opts, vertical="middle", style=b))
    line_break("")