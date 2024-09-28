from bot.bot_data import bot
from bot.fx.check_login import login_required

@bot.message_handler(commands=["help"])
@login_required
async def help(message):
    chatid = message.chat.id
    
    information = """ FUSALMO BOT 🤖🌱🌦️\n
    Command list\n
    /status - get current humidity and temperature\n
    /sign_in - sign in to have all access\n
    /t_report - get temperature chart from latest data\n
    /h_report - get humidity chart from latest data\n
    /reports - get all reports

    Information contact:
    → @xs_ismadn3ss
    """

    await bot.send_message(chatid, information)