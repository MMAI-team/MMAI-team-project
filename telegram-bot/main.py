import logging

from dotenv import dotenv_values
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)


from models import (
    DummyModel,
    PathModel,
)
from bot_methods import (
    BotMethods,
    CHOOSING_METHOD,
    SEND_FIRST_DOCUMENT,
    SEND_SECOND_DOCUMENT,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    env_values = dotenv_values(".env")

    token = env_values["BOT_TOKEN"]
    model_path = env_values["MODEL_PATH"]

    model = PathModel(model_path, "CNN model")

    application = ApplicationBuilder().token(token).build()

    models = [DummyModel("Method 1", 1), model]

    bot_methods = BotMethods(models)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", bot_methods.start)],
        states={
            CHOOSING_METHOD: [MessageHandler(filters.TEXT, bot_methods.choose_method)],
            SEND_FIRST_DOCUMENT: [
                MessageHandler(filters.ATTACHMENT, bot_methods.send_first_document)
            ],
            SEND_SECOND_DOCUMENT: [
                MessageHandler(filters.ATTACHMENT, bot_methods.send_second_document)
            ],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    application.run_polling()
