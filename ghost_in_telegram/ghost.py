import openai
import sys
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes


# TOKEN ="YOUR_TELEGRAM_TOKEN"
# openai.api_key = "YOUR_OPENAI_API_KEY"



TOKEN_REQUEST_LIMIT = 4096
token_outbound_count = 0

imprint = sys.argv[1]
print("\nInjecting Nerual imprint: "+ str(imprint)+" ...")
print("\n*Note: type [eject] to eject imprint <"+str(imprint)+"> from ghost")

imprint_path = "IMPRINTS/"+imprint+".ni"

imprint_file =open(imprint_path)
chat_history = eval(imprint_file.read())
imprint_file.close()

def token_est(history):
    return len(str(history))

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

def token_est(history):
    return len(str(history))/1.2

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def gst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global token_outbound_count
    global chat_history
    usr_input = update.effective_message.text[5:]

    if(token_est(chat_history)<TOKEN_REQUEST_LIMIT):
        token_outbound_count = 0
        resp = chat(chat_history, usr_input)
    else:
          token_outbound_count = token_outbound_count + 1
          chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
          resp= "*[Losing Old Memory]: "+chat(chat_history, usr_input)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('menu', menu)
    gst_handler = CommandHandler('gst', gst)

    application.add_handler(start_handler)
    application.add_handler(gst_handler)
    
    application.run_polling()








