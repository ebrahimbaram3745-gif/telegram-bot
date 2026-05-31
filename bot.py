import os
import json

from flask import Flask
from threading import Thread

app_flask = Flask('')

@app_flask.route('/', methods=['GET', 'HEAD'])
def home():
    return "Bot is running!", 200

def run():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os
TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "Pokemon_VPN"

SUPPORT_ID = "mak_11q"

ADMIN_ID = 7363962357
SECOND_ADMIN_ID = 8489061532

CARD_NUMBER = "6219861449318822"

waiting_receipt = {}
wallet_wait = {}
pending_config_user = {}
user_wallets = load_data("balances.json")

gift_wait = {}
used_gifts = load_data("gifts.json")
pending_gifts = {}
waiting_config = {}
broadcast_wait = {}
private_message_wait = {}

eco_prices = {
    "ð 1G | â³ 30D | ð° 50T": 50000,
    "ð 2G | â³ 30D | ð° 95T": 95000,
    "ð 3G | â³ 30D | ð° 140T": 140000,
    "ð 4G | â³ 30D | ð° 190T": 190000,
    "ð 5G | â³ 30D | ð° 235T": 235000,
    "ð 6G | â³ 30D | ð° 287T": 287000,
    "ð 7G | â³ 30D | ð° 340T": 340000,
    "ð 8G | â³ 30D | ð° 387T": 387000,
    "ð 9G | â³ 30D | ð° 438T": 438000,
    "ð 10G | â³ 30D | ð° 490T": 490000,
}

vip_prices = {
    "ð 70G | â³ 30D | ð° 690T": 690000,
}


def load_data(filename):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def joined(user_id, bot):

    try:

        member = await bot.get_chat_member(
            f"@{CHANNEL_USERNAME}",
            user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:
        return False


def home_keys():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "ð Ø®Ø±ÛØ¯ Ø³Ø±ÙÛØ³",
                callback_data="buy"
            )
        ],

        [
            InlineKeyboardButton(
                "ð° Ú©ÛÙ Ù¾ÙÙ",
                callback_data="wallet"
            ),

            InlineKeyboardButton(
                "ð Ù¾Ø´ØªÛØ¨Ø§ÙÛ",
                url=f"https://t.me/{SUPPORT_ID}"
            )
        ],

        [
            InlineKeyboardButton(
                "ð Ú©Ø¯ ÙØ¯ÛÙ",
                callback_data="gift"
            ),

            InlineKeyboardButton(
                "ð ØªØ³Øª Ø§Ú©Ø§ÙØª Ø±Ø§ÛÚ¯Ø§Ù",
                callback_data="free_test"
            )
        ],

        [
            InlineKeyboardButton(
                "ð Ø¢ÙÙØ²Ø´ Ø§ØªØµØ§Ù",
                callback_data="help"
            ),

            InlineKeyboardButton(
                "ð ØªØ¹Ø±ÙÙ ÙÛÙØªâÙØ§",
                callback_data="prices"
            )
        ],

        [
            InlineKeyboardButton(
                "ð¢ Ø§Ø±Ø³Ø§Ù Ù¾ÛØ§Ù ÙÙÚ¯Ø§ÙÛ",
                callback_data="broadcast"
            )
        ]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ok = await joined(
        update.effective_user.id,
        context.bot
    )

    if not ok:

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð¢ Ø¹Ø¶ÙÛØª Ø¯Ø± Ú©Ø§ÙØ§Ù",
                    url=f"https://t.me/{CHANNEL_USERNAME}"
                )
            ],

            [
                InlineKeyboardButton(
                    "â Ø¹Ø¶Ù Ø´Ø¯Ù",
                    callback_data="check_join"
                )
            ]
        ])

        await update.message.reply_text(
            "â Ø§Ø¨ØªØ¯Ø§ Ø¹Ø¶Ù Ú©Ø§ÙØ§Ù Ø´ÙÛØ¯",
            reply_markup=keyboard
        )

        return

    user_id = update.effective_user.id

    try:
        with open("users.txt", "a+", encoding="utf-8") as f:

            f.seek(0)

            users = f.read().splitlines()

            if str(user_id) not in users:

                f.write(f"{user_id}\n")

    except:
        pass

    if user_id not in user_wallets:
        user_wallets[user_id] = 0
        save_data("balances.json", user_wallets)

    text = """
â¨ Ø¨Ù PokÃ©mon VPN Ø®ÙØ´ Ø§ÙÙØ¯Û

ð Ø³Ø±ÙÛØ³ ÙØ§Û Ù¾Ø±Ø³Ø±Ø¹Øª V2Ray
ð©ðª Ø³Ø±ÙØ±ÙØ§Û Ù¾Ø§ÛØ¯Ø§Ø± Ø¢ÙÙØ§Ù
â¡ Ø³Ø±Ø¹Øª Ø¨Ø§ÙØ§ Ù Ù¾ÛÙÚ¯ Ø¹Ø§ÙÛ
"""

    await update.message.reply_text(
        text,
        reply_markup=home_keys()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    data = query.data

    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_wallets:
        user_wallets[user_id] = 0
        save_data("balances.json", user_wallets)

    # ØªØ§ÛÛØ¯ Ø±Ø³ÛØ¯
    if data.startswith("accept_"):

        target_user = int(data.split("_")[1])

        info = waiting_receipt.get(target_user)

        if info and info["type"] == "wallet":

            amount = info["amount"]

            user_wallets[target_user] += amount
            save_data("balances.json", user_wallets)

            await context.bot.send_message(
                target_user,
                f"""
â Ú©ÛÙ Ù¾ÙÙ Ø´ÙØ§ Ø´Ø§Ø±Ú Ø´Ø¯

ð° ÙØ¨ÙØº:
{amount:,} ØªÙÙØ§Ù

ðµ ÙÙØ¬ÙØ¯Û Ø¬Ø¯ÛØ¯:
{user_wallets[target_user]:,} ØªÙÙØ§Ù
"""
            )

            await query.answer(
                "Ú©ÛÙ Ù¾ÙÙ Ø´Ø§Ø±Ú Ø´Ø¯ â",
                show_alert=True
            )

        else:

            pending_config_user[target_user] = target_user

            await context.bot.send_message(
                target_user,
                """
â Ù¾Ø±Ø¯Ø§Ø®Øª Ø´ÙØ§ ØªØ§ÛÛØ¯ Ø´Ø¯

â³ ÙØ·ÙØ§ ÙÙØªØ¸Ø± Ø§Ø±Ø³Ø§Ù Ú©Ø§ÙÙÛÚ¯ Ø¨Ø§Ø´ÛØ¯
"""
            )

            await query.answer(
                "ØªØ§ÛÛØ¯ Ø´Ø¯ â",
                show_alert=True
            )

    # Ø±Ø¯ Ø±Ø³ÛØ¯
    elif data.startswith("reject_"):

        target_user = int(data.split("_")[1])

        await context.bot.send_message(
            target_user,
            """
â Ù¾Ø±Ø¯Ø§Ø®Øª Ø´ÙØ§ Ø±Ø¯ Ø´Ø¯

ð Ø¨Ø§ Ù¾Ø´ØªÛØ¨Ø§ÙÛ ØªÙØ§Ø³ Ø¨Ú¯ÛØ±ÛØ¯
"""
        )

    # ÚÚ© Ø¹Ø¶ÙÛØª
    elif data == "check_join":

        ok = await joined(
            query.from_user.id,
            context.bot
        )

        if ok:

            text = """
â¨ Ø¨Ù PokÃ©mon VPN Ø®ÙØ´ Ø§ÙÙØ¯Û

ð Ø³Ø±ÙÛØ³ ÙØ§Û Ù¾Ø±Ø³Ø±Ø¹Øª V2Ray
ð©ðª Ø³Ø±ÙØ±ÙØ§Û Ù¾Ø§ÛØ¯Ø§Ø± Ø¢ÙÙØ§Ù
â¡ Ø³Ø±Ø¹Øª Ø¨Ø§ÙØ§ Ù Ù¾ÛÙÚ¯ Ø¹Ø§ÙÛ
"""

            await query.message.edit_text(
                text,
                reply_markup=home_keys()
            )

        else:

            await query.answer(
                "â ÙÙÙØ² Ø¹Ø¶Ù ÙØ´Ø¯Û",
                show_alert=True
            )

    # Ø®Ø§ÙÙ
    elif data == "home":

        text = """
â¨ Ø¨Ù PokÃ©mon VPN Ø®ÙØ´ Ø§ÙÙØ¯Û

ð Ø³Ø±ÙÛØ³ ÙØ§Û Ù¾Ø±Ø³Ø±Ø¹Øª V2Ray
ð©ðª Ø³Ø±ÙØ±ÙØ§Û Ù¾Ø§ÛØ¯Ø§Ø± Ø¢ÙÙØ§Ù
â¡ Ø³Ø±Ø¹Øª Ø¨Ø§ÙØ§ Ù Ù¾ÛÙÚ¯ Ø¹Ø§ÙÛ
"""

        await query.message.edit_text(
            text,
            reply_markup=home_keys()
        )

    # Ø®Ø±ÛØ¯
    elif data == "buy":

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð©ðª Ù¾ÙÙ Ø§ÙØªØµØ§Ø¯Û",
                    callback_data="eco"
                )
            ],

            [
                InlineKeyboardButton(
                    "ð Ù¾ÙÙ VIP",
                    callback_data="vip"
                )
            ],

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            "ð ÙÙØ¹ Ù¾ÙÙ Ø±Ø§ Ø§ÙØªØ®Ø§Ø¨ Ú©ÙÛØ¯",
            reply_markup=keyboard
        )

    # Ú©ÛÙ Ù¾ÙÙ
    elif data == "wallet":

        text = f"""
ð° Ú©ÛÙ Ù¾ÙÙ Ø´ÙØ§

ð¤ {query.from_user.first_name}

ðµ ÙÙØ¬ÙØ¯Û:
{user_wallets[user_id]:,} ØªÙÙØ§Ù
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "â Ø§ÙØ²Ø§ÛØ´ ÙÙØ¬ÙØ¯Û",
                    callback_data="charge"
                )
            ],

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            reply_markup=keyboard
        )

    # Ø§ÙØ²Ø§ÛØ´ ÙÙØ¬ÙØ¯Û
    elif data == "charge":

        wallet_wait[user_id] = True

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="wallet"
                )
            ]
        ])

        await query.message.edit_text(
            "ðµ ÙØ¨ÙØº ÙÙØ±Ø¯ÙØ¸Ø± Ø±Ø§ Ø§Ø±Ø³Ø§Ù Ú©ÙÛØ¯",
            reply_markup=keyboard
        )

    # Ø§ÙØªØµØ§Ø¯Û
    elif data == "eco":

        keys = []

        for gb, price in eco_prices.items():

            keys.append([

                InlineKeyboardButton(
                    f"ð¢ {gb} â¢ {price:,}",
                    callback_data=f"eco_{gb}"
                )
            ])

        keys.append([

            InlineKeyboardButton(
                "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                callback_data="buy"
            )
        ])

        await query.message.edit_text(
            "ð©ðª Ù¾ÙÙ ÙØ§Û Ø§ÙØªØµØ§Ø¯Û",
            reply_markup=InlineKeyboardMarkup(keys)
        )

    # vip
    elif data == "vip":

        keys = []

        for gb, price in vip_prices.items():

            keys.append([

                InlineKeyboardButton(
                    f"ð¢ {gb} â¢ {price:,}",
                    callback_data=f"vip_{gb}"
                )
            ])

        keys.append([

            InlineKeyboardButton(
                "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                callback_data="buy"
            )
        ])

        await query.message.edit_text(
            "ð Ù¾ÙÙ ÙØ§Û VIP",
            reply_markup=InlineKeyboardMarkup(keys)
        )

    # Ø®Ø±ÛØ¯ Ø§ÙØªØµØ§Ø¯Û
    elif data.startswith("eco_"):

        gb = data.replace("eco_", "")
        price = eco_prices[gb]

        waiting_receipt[user_id] = {
            "type": "buy",
            "plan": gb,
            "amount": price
        }

        text = f"""
ð©ðª Economic Plan

ð¦ Ø­Ø¬Ù:
{gb}

ðµ ÙØ¨ÙØº:
{price:,} ØªÙÙØ§Ù

ð³ Ø´ÙØ§Ø±Ù Ú©Ø§Ø±Øª:

<code>{CARD_NUMBER}</code>

ð¤ Ø¨Ø¹Ø¯ Ø§Ø² Ù¾Ø±Ø¯Ø§Ø®Øª Ø±Ø³ÛØ¯ Ø§Ø±Ø³Ø§Ù Ú©ÙÛØ¯
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð° Ø®Ø±ÛØ¯ Ø§Ø² Ú©ÛÙ Ù¾ÙÙ",
                    callback_data=f"buywallet_eco_{gb}"
                )
            ],

            [
                InlineKeyboardButton(
                    "ð Ú©Ù¾Û Ø´ÙØ§Ø±Ù Ú©Ø§Ø±Øª",
                    switch_inline_query_current_chat=CARD_NUMBER
                )
            ],

            [
                InlineKeyboardButton(
                    "ðµ Ú©Ù¾Û ÙØ¨ÙØº",
                    switch_inline_query_current_chat=str(price)
                )
            ],

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="eco"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    # Ø®Ø±ÛØ¯ vip
    elif data.startswith("vip_"):

        gb = data.replace("vip_", "")
        price = vip_prices[gb]

        waiting_receipt[user_id] = {
            "type": "buy",
            "plan": gb,
            "amount": price
        }

        text = f"""
ð VIP Plan

ð¦ Ø­Ø¬Ù:
{gb}

ðµ ÙØ¨ÙØº:
{price:,} ØªÙÙØ§Ù

ð³ Ø´ÙØ§Ø±Ù Ú©Ø§Ø±Øª:

<code>{CARD_NUMBER}</code>

ð¤ Ø¨Ø¹Ø¯ Ø§Ø² Ù¾Ø±Ø¯Ø§Ø®Øª Ø±Ø³ÛØ¯ Ø§Ø±Ø³Ø§Ù Ú©ÙÛØ¯
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð° Ø®Ø±ÛØ¯ Ø§Ø² Ú©ÛÙ Ù¾ÙÙ",
                    callback_data=f"buywallet_vip_{gb}"
                )
            ],

            [
                InlineKeyboardButton(
                    "ð Ú©Ù¾Û Ø´ÙØ§Ø±Ù Ú©Ø§Ø±Øª",
                    switch_inline_query_current_chat=CARD_NUMBER
                )
            ],

            [
                InlineKeyboardButton(
                    "ðµ Ú©Ù¾Û ÙØ¨ÙØº",
                    switch_inline_query_current_chat=str(price)
                )
            ],

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="vip"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    # Ø®Ø±ÛØ¯ Ø¨Ø§ Ú©ÛÙ Ù¾ÙÙ Ø§ÙØªØµØ§Ø¯Û
    elif data.startswith("buywallet_eco_"):

        gb = data.replace("buywallet_eco_", "")
        price = eco_prices[gb]

        if user_wallets[user_id] < price:

            await query.message.edit_text(
                "â ÙÙØ¬ÙØ¯Û Ø´ÙØ§ Ú©Ø§ÙÛ ÙÛØ³Øª"
            )

            return

        user_wallets[user_id] -= price
        save_data("balances.json", user_wallets)

        pending_config_user[user_id] = user_id

        await context.bot.send_message(
            ADMIN_ID,
            f"""
ð Ø®Ø±ÛØ¯ Ø¬Ø¯ÛØ¯ Ø¨Ø§ Ú©ÛÙ Ù¾ÙÙ

ð¤ {query.from_user.first_name}

ð¦ {gb}

ðµ {price:,} ØªÙÙØ§Ù
"""
        )

        await context.bot.send_message(
            SECOND_ADMIN_ID,
            f"""
ð Ø®Ø±ÛØ¯ Ø¬Ø¯ÛØ¯ Ø¨Ø§ Ú©ÛÙ Ù¾ÙÙ

ð¤ {query.from_user.first_name}

ð¦ {gb}

ðµ {price:,} ØªÙÙØ§Ù
"""
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            """
â Ø®Ø±ÛØ¯ Ø§ÙØ¬Ø§Ù Ø´Ø¯

â³ ÙÙØªØ¸Ø± Ø§Ø±Ø³Ø§Ù Ú©Ø§ÙÙÛÚ¯ Ø¨Ø§Ø´ÛØ¯
""",
            reply_markup=keyboard
        )

    # Ø®Ø±ÛØ¯ Ø¨Ø§ Ú©ÛÙ Ù¾ÙÙ vip
    elif data.startswith("buywallet_vip_"):

        gb = data.replace("buywallet_vip_", "")
        price = vip_prices[gb]

        if user_wallets[user_id] < price:

            await query.message.edit_text(
                "â ÙÙØ¬ÙØ¯Û Ø´ÙØ§ Ú©Ø§ÙÛ ÙÛØ³Øª"
            )

            return

        user_wallets[user_id] -= price
        save_data("balances.json", user_wallets)

        pending_config_user[user_id] = user_id

        await context.bot.send_message(
            ADMIN_ID,
            f"""
ð Ø®Ø±ÛØ¯ Ø¬Ø¯ÛØ¯ Ø¨Ø§ Ú©ÛÙ Ù¾ÙÙ

ð¤ {query.from_user.first_name}

ð¦ {gb}

ðµ {price:,} ØªÙÙØ§Ù
"""
        )

        await context.bot.send_message(
            SECOND_ADMIN_ID,
            f"""
ð Ø®Ø±ÛØ¯ Ø¬Ø¯ÛØ¯ Ø¨Ø§ Ú©ÛÙ Ù¾ÙÙ

ð¤ {query.from_user.first_name}

ð¦ {gb}

ðµ {price:,} ØªÙÙØ§Ù
"""
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            """
â Ø®Ø±ÛØ¯ Ø§ÙØ¬Ø§Ù Ø´Ø¯

â³ ÙÙØªØ¸Ø± Ø§Ø±Ø³Ø§Ù Ú©Ø§ÙÙÛÚ¯ Ø¨Ø§Ø´ÛØ¯
""",
            reply_markup=keyboard
        )


    # ØªØ³Øª Ø±Ø§ÛÚ¯Ø§Ù
    elif data == "free_test":

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            "â Ø¯Ø± Ø­Ø§Ù Ø­Ø§Ø¶Ø± Ø§Ú©Ø§ÙØª ØªØ³Øª ÙÙØ¬ÙØ¯ ÙÛØ³Øª",
            reply_markup=keyboard
        )

    # Ú©Ø¯ ÙØ¯ÛÙ
    elif data == "gift":

        gift_wait[user_id] = True

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            "ð Ú©Ø¯ ÙØ¯ÛÙ ÙØ§Ø±Ø¯ Ú©ÙÛØ¯",
            reply_markup=keyboard
        )


    # ØªØ§ÛÛØ¯ Ú©Ø¯ ÙØ¯ÛÙ
    elif data.startswith("gift_accept_"):

        target_id = int(data.replace("gift_accept_", ""))

        volume = pending_gifts.get(target_id, "ÙØ§ÙØ´Ø®Øµ")

        waiting_config[query.from_user.id] = target_id

        await context.bot.send_message(
            chat_id=target_id,
            text="â Ú©Ø¯ ÙØ¯ÛÙ Ø´ÙØ§ Ø¨Ø§ ÙÙÙÙÛØª ØªØ§ÛÛØ¯ Ø´Ø¯\nâ³ Ø¯Ø± Ø­Ø§Ù Ø¨Ø±Ø±Ø³Û Ø§Ø³Øª Ù ÙÙØªØ¸Ø± Ú©Ø§ÙÙÛÙÚ¯ Ø¨Ø§Ø´ÛØ¯"
        )

        await query.message.reply_text(
            "ð¤ Ú©Ø§ÙÙÛÙÚ¯ Ú©Ø§Ø±Ø¨Ø± Ø±Ø§ Ø§Ø±Ø³Ø§Ù Ú©ÙÛØ¯"
        )

        await query.answer("ØªØ§ÛÛØ¯ Ø´Ø¯")

    # Ø±Ø¯ Ú©Ø¯ ÙØ¯ÛÙ
    elif data.startswith("gift_reject_"):

        target_id = int(data.replace("gift_reject_", ""))

        await context.bot.send_message(
            chat_id=target_id,
            text="â Ú©Ø¯ ÙØ¯ÛÙ Ø´ÙØ§ ØªÙØ³Ø· ÙØ¯ÛØ± Ø±Ø¯ Ø´Ø¯"
        )

        await query.answer("Ø±Ø¯ Ø´Ø¯")



    # Ù¾ÛØ§Ù ÙÙÚ¯Ø§ÙÛ
    elif data == "broadcast":

        if user_id != ADMIN_ID:

            return

        users_buttons = []

        try:

            with open("users.txt", "r", encoding="utf-8") as f:

                users = f.read().splitlines()

            for uid in users:

                try:

                    chat = await context.bot.get_chat(int(uid))

                    username = chat.username if chat.username else "ÙØ¯Ø§Ø±Ø¯"

                    users_buttons.append([

                        InlineKeyboardButton(
                            f"{username} | {uid}",
                            callback_data=f"pm_{uid}"
                        )

                    ])

                except:

                    users_buttons.append([

                        InlineKeyboardButton(
                            f"Ú©Ø§Ø±Ø¨Ø± | {uid}",
                            callback_data=f"pm_{uid}"
                        )

                    ])

        except:

            pass

        users_buttons.append([

            InlineKeyboardButton(
                "ð¢ Ø§Ø±Ø³Ø§Ù Ù¾ÛØ§Ù Ø¨Ù Ú©Ù Ú©Ø§Ø±Ø¨Ø±Ø§Ù",
                callback_data="send_all_users"
            )

        ])

        users_buttons.append([

            InlineKeyboardButton(
                "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                callback_data="home"
            )

        ])

        keyboard = InlineKeyboardMarkup(users_buttons)

        await query.message.edit_text(
            "ð¢ ÛÚ© Ú©Ø§Ø±Ø¨Ø± Ø§ÙØªØ®Ø§Ø¨ Ú©ÙÛØ¯ ÛØ§ Ø§Ø±Ø³Ø§Ù ÙÙÚ¯Ø§ÙÛ Ø¨Ø²ÙÛØ¯",
            reply_markup=keyboard
        )

    elif data == "send_all_users":

        broadcast_wait[user_id] = True

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="broadcast"
                )
            ]
        ])

        await query.message.edit_text(
            "ð¢ Ù¾ÛØ§Ù Ø®ÙØ¯ Ø±Ø§ Ø¨Ø±Ø§Û Ú©Ù Ú©Ø§Ø±Ø¨Ø±Ø§Ù Ø§Ø±Ø³Ø§Ù Ú©ÙÛØ¯",
            reply_markup=keyboard
        )

    elif data.startswith("pm_"):

        target_id = int(data.replace("pm_", ""))

        private_message_wait[user_id] = target_id

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="broadcast"
                )
            ]
        ])

        await query.message.edit_text(
            f"âï¸ Ù¾ÛØ§Ù Ø®ÙØ¯ Ø±Ø§ Ø¨Ø±Ø§Û Ú©Ø§Ø±Ø¨Ø± {target_id} Ø§Ø±Ø³Ø§Ù Ú©ÙÛØ¯",
            reply_markup=keyboard
        )


    # ØªØ¹Ø±ÙÙ
    elif data == "prices":

        text = """
Ø³ÙØ§Ù ÙÙÚ©Ø§Ø± Ú¯Ø±Ø§ÙÛ ð

ð£ ÙØ± Ú¯ÛÚ¯ 190 ØªÙÙØ§Ù

ID : @mak_11q

ð¢ Ø¢ÙÙØ§ÛÙ
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ø®Ø±ÛØ¯ Ø³Ø±ÙÛØ³",
                    callback_data="buy"
                )
            ],

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            reply_markup=keyboard
        )

    # Ø¢ÙÙØ²Ø´
    elif data == "help":

        text = """
ð Ø¢ÙÙØ²Ø´ Ø§ØªØµØ§Ù

1ï¸â£ Ø¨Ø±ÙØ§ÙÙ V2rayNG ÙØµØ¨ Ú©ÙÛØ¯

2ï¸â£ Ú©Ø§ÙÙÛÚ¯ Ø±Ø§ Ú©Ù¾Û Ú©ÙÛØ¯

3ï¸â£ Ø¯Ø§Ø®Ù Ø¨Ø±ÙØ§ÙÙ Paste Ú©ÙÛØ¯

4ï¸â£ Connect Ø¨Ø²ÙÛØ¯
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            reply_markup=keyboard
        )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    # Ø§Ø±Ø³Ø§Ù Ú©Ø§ÙÙÛÚ¯
    if (
        user_id == ADMIN_ID
        or user_id == SECOND_ADMIN_ID
    ) and pending_config_user:

        target_user = list(
            pending_config_user.values()
        )[-1]

        await context.bot.send_message(
            target_user,
            f"""
ð Ú©Ø§ÙÙÛÚ¯ Ø´ÙØ§ Ø¢ÙØ§Ø¯Ù Ø´Ø¯

<code>{update.message.text}</code>

ð Ø§ØªØµØ§Ù Ù¾Ø±Ø³Ø±Ø¹Øª Ù Ù¾Ø§ÛØ¯Ø§Ø±
""",
            parse_mode="HTML"
        )

        await update.message.reply_text(
            "â Ú©Ø§ÙÙÛÚ¯ Ø§Ø±Ø³Ø§Ù Ø´Ø¯"
        )

        del pending_config_user[
            list(pending_config_user.keys())[-1]
        ]

        return


    # Ú©Ø¯ ÙØ¯ÛÙ
    if user_id in gift_wait:

        code = update.message.text.strip()

        if user_id not in used_gifts:
            used_gifts[user_id] = []
            save_data("gifts.json", used_gifts)

        if code in used_gifts[user_id]:

            await update.message.reply_text(
                "â Ø´ÙØ§ ÙØ¨ÙØ§Ù Ø§Ø² Ø§ÛÙ Ú©Ø¯ ÙØ¯ÛÙ Ø§Ø³ØªÙØ§Ø¯Ù Ú©Ø±Ø¯ÙâØ§ÛØ¯"
            )

            return

        if code == "mam4di":

            used_gifts[user_id].append(code)
            save_data("gifts.json", used_gifts)

            pending_gifts[user_id] = "1 Ú¯ÛÚ¯"

            keyboard = InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "â ØªØ§ÛÛØ¯",
                        callback_data=f"gift_accept_{user_id}"
                    ),

                    InlineKeyboardButton(
                        "â Ø±Ø¯ Ú©Ø±Ø¯Ù",
                        callback_data=f"gift_reject_{user_id}"
                    )
                ]
            ])

            await context.bot.send_message(
                ADMIN_ID,
                f"""
ð Ú©Ø¯ ÙØ¯ÛÙ Ø¬Ø¯ÛØ¯ Ø«Ø¨Øª Ø´Ø¯

ð¤ ÙØ§Ù:
{update.effective_user.first_name}

ð ÛÙØ²Ø±ÙÛÙ:
@{update.effective_user.username}

ð Ø¢ÛØ¯Û:
{user_id}

ð Ú©Ø¯ ÙØ¯ÛÙ:
mam4di

ð¦ Ø­Ø¬Ù:
1 Ú¯ÛÚ¯
""",
                reply_markup=keyboard
            )

            await update.message.reply_text(
                "â Ú©Ø¯ ÙØ¯ÛÙ Ø´ÙØ§ Ø¨Ø§ ÙÙÙÙÛØª Ø«Ø¨Øª Ø´Ø¯\nð¦ Ø­Ø¬Ù Ú©Ø¯ ÙØ¯ÛÙ Ø´ÙØ§ 1 Ú¯ÛÚ¯ ÙÛØ¨Ø§Ø´Ø¯\nâ³ Ø¨Ø¹Ø¯ ØªØ§ÛÛØ¯ ÙØ¯ÛØ± Ú©Ø§ÙÙÛÙÚ¯ Ø´ÙØ§ Ø§Ø±Ø³Ø§Ù Ø®ÙØ§ÙØ¯ Ø´Ø¯"
            )

            del gift_wait[user_id]

            return

        elif code == "mam4di_1k":

            used_gifts[user_id].append(code)
            save_data("gifts.json", used_gifts)

            pending_gifts[user_id] = "2 Ú¯ÛÚ¯"

            keyboard = InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "â ØªØ§ÛÛØ¯",
                        callback_data=f"gift_accept_{user_id}"
                    ),

                    InlineKeyboardButton(
                        "â Ø±Ø¯ Ú©Ø±Ø¯Ù",
                        callback_data=f"gift_reject_{user_id}"
                    )
                ]
            ])

            await context.bot.send_message(
                ADMIN_ID,
                f"""
ð Ú©Ø¯ ÙØ¯ÛÙ Ø¬Ø¯ÛØ¯ Ø«Ø¨Øª Ø´Ø¯

ð¤ ÙØ§Ù:
{update.effective_user.first_name}

ð ÛÙØ²Ø±ÙÛÙ:
@{update.effective_user.username}

ð Ø¢ÛØ¯Û:
{user_id}

ð Ú©Ø¯ ÙØ¯ÛÙ:
mam4di_1k

ð¦ Ø­Ø¬Ù:
2 Ú¯ÛÚ¯
""",
                reply_markup=keyboard
            )

            await update.message.reply_text(
                "â Ú©Ø¯ ÙØ¯ÛÙ Ø´ÙØ§ Ø¨Ø§ ÙÙÙÙÛØª Ø«Ø¨Øª Ø´Ø¯\nð¦ Ø­Ø¬Ù Ú©Ø¯ ÙØ¯ÛÙ Ø´ÙØ§ 2 Ú¯ÛÚ¯ ÙÛØ¨Ø§Ø´Ø¯\nâ³ Ø¨Ø¹Ø¯ ØªØ§ÛÛØ¯ ÙØ¯ÛØ± Ú©Ø§ÙÙÛÙÚ¯ Ø´ÙØ§ Ø§Ø±Ø³Ø§Ù Ø®ÙØ§ÙØ¯ Ø´Ø¯"
            )

            del gift_wait[user_id]

            return

        else:

            await update.message.reply_text(
                "â Ú©Ø¯ ÙØ¯ÛÙ ÙØ§ÙØ¹ØªØ¨Ø± Ø§Ø³Øª"
            )

            return



    # Ø§Ø±Ø³Ø§Ù Ú©Ø§ÙÙÛÚ¯ ØªÙØ³Ø· ÙØ¯ÛØ±
    if user_id in waiting_config:

        target_user = waiting_config[user_id]

        await context.bot.send_message(
            chat_id=target_user,
            text=update.message.text
        )

        await update.message.reply_text(
            "â Ú©Ø§ÙÙÛÙÚ¯ Ø¨Ø§ ÙÙÙÙÛØª Ø§Ø±Ø³Ø§Ù Ø´Ø¯"
        )

        del waiting_config[user_id]

        return

    # Ù¾ÛØ§Ù ÙÙÚ¯Ø§ÙÛ
    if user_id in broadcast_wait:

        try:

            with open("users.txt", "r", encoding="utf-8") as f:

                users = f.readlines()

            for user in users:

                try:

                    uid = int(user.strip())

                    await context.bot.send_message(
                        chat_id=uid,
                        text=update.message.text
                    )

                except:

                    pass

            await update.message.reply_text(
                "â Ù¾ÛØ§Ù Ø´ÙØ§ Ø¨Ø§ ÙÙÙÙÛØª Ø¨Ø±Ø§Û Ú©Ø§Ø±Ø¨Ø±Ø§Ù Ø§Ø±Ø³Ø§Ù Ø´Ø¯"
            )

        except:

            await update.message.reply_text(
                "â ÙÛØ³Øª Ú©Ø§Ø±Ø¨Ø±Ø§Ù Ù¾ÛØ¯Ø§ ÙØ´Ø¯"
            )

        del broadcast_wait[user_id]

        return



    # Ù¾ÛØ§Ù Ø®ØµÙØµÛ ÙØ¯ÛØ±
    if user_id in private_message_wait:

        target_user = private_message_wait[user_id]

        await context.bot.send_message(
            chat_id=target_user,
            text=update.message.text
        )

        await update.message.reply_text(
            "â Ù¾ÛØ§Ù Ø´ÙØ§ Ø¨Ø§ ÙÙÙÙÛØª Ø§Ø±Ø³Ø§Ù Ø´Ø¯"
        )

        del private_message_wait[user_id]

        return


    # ÙØ¨ÙØº Ú©ÛÙ Ù¾ÙÙ
    if user_id in wallet_wait:

        try:
            amount = int(update.message.text)

        except:

            await update.message.reply_text(
                "â ÙÙØ· Ø¹Ø¯Ø¯ ÙØ§Ø±Ø¯ Ú©ÙÛØ¯"
            )

            return

        waiting_receipt[user_id] = {
            "type": "wallet",
            "amount": amount
        }

        text = f"""
ð° Ø§ÙØ²Ø§ÛØ´ ÙÙØ¬ÙØ¯Û Ú©ÛÙ Ù¾ÙÙ

ðµ ÙØ¨ÙØº:
{amount:,} ØªÙÙØ§Ù

ð³ Ø´ÙØ§Ø±Ù Ú©Ø§Ø±Øª:

<code>{CARD_NUMBER}</code>

ð¤ Ø¨Ø¹Ø¯ Ø§Ø² ÙØ§Ø±ÛØ² Ø±Ø³ÛØ¯ Ø§Ø±Ø³Ø§Ù Ú©ÙÛØ¯
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "ð Ú©Ù¾Û Ø´ÙØ§Ø±Ù Ú©Ø§Ø±Øª",
                    switch_inline_query_current_chat=CARD_NUMBER
                )
            ],

            [
                InlineKeyboardButton(
                    "ðµ Ú©Ù¾Û ÙØ¨ÙØº",
                    switch_inline_query_current_chat=str(amount)
                )
            ],

            [
                InlineKeyboardButton(
                    "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                    callback_data="wallet"
                )
            ]
        ])

        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

        del wallet_wait[user_id]


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in waiting_receipt:
        return

    photo = update.message.photo[-1].file_id

    info = waiting_receipt[user_id]

    if info["type"] == "wallet":

        txt = f"Ø´Ø§Ø±Ú Ú©ÛÙ Ù¾ÙÙ\n{info['amount']:,} ØªÙÙØ§Ù"

    else:

        txt = f"{info['plan']} | {info['amount']:,} ØªÙÙØ§Ù"

    caption = f"""
ð¥ Ø±Ø³ÛØ¯ Ø¬Ø¯ÛØ¯

ð¤ {update.effective_user.first_name}

ð @{update.effective_user.username}

ð ID:
{user_id}

ð Ø§Ø·ÙØ§Ø¹Ø§Øª:
{txt}
"""

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "â ØªØ§ÛÛØ¯",
                callback_data=f"accept_{user_id}"
            ),

            InlineKeyboardButton(
                "â Ø±Ø¯",
                callback_data=f"reject_{user_id}"
            )
        ]
    ])

    await context.bot.send_photo(
        ADMIN_ID,
        photo,
        caption=caption,
        reply_markup=keyboard
    )

    await context.bot.send_photo(
        SECOND_ADMIN_ID,
        photo,
        caption=caption,
        reply_markup=keyboard
    )

    keyboard2 = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "ð Ø¨Ø§Ø²Ú¯Ø´Øª",
                callback_data="home"
            )
        ]
    ])

    await update.message.reply_text(
        "â Ø±Ø³ÛØ¯ Ø´ÙØ§ Ø«Ø¨Øª Ø´Ø¯\nâ³ ÙÙØªØ¸Ø± ØªØ§ÛÛØ¯ ÙØ¯ÛØ±ÛØª Ø¨Ø§Ø´ÛØ¯",
        reply_markup=keyboard2
    )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(buttons)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
