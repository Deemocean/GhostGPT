import openai
import sys
import logging
from telegram import Update, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

import json
#Get options.
config_dict = {}
data_file_path = 'config/config.json'
try:
    with open (data_file_path) as config:
        config_dict = json.load(config)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    print("No valid config file found!\nRun either the shell script or the python script.")
    exit()

key = ""
tg_token=""

try:
    key = config_dict["OPENAI_KEY"]
except KeyError:
    print("No openAI key found!")
    exit()

try:
    tg_token = config_dict["TELEGRAM_TOKEN"]
except KeyError:
    print("No Telegram token found!")
    exit()

openai.api_key = key
TOKEN = tg_token

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

def wipe_history(history,path):
    history=[]
    save(history,path)
    return history

def token_est(history):
    return len(str(history))/1.0

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/gst--talk to ghost /imgc--generate img from Dall-E /wipe wipe ghost memory")

async def gst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global token_outbound_count
    global chat_history
    usr_input = update.effective_message.text[5:]
    try:
        if(token_est(chat_history)<TOKEN_REQUEST_LIMIT):
            token_outbound_count = 0
            resp = chat(chat_history, usr_input)
        else:
            token_outbound_count = token_outbound_count + 1
            chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
            resp= "[MEM FADING]"+chat(chat_history, usr_input)
    except:
        resp = "Error :("


    #resp=escape_markdown(resp, version=2)
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp,parse_mode=ParseMode.MARKDOWN_V2)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)


async def wipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_history
    wipe_history(chat_history, imprint_path)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="All memories flushed")


async def imgc(update: Update, context: ContextTypes.DEFAULT_TYPE):

    usr_input = update.effective_message.text[5:]
    try:
        response = openai.Image.create(
            prompt=usr_input,
            n=4,
            size="1024x1024"
            )
        img0 = InputMediaPhoto(media=response['data'][0]['url'])
        img1 = InputMediaPhoto(media=response['data'][1]['url'])
        img2 = InputMediaPhoto(media=response['data'][2]['url'])
        img3 = InputMediaPhoto(media=response['data'][3]['url'])

        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=[img0,img1,img2,img3])
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="error :(...")
    #await context.bot.send_photo(chat_id=update.effective_chat.id, photo=resp)

# async def imgm(update: Update, context: ContextTypes.DEFAULT_TYPE):

#     file_id = update.document.file_id
#     new_file = await bot.get_file(file_id)
#     await new_file.download_to_drive()

#     try:
#         response = openai.Image.create(
#             prompt=usr_input,
#             n=1,
#             size="1024x1024"
#             )
#         resp = response['data'][0]['url']
#     except:
#         resp = "error :(..."
   
#         await context.bot.send_document(chat_id=update.effective_chat.id, document=resp)



if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('menu', menu)
    gst_handler = CommandHandler('gst', gst)
    imgc_handler = CommandHandler('imgc', imgc)
    wipe_handler = CommandHandler('wipe', wipe)

    application.add_handler(start_handler)
    application.add_handler(gst_handler)
    application.add_handler(imgc_handler)
    application.add_handler(wipe_handler)
    
    application.run_polling()








