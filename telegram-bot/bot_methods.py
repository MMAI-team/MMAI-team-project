from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackContext,
)

CHOOSING_METHOD, SEND_FIRST_DOCUMENT, SEND_SECOND_DOCUMENT = range(3)


class BotMethods:
    def __init__(self, models):
        self.models = models
        self.methods = [model.name for model in models]
        self.reply_keyboard = ReplyKeyboardMarkup(
            [self.methods], one_time_keyboard=True
        )
        self.model_index = 0

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm a bot, please talk to me!\nChoose a method:",
            reply_markup=self.reply_keyboard,
        )
        return CHOOSING_METHOD

    async def choose_method(self, update: Update, context: CallbackContext):
        method_choice = update.message.text
        context.user_data["method"] = method_choice
        self.model_index = self.methods.index(method_choice)

        reply_markup = ReplyKeyboardRemove()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"You chose {method_choice}.\nNow, send the first document.",
            reply_markup=reply_markup,
        )
        return SEND_FIRST_DOCUMENT

    async def send_first_document(self, update: Update, context: CallbackContext):
        file_id = update.message.document.file_id

        # open file using opencv
        new_file = await context.bot.get_file(file_id)
        await new_file.download_to_drive("file1.jpg")

        reply_markup = ReplyKeyboardRemove()
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file_id,
            reply_markup=reply_markup,
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="First document received.\nNow, send the second document.",
        )
        return SEND_SECOND_DOCUMENT

    async def send_second_document(self, update: Update, context: CallbackContext):
        file_id = update.message.document.file_id

        # open file using opencv
        new_file = await context.bot.get_file(file_id)
        await new_file.download_to_drive("file2.jpg")

        reply_markup = ReplyKeyboardRemove()
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file_id,
            reply_markup=reply_markup,
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Received both documents!"
        )

        model = self.models[self.model_index]

        # TODO: get result from model using the two files
        result = model.predict(["file1.jpg", "file2.jpg"])

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Result: {result}"
        )

        # Clear user_data for the next conversation
        context.user_data.clear()

        return ConversationHandler.END
