"""Greek Cases Telegram Mini App launcher.

Bot does one thing: shows a button that opens the web app.
All logic lives in the deployed index.html.

Run:
  BOT_TOKEN=<token> WEB_APP_URL=<https-url> python bot.py
"""

import logging
import os

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    WebAppInfo,
)
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

WEB_APP_URL = os.environ.get("WEB_APP_URL", "")


def launch_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "🇬🇷 Открыть тренажёр",
            web_app=WebAppInfo(url=WEB_APP_URL),
        )
    ]])


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 <b>Καλώς ήρθες!</b>\n\n"
        "Тренажёр греческих падежей.\n"
        "53 упражнения на артикли · 100 на окончания.\n\n"
        "Нажми кнопку, чтобы открыть:",
        reply_markup=launch_keyboard(),
        parse_mode=ParseMode.HTML,
    )


async def cmd_play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Открыть тренажёр:",
        reply_markup=launch_keyboard(),
    )


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("Set BOT_TOKEN env var (get from @BotFather)")
    if not WEB_APP_URL or not WEB_APP_URL.startswith("https://"):
        raise RuntimeError("Set WEB_APP_URL env var to HTTPS URL of deployed index.html")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("play", cmd_play))
    logger.info("Bot starting. WEB_APP_URL=%s", WEB_APP_URL)
    app.run_polling()


if __name__ == "__main__":
    main()
