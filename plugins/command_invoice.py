import html
from typing import Dict
from uuid import uuid4
from utils import const
from pyrogram import Client, filters
from pyrogram.types import Message, User, Chat, InlineQuery
from pyrogram.raw.types import (
    InputMediaInvoice,
    DataJSON,
    Invoice,
    LabeledPrice,
    UpdateBotShippingQuery,
    ShippingOption,
    UpdateBotPrecheckoutQuery,
    InputBotInlineResult,
    InputWebDocument,
    DocumentAttributeImageSize,
    InputBotInlineMessageMediaInvoice,
)
from pyrogram.raw.functions.messages import (
    SendMedia,
    SetBotPrecheckoutResults,
    SetBotShippingResults,
    SetInlineBotResults,
)

from models import shared


from api import on_shipping_query, on_checkout_query


algo_7 = Invoice(
    currency="UZS",
    prices=[
        LabeledPrice(amount=300000000, label="ALGO 7"),
    ],
    test=True,
    name_requested=True,
    phone_requested=True,
    email_requested=True,
    shipping_address_requested=False,
    flexible=True,
    phone_to_provider=True,
    email_to_provider=True,
    max_tip_amount=1500000,
    suggested_tip_amounts=[500000, 1000000],
)
algo_30 = Invoice(
    currency="UZS",
    prices=[
        LabeledPrice(amount=300000000, label="ALGO 30"),
    ],
    test=True,
    name_requested=True,
    phone_requested=True,
    email_requested=True,
    shipping_address_requested=False,
    flexible=True,
    phone_to_provider=True,
    email_to_provider=True,
    max_tip_amount=1500000,
    suggested_tip_amounts=[500000, 1000000],
)

algo_demo = Invoice(
    currency="UZS",
    prices=[
        LabeledPrice(amount=10000000, label="ALGO 7"),
    ],
    test=True,
    name_requested=True,
    phone_requested=True,
    email_requested=True,
    shipping_address_requested=False,
    flexible=True,
    phone_to_provider=True,
    email_to_provider=True,
    max_tip_amount=1500000,
    suggested_tip_amounts=[500000, 1000000],
)


@Client.on_message(filters.private & filters.command("algo_7"))
async def send_algo_7(bot: Client, msg: Message):
    r = await bot.invoke(
        SendMedia(
            peer=await bot.resolve_peer(msg.chat.id),
            media=InputMediaInvoice(
                title="ALGO 7",
                description="ALGO SIGNAL MM kanaliga 7 kunlik obuna (Obuna to'lo'v amalga oshirilgan sanadan 7 kun amal qiladi.)",
                photo=InputWebDocument(
                    url=const.invoice_photos,
                    size=10,
                    mime_type="image/png",
                    attributes=[DocumentAttributeImageSize(
                        w=512, h=512
                    )]
                ),
                invoice=algo_7,
                payload=f"{msg.from_user.id}_bought".encode(),
                provider=const.PROVIDER_TOKEN_TEST,
                provider_data=DataJSON(data="{}"),
                start_param="start_param",
            ),
            message="",
            random_id=bot.rnd_id(),
        )
    )


@Client.on_message(filters.private & filters.command("algo_demo"))
async def send_algo_demo(bot: Client, msg: Message):
    r = await bot.invoke(
        SendMedia(
            peer=await bot.resolve_peer(msg.chat.id),
            media=InputMediaInvoice(
                title="ALGO DEMO",
                description="ALGO SIGNAL MM kanaliga 7 kunlik demo obuna (Obuna to'lo'v amalga oshirilgan sanadan 7 kun amal qiladi.)",
                photo=InputWebDocument(
                    url=const.invoice_photos,
                    size=1,
                    mime_type="image/png",
                    attributes=[DocumentAttributeImageSize(
                        w=512, h=512
                    )]
                ),
                invoice=algo_demo,
                payload=f"{msg.from_user.id}_bought".encode(),
                provider=const.PROVIDER_TOKEN_TEST,
                provider_data=DataJSON(data="{}"),
                start_param="start_param",
            ),

            message="",
            random_id=bot.rnd_id(),
        )
    )


@Client.on_message(filters.private & filters.command("algo_30"))
async def send_algo_30(bot: Client, msg: Message):
    r = await bot.invoke(
        SendMedia(
            peer=await bot.resolve_peer(msg.chat.id),
            media=InputMediaInvoice(
                title="ALGO 30",
                description="ALGO SIGNAL MM kanaliga 30 kunlik obuna (Obuna to'lo'v amalga oshirilgan sanadan 30 kun amal qiladi.)",
                photo=InputWebDocument(
                    url=const.invoice_photos,
                    size=1,
                    mime_type="image/png",
                    attributes=[DocumentAttributeImageSize(
                        w=512, h=512
                    )]
                ),
                invoice=algo_30,
                payload=f"{msg.from_user.id}_bought".encode(),
                provider="371317599:TEST:1715399177347",
                provider_data=DataJSON(data="{}"),
                start_param="start_param",
            ),

            message="",
            random_id=bot.rnd_id(),
        )
    )


@on_shipping_query
async def process_shipping_query(
    bot: Client,
    query: UpdateBotShippingQuery,
    users: Dict[int, User],
    chats: Dict[int, Chat],
):
    await bot.send_message(
        chat_id=query.user_id,
        text=f"You've chosen an option.\n\n<b>Payload</b>:\n<code>{html.escape(str(query))}</code>",
    )
    return await bot.invoke(
        SetBotShippingResults(
            query_id=query.query_id,
            shipping_options=[
                ShippingOption(
                    id="asd_shipping",
                    title="Test Shipping Option",
                    prices=[
                        LabeledPrice(amount=20000, label="asd"),
                    ],
                )
            ],
            error=None,
        )
    )


@on_checkout_query
async def process_checkout_query(
    bot: Client,
    query: UpdateBotPrecheckoutQuery,
    users: Dict[int, User],
    chats: Dict[int, Chat],
):
    await bot.send_message(
        chat_id=query.user_id,
        text=f"You successfully bought something.\n\n<b>Payload</b>:\n<code>{html.escape(str(query))}</code>",
    )
    return await bot.invoke(
        SetBotPrecheckoutResults(
            query_id=query.query_id,
            success=True,
            error=None,
        )
    )


@Client.on_inline_query()
async def inline_invoice(bot: Client, query: InlineQuery):
    return await bot.invoke(
        SetInlineBotResults(
            query_id=int(query.id),
            results=[
                InputBotInlineResult(
                    id=uuid4().hex,
                    type="article",
                    send_message=InputBotInlineMessageMediaInvoice(
                        title="Inline Title",
                        description="Inline Description",
                        invoice=algo_7,
                        payload=f"{query.from_user.id}_bought".encode(),
                        provider=shared.settings.PROVIDER_TOKEN,
                        provider_data=DataJSON(data="{}"),
                        photo=None,
                        reply_markup=None,
                    ),
                    title="Title",
                    description="Description",
                )
            ],
            cache_time=0,
            private=True,
        )
    )
