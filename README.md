# GhostGPT

<img width="907" alt="Screenshot 2023-03-02 at 6 28 17 PM" src="https://user-images.githubusercontent.com/39002684/222587190-b4d033f2-b9dd-4525-bb05-fabe8b47140f.png">


Ghost is a ChatBot based on the GPT3.5-turbo/DALLE model that runs in your terminal and on other platforms(Telegram). The unique thing about ghost is that you can create locally stored 'neural imprints' (.ni files) which for now are basically chat histories that shape Ghost's behavior. And you can also load imprints created by other people into Ghost to give it different personalities or features.

## Requirements
Ghost is developed and tested under MacOS/Linux

First, you need to install the required libraries, in the menu(`./gst.sh`), select:
```
4) [Config] -> 1) [Install] Required Libs
```
Second, fill in the nessary API keys(if you are not gonna run it on telegram, you dont need the bot token)

Generate a OpenAI's API KEY from https://platform.openai.com/account/api-keys

Generate a bot token from bot father: https://telegram.me/BotFather

In the menu, select:
```
4) [Config] -> 2) [Config] Keys
```

## Usage
Clone this project : 
```
git clone https://github.com/Deemocean/GhostGPT.git
```
`cd` into the project folder, you will find a shell script called `gst.sh` which is the overall menu for configuring your key/token/preferences, creating new imprints, injecting existing imprints into ghost, wiping imprints clean, install required libs. This is simply started by calling:
```
./gst.sh
```
<img width="1140" alt="Screenshot 2023-03-05 at 7 21 56 PM" src="https://user-images.githubusercontent.com/39002684/222995006-e2a4a3ef-a947-4cd5-b20f-6a3f067e0fe8.png">

## Ghost in the Shell
<img width="829" alt="Screenshot 2023-03-05 at 7 38 42 PM" src="https://user-images.githubusercontent.com/39002684/222995716-95db4f76-5f38-4982-93a6-2694f884fa19.png">

## Ghost in the Telegram
It is easy to deploy Ghost onto linux servers, more features with editing imprints in telegram client, and UI is in progress :)
As here we are going to call either the chatbot or DALL-E through commands `/gst`(ghost) and `/imgc`(image create), group chat is natually supported 

<img width="607" alt="Screenshot 2023-03-01 at 8 27 37 PM" src="https://user-images.githubusercontent.com/39002684/222307122-82ddcd05-540d-4a72-a359-677469f69ac6.png">

<img width="440" alt="Screenshot 2023-03-05 at 7 30 08 PM" src="https://user-images.githubusercontent.com/39002684/222995232-5d1348e3-4c4c-4131-ba30-91fc903df6a9.png">

## Possible Future Updates
1. Add more parameters of the model into the imprint
2. Teach Ghost to do Google search before it replies-(by inputting Google API response of the prompt, and telling ghost it is the search result beforehand)
3. and more
