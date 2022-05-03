import telebot
import os


class MyClass:
    APIKEY = os.environ['APIKEY']
    bot = telebot.TeleBot(APIKEY, parse_mode=None)
    def __init__(self):
        pass

    @bot.message_handler(commands=['help'])
    def send_welcome(self, message):
        self.bot.reply_to(message,
                     f"Upload two images (content first and style second) for mix ratio: /content_blending_ratio 0..1")