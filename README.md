# GhostGPT

<img width="608" alt="Screenshot 2023-03-01 at 8 04 30 PM" src="https://user-images.githubusercontent.com/39002684/222304189-09cd2422-666b-44a9-9b2f-ab1a17c7c113.png">

Ghost is a ChatBot based on chatGPT that runs in your terminal and other platforms(Telegram!). The unique thing about ghost is that you can create locally stored 'neural imprints' (.ni files) which are basically chat histories that shape Ghost's behavior. And you can also load imprints created by other people into Ghost to give it different personalities or features.

## Requirements
Ghost is developed and tested under MacOS.
For both implementations of Ghost(shell, telegram), you at least need Python and openai module installed:
```
pip install openai
```
For telegram, you will also need to install the telegram api module:
```
pip install python-telegram-bot --upgrade
```


## Usage
Under the folder of each version, you will find a shell script called `gst.sh` which is a gateway for creating new imprints, injecting existing imprints into ghost, or wiping imprints clean. This is simply started by calling:
```
./gst.sh
```
<img width="793" alt="Screenshot 2023-03-01 at 8 23 15 PM" src="https://user-images.githubusercontent.com/39002684/222306542-1f0ca5b1-ab1f-4ee7-9994-6786a074ddef.png">

## Ghost in the Shell
<img width="1139" alt="Screenshot 2023-03-01 at 8 26 35 PM" src="https://user-images.githubusercontent.com/39002684/222306986-b93f7675-b986-41c0-9efe-4fcc1726ea4a.png">
## Ghost in the Telegram
<img width="607" alt="Screenshot 2023-03-01 at 8 27 37 PM" src="https://user-images.githubusercontent.com/39002684/222307122-82ddcd05-540d-4a72-a359-677469f69ac6.png">

Of course, you can let them share the same `IMPRINTS` folder so they are sharing the same memories across platforms
