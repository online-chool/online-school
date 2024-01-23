from django.conf import settings

from telegram import Update, Bot


def bot():
    return Bot(token=settings.TELEGRAM_TOKEN)