from telegram.ext import Updater, CommandHandler
from optparse import OptionParser


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


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

    updater.dispatcher.add_handler(CommandHandler('acta', hello))

    updater.start_polling()
    updater.idle()
