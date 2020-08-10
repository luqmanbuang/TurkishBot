import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from googletrans import Translator
import threading
from gtts import gTTS


# Create updater object
updater = Updater(
    token='API TOKEN', use_context=True)
dispatcher = updater.dispatcher

# logging module, so you will know when (and why) things don't work as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# initialize src and dest
src = None
dest = None


#  ------------------------------- vv Handlers vv ------------------------------ #

# 1 /start; Function called every time the Bot receives a Telegram message that contains the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to Luqman's testing ground! :)\nInput /help for the list of commands")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# 2 /help; Returns a list of commands that can be used in the bot
def help_input(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='List of commands that you can use in this bot!\n\n/start - Start the bot \n/ETT - Activate English to Turkish Translation \n/TTE - Activate Turkish to English Translation', )


help_handler = CommandHandler('help', help_input)
dispatcher.add_handler(help_handler)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TTE
def TTE(update, context):
    global src, dest
    src = 'tr'
    dest = 'en'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Turkish to English translation activated")


TTE_handler = CommandHandler('TTE', TTE)
dispatcher.add_handler(TTE_handler)

# ETT


def ETT(update, context):
    global src, dest
    src = 'en'
    dest = 'tr'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="English to Turkish translation activated")


ETT_handler = CommandHandler('ETT', ETT)
dispatcher.add_handler(ETT_handler)

# 3 Translates messages


def translate(update, context):
    trans = Translator()
    sentence = update.message.text
    if src:
        # Word or sentence translation
        translation = trans.translate(text=sentence, src=src, dest=dest)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Translation:\n{translation.text}")

        # Returns audio file of the pronunciation
        output = gTTS(text=translation.text, lang=dest, slow=False)
        output.save("output.mp3")
        context.bot.send_voice(
            chat_id=update.effective_chat.id, voice=open('output.mp3', 'rb'))
    else:
        return


echo_handler = MessageHandler(Filters.text & (~Filters.command), translate)
dispatcher.add_handler(echo_handler)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# 6 /stop1234; stops server
def shutdown():
    updater.stop()
    updater.is_idle = False


def stop(bot, update):
    threading.Thread(target=shutdown).start()


stop_handler = CommandHandler('stop1234', stop)
dispatcher.add_handler(stop_handler)


# 7 unknown command error; Returns error when invalid command is input
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Invalid command, please use /help for the list of commands")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#  ------------------------------- ^^ Handlers ^^ ------------------------------ #


updater.start_polling()
updater.idle

