import logging
import os

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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if __name__ == "__main__":
    dotenv.load_dotenv()

    token = os.environ.get("BOT_TOKEN")

    application = ApplicationBuilder().token(token).build()

    # TODO: pass address and endpoint using env variables
    api_sender = APISender("http://localhost:5000", "predict")

    models = api_sender.get_models()

    bot_methods = BotMethods(models, api_sender)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", bot_methods.start)],
        states={
            CHOOSING_METHOD: [MessageHandler(filters.TEXT,
                                             bot_methods.choose_method)],
            SEND_FIRST_DOCUMENT: [
                MessageHandler(
                    filters.ATTACHMENT | filters.PHOTO,
                    bot_methods.send_first_document
                )
            ],
            SEND_SECOND_DOCUMENT: [
                MessageHandler(
                    filters.ATTACHMENT | filters.PHOTO,
                    bot_methods.send_second_document
                )
            ],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    application.run_polling()
