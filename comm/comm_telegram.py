import asyncio

import telegram
from decouple import config


# async def send_telegram_message_wrapper(data):
def send_telegram_message(data):
    chat_id = config("TELEGRAM_CHAT_ID")
    token = config("TELEGRAM_TOKEN")

    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """

    # you must have username
    # add telegram bot raw to your group
    # type /start and he will give you json

    # bot token
    # token that can be generated talking with @BotFather on telegram

    async def send_telegram_message_wrapper(data):
        async with telegram.Bot(token=token) as bot:
            await bot.sendMessage(chat_id=chat_id, text=data)

    asyncio.run(send_telegram_message_wrapper(data))


if __name__ == '__main__':
    send_telegram_message('ppp')
