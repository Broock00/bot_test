import os
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME: Final = '@xlounge_bot'

# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello wellcome to the x lounge service, im ur assistant...')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('do u need help?')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('this is custome command, let me know if u need smtg')

def handle_response(text: str):
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey There'
    
    if 'how are you' in processed:
        return 'I am good'
    
    if 'i love python' in processed:
        return 'Remeber the man'
    
    return 'i dont understand what you wrote...'

from telegram.error import TimedOut

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message_type: str = update.message.chat.type
        text: str = update.message.text

        print(f'user ({update.message.chat.id}) in {message_type}: "{text}"')

        if message_type == 'group':
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                response: str = handle_response(new_text)
            else:
                return
        else:
            response: str = handle_response(text)

        print('Bot:', response)
        await update.message.reply_text(response)

    except TimedOut:
        print("⚠️ Warning: Message response timed out! Retrying...")
        await update.message.reply_text("Oops, that took too long! Try again.")



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=0.5)
