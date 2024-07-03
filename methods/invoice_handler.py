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


from api import on_shipping_query, on_checkout_query


def set_invoice(currency="UZS", label="Demo", amount=10000000):
    return Invoice(
        currency=currency,  # UZS
        prices=[
            LabeledPrice(amount=amount, label=label),  # 100 000.00
        ],
        test=True,
        name_requested=True,
        phone_requested=True,
        email_requested=True,
        shipping_address_requested=False,
        flexible=True,
        phone_to_provider=True,
        email_to_provider=True,
        max_tip_amount=1500000,  # 15 000.00 максимум пожертвование
        suggested_tip_amounts=[500000, 1000000],
    )


async def init_invoice(bot, msg, title="ALGO DEMO", invoice="",
                       invoice_description="ALGO SIGNAL MM kanaliga 7 kunlik demo obuna "
                                           "(Obuna to'lo'v amalga oshirilgan sanadan 7 kun amal qiladi.)",
                       image_url=const.invoice_photos, invoice_payload="payloads",
                       provider_token=const.PROVIDER_TOKEN_TEST
                       ):
    return await bot.invoke(
        SendMedia(
            peer=await bot.resolve_peer(msg.chat.id),
            media=InputMediaInvoice(
                title=title,
                description=invoice_description,
                photo=InputWebDocument(
                    url=image_url,
                    size=1,
                    mime_type="image/png",
                    attributes=[DocumentAttributeImageSize(
                        w=512, h=512
                    )]
                ),
                invoice=set_invoice(),
                payload=f"{msg.from_user.id}_bought".encode(),
                provider=const.PROVIDER_TOKEN_TEST,
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
