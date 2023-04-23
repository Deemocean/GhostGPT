import openai
from ghost import imprint
import logging
from telegram import Update, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os
TOKEN= None
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

imp = imprint.get()
print("\nInjecting Nerual imprint: "+ str(imp.name)+" ...")
print("\n*Note: type [eject] to eject imprint <"+str(imp.name)+"> from ghost")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/g--talk to ghost /imgc--generate img from Dall-E /wipe wipe ghost memory")

async def g(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global token_outbound_count
    global chat_history
    usr_input = update.effective_message.text[3:]
    try:
        resp = imp.chat(usr_input)
    except Exception as e:
         resp = str(e)

    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp,parse_mode=ParseMode.MARKDOWN_V2)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp)


async def wipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global imp
    imp.wipe()
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
    g_handler = CommandHandler('g', g)
    imgc_handler = CommandHandler('imgc', imgc)
    wipe_handler = CommandHandler('wipe', wipe)

    application.add_handler(start_handler)
    application.add_handler(g_handler)
    application.add_handler(imgc_handler)
    application.add_handler(wipe_handler)
    
    application.run_polling()