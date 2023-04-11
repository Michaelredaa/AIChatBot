# -*- coding: utf-8 -*-
"""
Documentation: 
"""

# ---------------------------------
# Import Libraries
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


# ---------------------------------
# Variables


# ---------------------------------
# Start Here

def create_bot(telegram_bot_token, rapid_api_token):
    bot = Bot(token=telegram_bot_token)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    async def start_command(message: types.Message):
        await message.reply("Hi! I'm a bot created by Michael Reda.")

    @dp.message_handler()
    async def echo_message(message: types.Message):
        msg_text = message.text
        msg_id = message.chat.id

        await bot.send_chat_action(chat_id=msg_id, action=types.ChatActions.TYPING)
        ai_response = post_request(msg_text, rapid_api_token)

        await message.reply(ai_response)

    executor.start_polling(dp, skip_updates=True)


def post_request(in_text: str, rapidapi_key: str, model: str = "gpt-3.5-turbo"):
    url = "https://openai80.p.rapidapi.com/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": in_text
            }
        ]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "openai80.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json().get('choices')[0].get('message').get('content')


# Main Function
def main():
    telegram_bot_token = "TELEGRAM_TOKEN"
    rapidapi_token = "RAPIDAPI_TOKEN"
    create_bot(telegram_bot_token, rapidapi_token)


if __name__ == '__main__':
    main()
