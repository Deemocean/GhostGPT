import openai
import sys

#PUT YOUR OPENAI API KEY HERE:
#openai.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

imprint = sys.argv[1]
#imprint = "test"
print("\nInjecting Nerual Imprint: "+ str(imprint)+" ...")

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
    messages=unanswered_history)
    msg = response['choices'][0]['message']['content']
    history_add(history, "assistant",msg)
    save(history,imprint_path)
    return msg

def save(history, path):
    nifile = open(path, "w")
    nifile.write(str(history))
    nifile.close()

usr_input=""
while (usr_input!="exit"):
    usr_input=input("YOU: ")
    if(usr_input!="exit"):
      print("GHOST: "+chat(chat_history, usr_input))