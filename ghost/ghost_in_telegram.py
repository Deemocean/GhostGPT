import openai
from ghost import imprint
import logging
from telegram import Update, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import ghost_helper
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

imp = imprint.get(printing = False)
print("\nInjecting Nerual imprint: "+ str(imp.name)+" ...")
print("\n*Note: type [eject] to eject imprint <"+str(imp.name)+"> from ghost")

# TOKEN_REQUEST_LIMIT = 4096-200
# token_outbound_count = 0

# imprint = sys.argv[1]
# print("\nInjecting Nerual imprint: "+ str(imprint)+" ...")
# print("\n*Note: type [eject] to eject imprint <"+str(imprint)+"> from ghost")

# imprint_path = "IMPRINTS/"+imprint+".ni"

# imprint_file =open(imprint_path)
# chat_history = eval(imprint_file.read())
# imprint_file.close()


# def history_add(history, role, content):
#     history.append({"role": role, "content": content})
#     return history


# def chat(history,content):
#     unanswered_history = history_add(history,"user",content)
#     response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=unanswered_history)
#     msg = response['choices'][0]['message']['content']
#     history_add(history, "assistant",msg)
#     save(history,imprint_path)
#     return msg

# def save(history, path):
#     nifile = open(path, "w")
#     nifile.write(str(history))
#     nifile.close()

# def rm_history(history,path,n):
#     shorter_history=history[n:]
#     save(shorter_history,path)
#     return shorter_history

# def wipe_history(history,path):
#     history=[]
#     save(history,path)
#     return history


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/g--talk to ghost /imgc--generate img from Dall-E /wipe wipe ghost memory")
# async def g(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     global token_outbound_count
#     global chat_history
#     usr_input = update.effective_message.text[3:]
#     try:
#         if(ghost_helper.token_est(chat_history)<TOKEN_REQUEST_LIMIT):
#             token_outbound_count = 0
#             resp = chat(chat_history, usr_input)
#         else:
#             token_outbound_count = token_outbound_count + 1
#             chat_history = rm_history(chat_history,imprint_path,token_outbound_count)
#             resp= "[MEM FADING]"+chat(chat_history, usr_input)
#     except:
#         resp = "Error :("
async def gst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global token_outbound_count
    global chat_history
    usr_input = update.effective_message.text[5:]
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