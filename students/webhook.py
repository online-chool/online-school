from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from .bot import bot
from .callbacks import start, register, send_code

bot = bot()

@api_view(['POST'])
@csrf_exempt
def webhook(request: Request) -> Response:
    # get update from request
    update = Update.de_json(request.data, bot)

    # create dispatcher
    dispatcher = Dispatcher(bot, None, workers=0)

    # command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('login', send_code))

    # message handlers
    dispatcher.add_handler(MessageHandler(Filters.contact, register))
    
    # process update
    dispatcher.process_update(update)

    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def set_webhook(request: Request) -> Response:
    if bot.set_webhook(url=settings.TELEGRAM_WEBHOOK_URL):
        return Response(status=200)
    else:
        return Response(status=500)
    