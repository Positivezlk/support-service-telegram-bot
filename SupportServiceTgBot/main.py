# Import the telebot library
import telebot

# Initialize the telebot with the API token
bot = telebot.TeleBot('Your_API_token')

# Define user_id and admin_id
user_id = 0
admin_id = 1234567890  # The administrator's ID should be located here


# Handler of the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create an inline keyboard with a button
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton('Report a problem', callback_data='user_question')
    markup.add(button)
    # Send a welcome message with the inline keyboard
    bot.send_message(message.chat.id, f'<b>Hello!</b> I am a service support bot "your service name"',
                     reply_markup=markup, parse_mode='HTML')


# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'user_question':
        # Prompt the user to describe the problem
        bot.send_message(call.message.chat.id, 'Describe your problem to me')
        bot.register_next_step_handler(call.message, user_question)
    elif call.data == 'reply_to_user':
        # Prompt the admin to enter the user ID and message separated by a space
        bot.send_message(call.message.chat.id, 'Enter the user <b>ID</b> and message separated by a space',
                         parse_mode='HTML')
        bot.register_next_step_handler(call.message, admin_answer)


# Function to handle the user's question
def user_question(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton('Reply to the user', callback_data='reply_to_user')
    markup.add(button)
    # Save the user's ID
    global user_id
    user_id = message.chat.id
    user_text = message.text
    # Send a confirmation message to the user and forward the message to the admin
    bot.send_message(message.chat.id, 'Your message has been sent to the administrator. <b>Thanks!</b>',
                     parse_mode='HTML')
    bot.send_message(admin_id, f'Message from ID <code>{user_id}</code>:\n\n<b>{user_text}</b>',
                     reply_markup=markup, parse_mode='HTML')


# Function to handle the admin's response
def admin_answer(message):
    try:
        user_idd, admin_answerr = message.text.split(' ', 1)
        # Send a confirmation message to the admin and forward the message to the user
        bot.send_message(message.chat.id, 'The message has been sent to the user!')
        bot.send_message(user_idd, f'Message from the administrator:\n\n<b>{admin_answerr}</b>', parse_mode='HTML')
    except ValueError:
        # If the administrator entered the ID and message incorrectly
        bot.send_message(admin_id, '<b>Incorrect input</b>. '
                                   'Click the button again and enter the user ID and message separated by a space',
                         parse_mode='HTML')


# Start the bot, constantly polling for updates
bot.polling(none_stop=True)
