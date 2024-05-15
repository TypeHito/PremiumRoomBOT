from models import shared, Settings
import asyncio
import sys
from utils import const
from pyrogram import Client, idle, enums
from api import connection, initial, uninstall
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from methods import user, timer


async def main():
    shared.settings = Settings()

    user_input = input("Start Type"
                       "\ni-init"
                       "\nn-normal"
                       "\nr-reload(database will delete and new open !!!!!!)"
                       "\nignore if you don't know: ")

    await connection()

    if user_input == "i":
        await initial(shared.database)
    elif user_input == "r":
        await uninstall(shared.database)
        await initial(shared.database)

    bot = Client(
        "ALGO_Moderator",
        api_id=shared.settings.API_ID,
        api_hash=shared.settings.API_HASH,
        bot_token=shared.settings.BOT_TOKEN,
        plugins=dict(root="plugins"),
        parse_mode=enums.ParseMode.HTML,
    )

    async def review():
        now = str(timer.get_current_time())
        try:
            users = await user.review_subscription(shared.database, now)
        except Exception as err:
            await bot.send_message(const.ADMINS[0], err)
        else:
            for i in users:
                await bot.send_message(const.ADMINS[0], f"{i[1]} time end. . .")
                await user.update_subscription_end(shared.database, i[1], 0, now)
                await bot.ban_chat_member(const.CHANNEL, i[1])
            # print(text)
            # await bot.send_message(const.ADMINS[0], "Hi!")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(review, "interval", seconds=10)
    print("\rBot has been started!")

    scheduler.start()
    await bot.start()

    return await idle()


sys.exit(asyncio.run(main()))
