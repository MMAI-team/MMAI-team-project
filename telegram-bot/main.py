import logging
from dotenv import dotenv_values
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CHOOSING_METHOD, SEND_FIRST_DOCUMENT, SEND_SECOND_DOCUMENT = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Move methods list to a config file
    reply_markup = ReplyKeyboardMarkup([["Method 1"], ["Method 2"]], resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot, please talk to me!\nChoose a method:",
                                   reply_markup=reply_markup)
    return CHOOSING_METHOD


async def choose_method(update: Update, context: CallbackContext):
    method_choice = update.message.text
    context.user_data['method'] = method_choice

    reply_markup = ReplyKeyboardRemove()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"You chose {method_choice}.\nNow, send the first document.",
                                   reply_markup=reply_markup)
    return SEND_FIRST_DOCUMENT


async def send_first_document(update: Update, context: CallbackContext):
    file_id = update.message.document.file_id

    # open file using opencv
    new_file = await context.bot.get_file(file_id)
    await new_file.download_to_drive('file1.jpg')

    reply_markup = ReplyKeyboardRemove()
    await context.bot.send_document(chat_id=update.effective_chat.id, document=file_id,
                                    reply_markup=reply_markup)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="First document received.\nNow, send the second document.")
    return SEND_SECOND_DOCUMENT


async def send_second_document(update: Update, context: CallbackContext):
    file_id = update.message.document.file_id

    # open file using opencv
    new_file = await context.bot.get_file(file_id)
    await new_file.download_to_drive('file2.jpg')

    reply_markup = ReplyKeyboardRemove()
    await context.bot.send_document(chat_id=update.effective_chat.id, document=file_id,
                                    reply_markup=reply_markup)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Received both documents!")

    # Clear user_data for the next conversation
    context.user_data.clear()

    return ConversationHandler.END


if __name__ == '__main__':
    token = dotenv_values('.env')['BOT_TOKEN']

    application = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_METHOD: [MessageHandler(filters.TEXT, choose_method)],
            SEND_FIRST_DOCUMENT: [MessageHandler(filters.ATTACHMENT, send_first_document)],
            SEND_SECOND_DOCUMENT: [MessageHandler(filters.ATTACHMENT, send_second_document)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)

    application.run_polling()
