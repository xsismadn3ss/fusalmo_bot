import json
from bot.bot_data import bot
from bot.fx.handle_reports import (
    humidity_report,
    send_h_report,
    send_t_report,
    temperature_report,
)
from data.models import User
from data import humidity_queries, temperature_queries, user_queries
from datetime import datetime, time

from raspberry.load_config import load_config


async def status_state(state: bool, key: str) -> None:
    "Update reports sent status"
    config_path = "raspi_config.json"

    with open(config_path, "r") as f:
        data = json.load(f)

    data["status"][key] = state
    with open(config_path, "w") as f:
        json.dump(data, f, indent=4)


async def check_conditions(h: float, t: float):
    """Cheack tempereture and humidity conditions"""
    data = await load_config()
    status = data["status"]["alert_sent"]
    print("checking conditions...")

    if h >= 30 and t <= 22 and status == False:
        users: list[User] = await user_queries.get_all()
        for user in users:
            await bot.send_message(
                user.chat_id,
                f"Humedad: {h}%\nTemperatura: {t}° C\nEl clima en este momento esta helado.",
            )

    elif h > 50 and t <= 28 and status == False:  # humedad alta
        users: list[User] = await user_queries.get_all()
        for user in users:
            await bot.send_message(
                user.chat_id,
                "El nivel de humedad esta demesaiado alto",
            )

    elif h > 50 and t > 28 and status == False:
        users: list[User] = await user_queries.get_all()
        for user in users:
            await bot.send_message(
                user.chat_id,
                f"Humedad: {h}%\nTemperatura: {t}° C\nEs posible que tengas una sensación térmica mayor a la temperatura ambiente debido al exceso de humedad",
            )

    await status_state(True, "alert_sent")
    print("alert sent")
    return True


async def send_reports():
    # load data
    h_data = await humidity_queries.get_from_today()
    t_data = await temperature_queries.get_from_today()

    # create reports
    h_chart, max_h, min_h = await humidity_report(h_data=h_data)
    t_chart, max_t, min_t = await temperature_report(t_data=t_data)

    # load user
    users: list[User] = await user_queries.get_all()

    # send reports
    for user in users:
        await send_h_report(chat_id=user.chat_id, h_chart=h_chart, min_h=min_h, max_h=max_h)
        await bot.send_message(user.chat_id, "---------------")
        await send_t_report(chat_id=user.chat_id, t_chart=t_chart, max_t=max_t, min_t=min_t)


async def generateReports(time: datetime):
    """send reports tu users automatically"""
    data = await load_config()
    status = data["status"]["reports_sent"]

    if time.hour >= 3 and time.hour <= 5 and status == False:
        await send_reports()
        await status_state(True, "reports_sent")

    elif time.hour >= 11 and time.hour <= 14 and status == False:
        await send_reports()
        await status_state(True, "reports_sent")

    elif (time.hour > 5 and time.hour < 11) or (time.hour > 14 and time.hour < 3):
        await status_state(False, "reports_sent")
