from bot.fx.check_login import login_required
from bot.fx.handle_reports import (
    humidity_report,
    send_h_report,
    send_t_report,
    temperature_report,
)
from data import humidity_queries, temperature_queries
from .bot_data import bot


@bot.message_handler(commands=["reports"])
@login_required
async def reports(message):
    chatid = message.chat.id
    h_data = await humidity_queries.get_from_today()
    t_data = await temperature_queries.get_from_today()

    if h_data is not None:
        h_chart, max_h, min_h = await humidity_report(h_data=h_data)
        await send_h_report(chat_id=chatid, h_chart=h_chart, min_h=min_h, max_h=max_h)

    if t_data is not None:
        t_chart, max_t, min_t = await temperature_report(t_data=t_data)
        await send_t_report(chat_id=chatid, t_chart=t_chart, max_t=max_t, min_t=min_t)

    else:
        await bot.send_message(
            message.chat.id, "No se pudo crear la grafica, intenta de nuevo"
        )


@bot.message_handler(commands=["t_report"])
@login_required
async def t_reports(message):
    chatid = message.chat.id
    t_data = await temperature_queries.get_from_today()

    if t_data is not None:
        t_chart, max_t, min_t = await temperature_report(t_data=t_data)
        await send_t_report(chat_id=chatid, t_chart=t_chart, max_t=max_t, min_t=min_t)

    else:
        await bot.send_message(
            message.chat.id, "No se pudo crear la grafica, intenta de nuevo"
        )


@bot.message_handler(commands=["h_report"])
@login_required
async def h_reports(message):
    chatid = message.chat.id
    h_data = await humidity_queries.get_from_today()

    if h_data is not None:
        h_chart, max_h, min_h = await humidity_report(h_data=h_data)
        await send_h_report(chat_id=chatid, h_chart=h_chart, max_h=max_h, min_h=min_h)

    else:
        await bot.send_message(
            message.chat.id, "No se pudo crear la grafica, intenta de nuevo"
        )
