from pyrogram import Client, filters
from pyrogram.types import Message, User, Chat, InlineQuery

# @Client.on_inline_query()
# async def inline_invoice(bot: Client, query: InlineQuery):
#     return await bot.invoke(
#         SetInlineBotResults(
#             query_id=int(query.id),
#             results=[
#                 InputBotInlineResult(
#                     id=uuid4().hex,
#                     type="article",
#                     send_message=InputBotInlineMessageMediaInvoice(
#                         title="Inline Title",
#                         description="Inline Description",
#                         invoice=algo_7,
#                         payload=f"{query.from_user.id}_bought".encode(),
#                         provider=shared.settings.PROVIDER_TOKEN,
#                         provider_data=DataJSON(data="{}"),
#                         photo=None,
#                         reply_markup=None,
#                     ),
#                     title="Title",
#                     description="Description",
#                 )
#             ],
#             cache_time=0,
#             private=True,
#         )
#     )
