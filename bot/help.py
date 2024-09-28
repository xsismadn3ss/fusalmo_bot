from bot.bot_data import bot
from bot.fx.check_login import login_required

@bot.message_handler(commands=["help"])
@login_required
async def help(message):
    chatid = message.chat.id
    
    information = """
\nFUSALMO BOT 🚀🌱🌦️\n
Command list
/status - current humidity and temperature
/sign_in - sign in to have all access
/t_report - load temperature chart
/h_report - load humidity chart
/reports - get all reports

Information contact:
→ @xs_ismadn3ss
"""

    await bot.send_message(chatid, information)