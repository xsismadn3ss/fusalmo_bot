from bot.bot_data import bot
from bot.fx.check_login import login_required

@bot.message_handler(commands=["help"])
@login_required
async def help(message):
    chatid = message.chat.id
    
    information = """
\nFUSALMO BOT 🚀🌱🌦️\n
Command list
/status - get current humidity and temperature
/sign_in - sign in to have all access
/t_report - get temperature chart from latest data
/h_report - get humidity chart from latest data
/reports - get all reports

Information contact:
→ @xs_ismadn3ss
"""

    await bot.send_message(chatid, information)