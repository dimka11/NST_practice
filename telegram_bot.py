import telebot  # TestTG11_bot
import glob
import os

from nst import make_style_transfer

from tg_bot_utils import clean_folder, pre_start_work
clean_folder()
pre_start_work()


class LocalState:
    content_blending_ratio = {}


APIKEY = os.environ['APIKEY']
bot = telebot.TeleBot(APIKEY, parse_mode=None)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,
                 f"Upload two images (content first and style second) for mix ratio: /content_blending_ratio 0..1")


@bot.message_handler(commands=['content_blending_ratio'])
def send_welcome(message):
    if len(message.text) != 0:
        chat_id = message.chat.id
        ls.content_blending_ratio[chat_id] = float(message.text.split(' ')[-1])
        bot.reply_to(message, f"content blending ratio was set")
    else:
        "message text is zero"


@bot.message_handler(content_types=['document', 'photo'])
def handle_docs_photo(message):
    # https://stackoverflow.com/questions/31096358/how-do-i-download-a-file-or-photo-that-was-sent-to-my-telegram-bot
    print(message)
    chat_id = message.chat.id
    chat_id_str = str(chat_id)
    print(chat_id)

    if not os.path.isdir(f'./pics/{chat_id}'):
        os.mkdir(f'./pics/{chat_id}')

    if os.path.exists(f'./pics/{chat_id}/final_image.jpg'):
        for file in glob.glob(f'./pics/{chat_id}/*'):
            os.remove(file)

    raw = message.photo[2].file_id
    if len([item for item in os.listdir(f'./pics/{chat_id}') if not item.startswith('.')]) == 0:
        path = 'content' + ".jpg"
    else:
        path = 'style' + ".jpg"

    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'./pics/{chat_id}/' + path, 'wb') as new_file:
        new_file.write(downloaded_file)

    if len([item for item in os.listdir(f'./pics/{chat_id}') if not item.startswith('.')]) > 1:
        # run model
        bot.reply_to(message, "waiting...")

        if not chat_id in ls.content_blending_ratio:
            ls.content_blending_ratio[chat_id] = 0.75

        make_style_transfer(f'./pics/{chat_id}/content.jpg', f'./pics/{chat_id}/style.jpg',
                            ls.content_blending_ratio[chat_id], path_save_final_img=f'./pics/{chat_id}/final_image.jpg')

        # upload photo
        final_image = open(f'./pics/{chat_id}/final_image.jpg', 'rb')
        bot.reply_to(message, "Done")
        bot.send_photo(chat_id, final_image)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "Use /help command")


if __name__ == '__main__':
    ls = LocalState()
    bot.infinity_polling()
    clean_folder()
