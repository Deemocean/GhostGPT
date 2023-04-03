import openai
import sys
import logging
import ghost_in_shell as ghost
from telegram import Update, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import os
tg_token= None
openai.api_key = None
try:
    openai.api_key = os.environ["OPENAI_KEY"]
except KeyError:
    print("No openAI key found!")
    exit()
try:
    TOKEN = os.environ["TELEGRAM_TOKEN"]
except KeyError:
    print("No Telegram token found!")
    exit()
forget = os.environ["FORGET"] == "True"
TOKEN_REQUEST_LIMIT = 4096
token_outbound_count = 0

imprint = sys.argv[1]
print("\nInjecting Nerual imprint: "+ str(imprint)+" ...")
print("\n*Note: type [eject] to eject imprint <"+str(imprint)+"> from ghost")

imprint_path = "IMPRINTS/"+imprint+".ni"

with open(imprint_path) as imprint_file:
    chat_history = eval(imprint_file.read())

def token_est(history):
    ghost.token_est(history)

def history_add(history, role, content):
    return ghost.history_add(history, role, content)


def chat(history,content,path):
    return ghost.chat(history, content, path, telegram=True)

def save(history, path):
    ghost.save(history, path)

def rm_history(history,path,n):
    return ghost.rm_history(history, path, n)

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
            resp = chat(chat_history, usr_input, imprint_path)
        else:
            token_outbound_count = token_outbound_count + 1
            initial_length = len(chat_history)
            chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
            if initial_length - len(chat_history) > 0:
                resp = "[MEM FADING]: " + chat(chat_history, usr_input, imprint_path)
            else:
                resp = "[MEM FULL]: " + chat(chat_history, usr_input, imprint_path)
    except Exception as e:
        resp = str(e)


    #resp=escape_markdown(resp, version=2)
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp,parse_mode=ParseMode.MARKDOWN_V2)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)


async def wipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_history
    chat_history = wipe_history(chat_history, imprint_path)
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
