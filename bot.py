from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler)
from optparse import OptionParser
from telegram import ReplyKeyboardMarkup, KeyboardButton
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    reply_keyboard = [[KeyboardButton(text="Yes", request_contact=True), KeyboardButton(text="No")]
                                ]
    update.message.reply_text(
        'Hola {} ¿podemos usar tu número de teléfono para saber quien sos?'.format(update.message.from_user.first_name),reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


type_keyboard = [['Mesa', 'Telegrama', 'Certificado', 'Copia de acta de fiscal']]
type_markup = ReplyKeyboardMarkup(type_keyboard, one_time_keyboard=True)


TIPO, NUMERO_DE_MESA, CIRCUITO, SECCION_ELECTORAL, TODO_CARGADO, CONFIRMACION = range(6)

def user_data_to_str(user_data):
    user_data_list = list()

    for key, value in user_data.items():
        user_data_list.append('{} - {}'.format(key, value))

    return "\n".join(user_data_list).join(['\n', '\n'])



def acta(bot, update):
    update.message.reply_text(
        '¿Qué tipo de acta querés cargar?',
        reply_markup=type_markup)
    return TIPO

def mesa(bot, update, user_data):
    user_data['tipo'] = update.message.text
    update.message.reply_text(
        '¿De que número de mesa es?')
    return NUMERO_DE_MESA

def circuito(bot, update, user_data):
    user_data['numero_de_mesa'] = update.message.text
    update.message.reply_text(
        '¿De que curcuito es?')
    return CIRCUITO

def seccion(bot, update, user_data):
    user_data['circuito'] = update.message.text
    update.message.reply_text(
        '¿De que sección es?')
    return SECCION_ELECTORAL

def imagen(bot, update, user_data):
    user_data['seccion'] = update.message.text
    update.message.reply_text(
        'Por favor enviá la imágen')
    return TODO_CARGADO

def confirmation(bot, update, user_data):
    response = user_data_to_str(user_data)
    update.message.reply_text(
        'Confirmás que los datos son correctos '+ response)
    return CONFIRMACION


def contact(bot, update):
    print(update)

def end(bot, update, user_data):
    response = user_data_to_str(user_data)
    update.message.reply_text(
        'Gracias '+ response)
    
def thanks(bot, update,):
    update.message.reply_text(
        'Gracias ')


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
    

    
    #contact_handler = MessageHandler(Filters.contact, contact)
    #updater.dispatcher.add_handler(contact_handler)

    updater.dispatcher.add_handler(CommandHandler('start', start))

    #text_handler = MessageHandler(Filters.text, text, pass_user_data=True)
    #updater.dispatcher.add_handler(text_handler)


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('acta', acta)],

        states={
            TIPO: [RegexHandler('^(Mesa|Telegrama|Certificado|Copia de acta de fiscal)$',
                                    mesa,
                                    pass_user_data=True),
                       MessageHandler(Filters.text,
                                    end,
                                    pass_user_data=True),
                       ],

            NUMERO_DE_MESA: [MessageHandler(Filters.text,
                                           circuito,
                                           pass_user_data=True),
                            ],

            CIRCUITO: [MessageHandler(Filters.text,
                                          seccion,
                                          pass_user_data=True),
                           ],
            SECCION_ELECTORAL: [MessageHandler(Filters.text,
                                          imagen,
                                          pass_user_data=True),
                           ],
            TODO_CARGADO: [MessageHandler(Filters.text,
                                          confirmation,
                                          pass_user_data=True),
                           ],
            CONFIRMACION: [MessageHandler(Filters.text,
                                          thanks),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', end, pass_user_data=True)]
    )
    updater.dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()
