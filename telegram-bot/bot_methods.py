import base64
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from PIL import Image
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackContext,
)

CHOOSING_METHOD, SEND_FIRST_DOCUMENT, SEND_SECOND_DOCUMENT = range(3)


class BotMethods:
    def __init__(self, models, sender):
        self.models = models
        self.methods = [model["name"] for model in models]
        self.reply_keyboard = ReplyKeyboardMarkup(
            [self.methods], one_time_keyboard=True
        )
        self.user_to_model = {}

        self.sender = sender

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Let's begin!\nChoose a method:",
            reply_markup=self.reply_keyboard,
        )
        return CHOOSING_METHOD

    async def choose_method(self, update: Update, context: CallbackContext):
        user_id = update.effective_chat.id

        method_choice = update.message.text
        self.user_to_model[user_id] = self.methods.index(method_choice)

        reply_markup = ReplyKeyboardRemove()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"You chose {method_choice}.\nNow, send the first photo.",
            reply_markup=reply_markup,
        )
        return SEND_FIRST_DOCUMENT

    async def send_first_document(self, update: Update, context: CallbackContext):
        user_id = update.effective_chat.id
        file_path = f"{user_id}-1.jpg"

        if update.message.document is not None:
            file_id = update.message.document.file_id
            new_file = await context.bot.get_file(file_id)
            await new_file.download_to_drive(file_path)

        elif update.message.photo is not None:
            file_id = update.message.photo[-1].file_id
            new_file = await context.bot.get_file(file_id)
            await new_file.download_to_drive(file_path)

        reply_markup = ReplyKeyboardRemove()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="First document received.\nNow, send the second photo.",
            reply_markup=reply_markup,
        )
        return SEND_SECOND_DOCUMENT

    async def send_second_document(self, update: Update, context: CallbackContext):
        user_id = update.effective_chat.id
        file_path = f"{user_id}-2.jpg"

        if update.message.document is not None:
            file_id = update.message.document.file_id
            new_file = await context.bot.get_file(file_id)
            await new_file.download_to_drive(file_path)

        elif update.message.photo is not None:
            file_id = update.message.photo[-1].file_id
            new_file = await context.bot.get_file(file_id)
            await new_file.download_to_drive(file_path)

        reply_markup = ReplyKeyboardRemove()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Received both documents!",
            reply_markup=reply_markup,
        )

        # model = self.models[self.user_to_model[user_id]]

        photos = [f"{user_id}-1.jpg", f"{user_id}-2.jpg"]

        # open the images as regular files
        images = [open(photo, "rb") for photo in photos]
        # encode using base64
        images = [base64.b64encode(image.read()).decode("utf-8")
                  for image in images]

        # send the images to the API
        try:
            result = self.sender.predict(images)
        except Exception as e:
            result = f"Error: {e}"

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Result: {result}",
        )

        context.user_data.clear()

        return ConversationHandler.END
