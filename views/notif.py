
from telegram import Bot
from telegram.parsemode import ParseMode
import datetime  as dt

# pip install python-telegram-bot --upgrade
# from telegram import Bot
# from telegram.parsemode import ParseMode
# import datetime  as dt

def telegram_notif_gmkt(user_name, message, activity_dt = dt.datetime.now()):
    
    # initializing the bot with API
    bot = Bot("1215887198:AAFlRV9fiZUqi3fK1yisue7KvpWRWiwlB50")

    # getting the bot details
    # print(bot.get_me())

    # Reporting Channel
    my_cat_id = '-1001213465234'

    message = """<strong style="color:red;">Capillarité OM app | {0}</strong>\n {1} {2}""".format(user_name, message, activity_dt.strftime("%Y-%m-%d %H:%M:%S"))

    bot.send_message(chat_id=my_cat_id,text=message,parse_mode=ParseMode.HTML)

    return None

# telegram_notif_gmkt(user_name = "sanirou",message = "Cet utilisisateur s'est connecté à l'application à")



#--------------------------------------------------------------------------------------------
    