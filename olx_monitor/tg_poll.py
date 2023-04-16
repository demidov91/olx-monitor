import os
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler
from telegram.ext.filters import Regex
from telegram import Update

from olx_monitor.handlers import stop_updates, handle_browser_url, tg_help
from olx_monitor.url_interpreter import like_an_url_pattern
from olx_monitor.db import update_active_connection


async def _stop_poll_handle(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message_text = await stop_updates(chat_id)
    await context.bot.send_message(chat_id=chat_id, text=message_text)


async def _start_poll_handle(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await context.bot.send_video(
        chat_id=chat_id,
        video='https://user-images.githubusercontent.com/1383146/169698120-d1d8e047-9df7-4b37-aa12-d873a5d660dd.mp4',
    )

async def _help_poll_handle(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    message_text = await tg_help(chat_id)
    await context.bot.send_message(chat_id=chat_id, text=message_text)


async def _message_poll_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text

    message_text = await handle_browser_url(text, chat_id)
    await context.bot.send_message(chat_id=chat_id, text=message_text)


def start_polling_app():
    update_active_connection()

    tg_app = ApplicationBuilder().token(os.environ['TG_TOKEN']).build()
    tg_app.add_handlers(
        [
            CommandHandler('stop', _stop_poll_handle),
            CommandHandler('start', _start_poll_handle),
            CommandHandler('help', _help_poll_handle),
            MessageHandler(filters=Regex(like_an_url_pattern), callback=_message_poll_handler),
        ]
    )

    tg_app.run_polling()


if __name__ == '__main__':
    start_polling_app()