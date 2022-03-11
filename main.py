from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import socket
import re
import os


token = os.getenv('TELEGRAM') #token from telegram, hidden in env
updater = Updater(token,
                  use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to Server Checker! type /help for more details")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /check - To check the server availibility
    /summary - To check the summary of how many servers are working
    """)

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)
  
def is_running(site, port, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #the AF_INET and SOCK_Stream are the default values, it can be left empty
        sock.connect((site, port))
        return True
    except:
        return False

def check(update: Update, context: CallbackContext):
    SERVER=[]
    PORT=22 #which port you want to connect to
    CONNTIMEOUT=5 #Connection timeout in sec, because the default is none and will hang if not set
    SITEOK=0
    TOTALSITE=0
    currentDir=os.getcwd()
    output=""

    with open(currentDir + '/serverlist.txt', 'r') as serverlist:
        for line in serverlist:
            line=re.sub(r'\n','',line) #removing the \n from the list
            SERVER.append(line)

    for site in SERVER:
        try:
            if is_running(site, PORT, CONNTIMEOUT):
                output=output+str(f'{site} is running!\n')
                SITEOK+=1
            else:
                output=output+str(f'There is NO response for server {site}\n')
        except:
            output=output+str('something went terribly wrong with the function\n')
        finally:
            TOTALSITE+=1

    update.message.reply_text(    
        f'{output}SUMMARY (OK/NOK): ' + str(SITEOK) + '/' + str(TOTALSITE))

def summary(update: Update, context: CallbackContext):
    SERVER=[]
    PORT=22 #which port you want to connect to
    CONNTIMEOUT=5 #Connection timeout in sec, because the default is none and will hang if not set
    SITEOK=0
    TOTALSITE=0
    currentDir=os.getcwd()
    output=""

    with open(currentDir + '/serverlist.txt', 'r') as serverlist:
        for line in serverlist:
            line=re.sub(r'\n','',line) #removing the \n from the list
            SERVER.append(line)

    for site in SERVER:
        try:
            if is_running(site, PORT, CONNTIMEOUT):
                SITEOK+=1
            else:
                pass
        except:
            output=output+str('something went terribly wrong with the function\n')
        finally:
            TOTALSITE+=1

    update.message.reply_text(    
        f'{output}SUMMARY (OK/NOK): ' + str(SITEOK) + '/' + str(TOTALSITE))


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('check', check))
updater.dispatcher.add_handler(CommandHandler('summary', summary))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # Filters out unknown commands

updater.start_polling()
