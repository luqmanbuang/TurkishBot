import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
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
src = 'en'
dest = 'tr'

# initialize voice toggle
voice_toggle = True
voicemode = "ON" 

#  ------------------------------- vv Handlers vv ------------------------------ #


# 1 /start; Function called every time the Bot receives a Telegram message that contains the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to Luqman's testing ground! :)\n\nTo select or change translation mode input /change!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# 2 /help; Returns a list of commands that can be used in the bot
def help_input(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='To change translation language input /change')


help_handler = CommandHandler('help', help_input)
dispatcher.add_handler(help_handler)


# 3 /change; Change translation language
def change(update, context):
    keyboard = [[InlineKeyboardButton("Turkish to English", callback_data='1'), InlineKeyboardButton("English to Turkish", callback_data='2')],
    [InlineKeyboardButton(text="Voice Toggle ON/OFF", callback_data="vtoggle")],
    [InlineKeyboardButton(text="Check out the source code on Github!", url="https://github.com/luqmanbuang/TurkishBot")]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    if src == 'tr':
        langmode = 'Turkish to English'
    else:
        langmode = "English to Turkish"

    update.message.reply_text(f'Current mode: {langmode}\nVoice toggle = {voicemode}', reply_markup=reply_markup)


change_handler = CommandHandler('change', change)
dispatcher.add_handler(change_handler)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    # calls appropriate function based on selected translation mode 
    if query.data == '1':
        TTE(update, context)
    elif query.data == '2':
        ETT(update, context)
    elif query.data == 'vtoggle':
        VoiceToggle(update, context)


dispatcher.add_handler(CallbackQueryHandler(button))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TTE
def TTE(update, context):
    global src, dest
    src = 'tr'
    dest = 'en'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Turkish to English translation activated")


# ETT
def ETT(update, context):
    global src, dest
    src = 'en'
    dest = 'tr'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="English to Turkish translation activated")


# Voice toggle
def VoiceToggle(update, context):
    global voice_toggle, voicemode
    voice_toggle = not voice_toggle

    if voice_toggle:
        voicemode = "ON"
    else:
        voicemode = "OFF"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Voice mode is {voicemode}")


# Voice translation, Returns audio file of the pronunciation
def VoiceTranslate(update, context, sentence):
    # 
    output = gTTS(text=sentence, lang=dest, slow=False)
    output.save("output.mp3")
    context.bot.send_voice(chat_id=update.effective_chat.id, voice=open('output.mp3', 'rb'))




# 3 Translates messages
def translate(update, context):
    trans = Translator()
    sentence = update.message.text
    if src:
        # Word or sentence translation
        translation = trans.translate(text=sentence, src=src, dest=dest)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Translation:\n{translation.text}")

        if voice_toggle:
            VoiceTranslate(update, context, translation.text)

    else:
        return


echo_handler = MessageHandler(Filters.text & (~Filters.command), translate)
dispatcher.add_handler(echo_handler)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# 4 /stop; stops server
def shutdown():
    updater.stop()
    updater.is_idle = False


def stop(bot, update):
    threading.Thread(target=shutdown).start()


stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)


# 5 unknown command error; Returns error when invalid command is input
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Invalid command, please use /change to change the translation mode!")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#  ------------------------------- ^^ Handlers ^^ ------------------------------ #


updater.start_polling()
updater.idle
