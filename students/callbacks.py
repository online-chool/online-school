from .random_core import generate_random_digit_code

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from django.core.cache import cache

from .serializers import StudentSerializer


def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton(text="Send contact", request_contact=True)]
    ]

    update.message.reply_text(
        text="Hello, I'm a bot! Please, send me your contact.", 
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

def register(update: Update, context: CallbackContext):
    # get user
    user = update.effective_user

    # get contact
    contact = update.message.contact

    # collect data
    phone = contact.phone_number
    telegram_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username

    # validate data
    data = {
        'phone_number': f"+{phone}",
        'telegram_id': telegram_id,
        'first_name': first_name,
    }
    if last_name:
        data['last_name'] = last_name
    if username:
        data['username'] = username

    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        # save student
        serializer.save()

        # send message
        update.message.reply_text(
            text="You have successfully registered!"
        )
    else:
        # send message with errors
        update.message.reply_text(
            text=f"Your Contact is not valid!"
        )

def send_code(update: Update, context: CallbackContext):
    # get user
    user = update.effective_user

    # generate code
    code = generate_random_digit_code()

    # check before cache
    if cache.get(f"code:{user.id}"):
        cache.delete(f"code:{user.id}")

    # save code to cache
    cache.set(f"code:{user.id}", code, timeout=60)

    # send message
    update.message.reply_markdown_v2(
        text=f"Your code is: `{code}`"
    )
