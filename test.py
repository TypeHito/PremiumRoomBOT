from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pyrogram import Client
from utils import const

bot = Client(
        "ALGO_Moderator",
        api_id=const.API_ID,
        api_hash=const.API_HASH,
        bot_token=const.BOT_TOKEN,
        plugins=dict(root="plugins"),
    )


async def job():
    await bot.send_message(const.ADMINS[0], "Hi!")


scheduler = AsyncIOScheduler()
scheduler.add_job(job, "interval", seconds=3)

scheduler.start()
bot.run()