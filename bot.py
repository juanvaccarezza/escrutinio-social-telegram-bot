from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from optparse import OptionParser
from telegram import ReplyKeyboardMarkup, KeyboardButton



def start(bot, update):
    reply_keyboard = [[KeyboardButton(text="Yes", request_contact=True), KeyboardButton(text="No")]
                                ]
    update.message.reply_text(
        'Hola {} ¿podemos usar tu número de teléfono para saber quien sos?'.format(update.message.from_user.first_name),reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
def text(bot, update, user_data):
    print(update.message.text)
    print(user_data)

def contact(bot, update):
    print(update)

def parse_cmd():
    parser = OptionParser()
    parser.add_option("-t", "--token", help="Bot api token", action="store", type="string",  dest="token")

    (options, args) = parser.parse_args()
    if options.token is None:
        parser.print_help()
        exit(1)

    return options

if __name__ == '__main__':

    options = parse_cmd()
    updater = Updater(options.token)
    

    
    contact_handler = MessageHandler(Filters.contact, contact)
    updater.dispatcher.add_handler(contact_handler)

    updater.dispatcher.add_handler(CommandHandler('start', start))

    text_handler = MessageHandler(Filters.text, text, pass_user_data=True)
    updater.dispatcher.add_handler(text_handler)
    
    updater.start_polling()
    updater.idle()
