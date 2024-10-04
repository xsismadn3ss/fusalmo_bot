import asyncio
from datetime import datetime
from bot.bot_data import bot
from bot import *
from bot.help import help
from raspberry.read import read_dht
from raspberry.handle_data import save_data
from raspberry.events import check_conditions, generateReports, status_state


async def raspberry():
    print("Leyendo sensores...")
    i = 0
    h_list = []
    t_list = []
    while True:
        try:
            h, t = await read_dht()
            t_list.append(t)
            h_list.append(h)
            if i == 10:
                h_list, t_list, i = await save_data(h_list, t_list, i)

        except Exception as e:
            print(e)
            break
        i += 1


async def reports():
    current_time = datetime.now()
    await generateReports(current_time)
    await asyncio.sleep(5)
    await reports()

async def conditions():
    print("conditions")
    h, t = await read_dht()
    alert_sent = await check_conditions(h=h, t=t)
    print(alert_sent)
    if alert_sent:
        print("checking condition in 30 min")
        await asyncio.sleep(1800)
        await status_state(False, 'alert_sent')
        await conditions()
    else:
        print('conditions failed')


async def main():
    print("Iniciando procesos...")
    raspberry_task = asyncio.create_task(raspberry())
    reports_task = asyncio.create_task(reports())
    conditions_task = asyncio.create_task(conditions())
    await bot.polling()

    asyncio.gather(raspberry_task, reports_task, conditions_task)

if __name__ == "__main__":
    print("Bot inicializado 🤖")
    try:
        asyncio.run(main())
    except Exception as e:
        print("\nBot finalizado")
