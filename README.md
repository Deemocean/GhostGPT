# GhostGPT

<img width="907" alt="Screenshot 2023-03-02 at 6 28 17 PM" src="https://user-images.githubusercontent.com/39002684/222587190-b4d033f2-b9dd-4525-bb05-fabe8b47140f.png">


Ghost is a ChatBot based on ChatGPT that runs in your terminal and other platforms(Telegram also has DALL-E!). The unique thing about ghost is that you can create locally stored 'neural imprints' (.ni files) which are basically chat histories that shape Ghost's behavior. And you can also load imprints created by other people into Ghost to give it different personalities or features.

## Requirements
Ghost is developed and tested under MacOS.
For both implementations of Ghost(shell, telegram), you at least need Python 3.7+ and openai module installed:
```
pip install openai
```
And generate a OpenAI's API KEY from https://platform.openai.com/account/api-keys, fill that using the "Configure" menu option in the shell script.

For the Telegram implementation, you will also need to install the telegram api module:
```
pip install python-telegram-bot --upgrade
```
And generate a bot token from bot father(https://telegram.me/BotFather) , fill that in like the API KEY in the same manner.

## Usage
Under the folder of each version, you will find a shell script called `gst.sh` which is a gateway for configuring your key/token/preferences, creating new imprints, injecting existing imprints into ghost, or wiping imprints clean. This is simply started by calling:
```
./gst.sh
```
<img width="502" alt="Screenshot 2023-03-03 at 10 02 59 PM" src="https://user-images.githubusercontent.com/92696735/222872671-3c49ad62-9ad3-4bda-8897-a3ed9582caf0.png">



## Ghost in the Shell
<img width="502" alt="Screenshot 2023-03-03 at 10 04 31 PM" src="https://user-images.githubusercontent.com/92696735/222872738-eeedb10e-3c47-450e-adb6-ec9a7acdd6c1.png">


## Ghost in the Telegram
It is easy to deploy Ghost onto linux servers, more features with editing imprints in telegram client, and UI is in progress :)
As here we are going to call either the chatbot or DALL-E through commands `/gst`(ghost) and `/imgc`(image create), group chat is natually supported 

<img width="607" alt="Screenshot 2023-03-01 at 8 27 37 PM" src="https://user-images.githubusercontent.com/39002684/222307122-82ddcd05-540d-4a72-a359-677469f69ac6.png">

<img width="491" alt="Screenshot 2023-03-02 at 9 11 11 PM" src="https://user-images.githubusercontent.com/39002684/222614214-c477078c-9610-4abe-93da-c2c6d0d95827.png">


Of course, you can let them share the same `IMPRINTS` folder so they are sharing the same memories across platforms
