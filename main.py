from models import shared, Settings
import asyncio
import sys
from utils import const
from pyrogram import Client, idle, enums
from api import connection, initial, uninstall
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from methods import user, timer
from utils import lang


async def main():
    start_type = input(const.START_INFO)

    shared.settings = Settings()
    await connection()

    if start_type == "i":
        await initial(shared.database)
    elif start_type == "r":
        await uninstall(shared.database)
        await initial(shared.database)

    bot = Client(
        const.APP_NAME,
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
            await bot.send_message(const.ADMINS[0],  str(err))
        else:
            for i in users:
                for admin in const.ADMINS:
                    print(lang.no_lang["info_user"].format(
                                               str(i[2]), str(i[1]), str(i[1]),  str(i[16]), str(i[17])))
                    await bot.send_message(admin,
                                           lang.no_lang["info_user"].format(
                                               str(i[2]), str(i[1]), str(i[1]),  str(i[16]), str(i[17])))
                await user.update_subscription_end(shared.database, i[1], 0, now)
                await bot.ban_chat_member(const.CHANNEL, i[1])

    scheduler = AsyncIOScheduler()
    scheduler.add_job(review, "interval", seconds=10)
    print("\rBot has been started!")

    scheduler.start()
    await bot.start()

    return await idle()


sys.exit(asyncio.run(main()))
