import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6439029069:AAG34OOQDTouXDNeeUG1JwxX4vqXYYXvh8c')

# Define a function to handle incoming messages
@bot.message_handler(content_types=['text'])
def handle_message(message):
    # Check if the message is from a group chat (chat type is 'group')
    if message.chat.type:
        chat_id = message.chat.id
        user_id = message.from_user.id
        username = message.from_user.username
        text = message.text.lower()  # Convert message text to lowercase
        print (text)

        # Check if the lowercase message text is 'start'
        if text == 'start':
            # Reply to the message
            bot.send_message(chat_id, f"Hello, {username}! You sent 'start'.")

# Start the bot
bot.polling()

