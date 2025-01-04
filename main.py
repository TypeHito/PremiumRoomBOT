from methods.command_handler import command_start
from models import shared, Settings
from pyrogram.errors.exceptions.bad_request_400 import BadRequest
from pyrogram.errors.exceptions.bad_request_400 import UserIsBot
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
        now = timer.get_current_time()
        members = []
        for CHANNEL in const.CHANNELS:
            try:
                async for member in bot.get_chat_members(CHANNEL):
                    members.append(member.user.id)
            except ValueError as err:
                return await bot.send_message(const.ADMINS[0], str(err))
        ids = await user.review_ids(shared.database, str(now))
        to_ban = set(members) - set(list(sum(ids, ())))
        for i in to_ban:
            if i not in const.ADMINS:
                for CHANNEL in const.CHANNELS:
                    try:
                        await bot.ban_chat_member(CHANNEL, i)
                    except BadRequest as err:
                        await bot.send_message(const.ADMINS[0], str(err))
        try:
            users = await user.review_subscription(shared.database, str(now))

        except Exception as err:
            await bot.send_message(const.ADMINS[0],  str(err))
        else:
            for i in users:
                await user.update_subscription_end(shared.database, i[1], 0, str(now))
                await bot.ban_chat_member(const.CHAT_ID, i[1])
                for channel in range(len(const.CHANNELS)):
                    await bot.ban_chat_member(const.CHANNELS[channel], i[1])


    scheduler = AsyncIOScheduler()
    scheduler.add_job(review, "interval", seconds=const.interval)
    print("\rBot has been started!")

    scheduler.start()
    await bot.start()

    return await idle()


sys.exit(asyncio.run(main()))
