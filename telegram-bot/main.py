import logging
import os
from turtle import end_fill

from dotenv import dotenv_values
import dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

from bot_methods import (
    BotMethods,
    CHOOSING_METHOD,
    SEND_FIRST_DOCUMENT,
    SEND_SECOND_DOCUMENT,
)
from api_sender import APISender
from models import PathModel, APIModel

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    dotenv.load_dotenv()

    model_path = os.environ.get("MODEL_PATH")
    token = os.environ.get("BOT_TOKEN")
    address = os.environ.get("ENDPOINT")

    application = ApplicationBuilder().token(token).build()

    api_sender = APISender(address)

    models = [
        PathModel(model_path, "CNN ResNet152"),
        APIModel(api_sender, "sift", "API Model — SIFT"),
    ]

    bot_methods = BotMethods(models)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", bot_methods.start)],
        states={
            CHOOSING_METHOD: [MessageHandler(filters.TEXT, bot_methods.choose_method)],
            SEND_FIRST_DOCUMENT: [
                MessageHandler(
                    filters.ATTACHMENT | filters.PHOTO, bot_methods.send_first_document
                )
            ],
            SEND_SECOND_DOCUMENT: [
                MessageHandler(
                    filters.ATTACHMENT | filters.PHOTO, bot_methods.send_second_document
                )
            ],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    application.run_polling()
