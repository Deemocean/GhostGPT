# GhostGPT

<img width="594" alt="Screenshot 2023-03-01 at 8 51 39 PM" src="https://user-images.githubusercontent.com/39002684/222310215-bd37bb72-0ed2-4b4b-bc54-31612ffd5dde.png">

Ghost is a ChatBot based on chatGPT that runs in your terminal and other platforms(Telegram!). The unique thing about ghost is that you can create locally stored 'neural imprints' (.ni files) which are basically chat histories that shape Ghost's behavior. And you can also load imprints created by other people into Ghost to give it different personalities or features.

## Requirements
Ghost is developed and tested under MacOS.
For both implementations of Ghost(shell, telegram), you at least need Python and openai module installed:
```
pip install openai
```
And generate a OpenAI's API KEY from https://platform.openai.com/account/api-keys, fill that in `ghost.py`
```
# openai.api_key = "YOUR_OPENAI_API_KEY"
```
For the Telegram implementation, you will also need to install the telegram api module:
```
pip install python-telegram-bot --upgrade
```
And generate a bot token from bot father(https://telegram.me/BotFather) , fill that in `ghost.py`
```
TOKEN ="YOUR_TELEGRAM_TOKEN"
```


## Usage
Under the folder of each version, you will find a shell script called `gst.sh` which is a gateway for creating new imprints, injecting existing imprints into ghost, or wiping imprints clean. This is simply started by calling:
```
./gst.sh
```
<img width="795" alt="Screenshot 2023-03-01 at 8 50 59 PM" src="https://user-images.githubusercontent.com/39002684/222310139-590e5cd9-04d1-49e2-aa7f-7fc87abfa8ff.png">


## Ghost in the Shell
<img width="795" alt="Screenshot 2023-03-01 at 8 49 55 PM" src="https://user-images.githubusercontent.com/39002684/222309983-29f0228a-d7e3-41e9-abda-ba9f7a9b8faf.png">


## Ghost in the Telegram
<img width="607" alt="Screenshot 2023-03-01 at 8 27 37 PM" src="https://user-images.githubusercontent.com/39002684/222307122-82ddcd05-540d-4a72-a359-677469f69ac6.png">

Of course, you can let them share the same `IMPRINTS` folder so they are sharing the same memories across platforms
