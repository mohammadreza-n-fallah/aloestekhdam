import telebot
from random import randint

API_TOKEN = '6439029069:AAG34OOQDTouXDNeeUG1JwxX4vqXYYXvh8c'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def send_koni(message):
    if 'کو' in message.text or message.text == 'کانی':
        random_koni = randint(1,10)
        if message.from_user.id == 6531030681:
                bot.reply_to(message, f'{message.from_user.first_name}\n تو یه کونی نیستی.')
        else:
            if random_koni % 2 == 0:
                bot.reply_to(message, f'{message.from_user.first_name}\n تو یه کونی نیستی.')
            else:
                with open('koni.mp4', 'rb') as gif_file:
                    bot.send_animation(message.chat.id, gif_file)        


bot.polling()
