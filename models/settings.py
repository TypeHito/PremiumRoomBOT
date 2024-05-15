from typing import Optional

from utils import const


class Settings:
    # Pyrogram
    API_ID: int = const.API_ID
    API_HASH: str = const.API_HASH
    BOT_TOKEN: str = const.BOT_TOKEN

    ADMIN: Optional[int] = const.ADMIN
    PROVIDER_TOKEN_LIVE: str = const.PROVIDER_TOKEN_LIVE
    PROVIDER_TOKEN_TEST: str = const.PROVIDER_TOKEN_TEST

    # Antiflood
    MESSAGES: int = 3
    # Rate limit (N) messages every x seconds
    SECONDS: int = 10
    # Rate limit x messages every (N) seconds
    CB_SECONDS: int = 10
    # Rate limit x callback queries every (N) seconds


