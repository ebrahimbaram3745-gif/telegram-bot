import os
import json

def load_data(filename):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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
find_user_wait = {}
send_found_user_wait = {}

eco_prices = {
    "📊 1G | ⏳ 30D | 💰 50T": 50000,
    "📊 2G | ⏳ 30D | 💰 95T": 95000,
    "📊 3G | ⏳ 30D | 💰 140T": 140000,
    "📊 4G | ⏳ 30D | 💰 190T": 190000,
    "📊 5G | ⏳ 30D | 💰 235T": 235000,
    "📊 6G | ⏳ 30D | 💰 287T": 287000,
    "📊 7G | ⏳ 30D | 💰 340T": 340000,
    "📊 8G | ⏳ 30D | 💰 387T": 387000,
    "📊 9G | ⏳ 30D | 💰 438T": 438000,
    "📊 10G | ⏳ 30D | 💰 490T": 490000,
}

vip_prices = {
    "📊 70G | ⏳ 30D | 💰 690T": 690000,
}


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
                "🛒 خرید سرویس",
                callback_data="buy"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 کیف پول",
                callback_data="wallet"
            ),

            InlineKeyboardButton(
                "📞 پشتیبانی",
                url=f"https://t.me/{SUPPORT_ID}"
            )
        ],

        [
            InlineKeyboardButton(
                "🎁 کد هدیه",
                callback_data="gift"
            ),

            InlineKeyboardButton(
                "🆓 تست اکانت رایگان",
                callback_data="free_test"
            )
        ],

        [
            InlineKeyboardButton(
                "📚 آموزش اتصال",
                callback_data="help"
            ),

            InlineKeyboardButton(
                "📋 تعرفه قیمت‌ها",
                callback_data="prices"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 ارسال پیام همگانی",
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
                    "📢 عضویت در کانال",
                    url=f"https://t.me/{CHANNEL_USERNAME}"
                )
            ],

            [
                InlineKeyboardButton(
                    "✅ عضو شدم",
                    callback_data="check_join"
                )
            ]
        ])

        await update.message.reply_text(
            "❌ ابتدا عضو کانال شوید",
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
✨ به Pokémon VPN خوش اومدی

🚀 سرویس های پرسرعت V2Ray
🇩🇪 سرورهای پایدار آلمان
⚡ سرعت بالا و پینگ عالی
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

    # تایید رسید
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
✅ کیف پول شما شارژ شد

💰 مبلغ:
{amount:,} تومان

💵 موجودی جدید:
{user_wallets[target_user]:,} تومان
"""
            )

            await query.answer(
                "کیف پول شارژ شد ✅",
                show_alert=True
            )

        else:

            pending_config_user[target_user] = target_user

            await context.bot.send_message(
                target_user,
                """
✅ پرداخت شما تایید شد

⏳ لطفا منتظر ارسال کانفیگ باشید
"""
            )

            await query.answer(
                "تایید شد ✅",
                show_alert=True
            )

    # رد رسید
    elif data.startswith("reject_"):

        target_user = int(data.split("_")[1])

        await context.bot.send_message(
            target_user,
            """
❌ پرداخت شما رد شد

📞 با پشتیبانی تماس بگیرید
"""
        )

    # چک عضویت
    elif data == "check_join":

        ok = await joined(
            query.from_user.id,
            context.bot
        )

        if ok:

            text = """
✨ به Pokémon VPN خوش اومدی

🚀 سرویس های پرسرعت V2Ray
🇩🇪 سرورهای پایدار آلمان
⚡ سرعت بالا و پینگ عالی
"""

            await query.message.edit_text(
                text,
                reply_markup=home_keys()
            )

        else:

            await query.answer(
                "❌ هنوز عضو نشدی",
                show_alert=True
            )

    # خانه
    elif data == "home":

        text = """
✨ به Pokémon VPN خوش اومدی

🚀 سرویس های پرسرعت V2Ray
🇩🇪 سرورهای پایدار آلمان
⚡ سرعت بالا و پینگ عالی
"""

        await query.message.edit_text(
            text,
            reply_markup=home_keys()
        )

    # خرید
    elif data == "buy":

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🇩🇪 پلن اقتصادی",
                    callback_data="eco"
                )
            ],

            [
                InlineKeyboardButton(
                    "💎 پلن VIP",
                    callback_data="vip"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            "🛒 نوع پلن را انتخاب کنید",
            reply_markup=keyboard
        )

    # کیف پول
    elif data == "wallet":

        text = f"""
💰 کیف پول شما

👤 {query.from_user.first_name}

💵 موجودی:
{user_wallets[user_id]:,} تومان
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "➕ افزایش موجودی",
                    callback_data="charge"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            reply_markup=keyboard
        )

    # افزایش موجودی
    elif data == "charge":

        wallet_wait[user_id] = True

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="wallet"
                )
            ]
        ])

        await query.message.edit_text(
            "💵 مبلغ موردنظر را ارسال کنید",
            reply_markup=keyboard
        )

    # اقتصادی
    elif data == "eco":

        keys = []

        for gb, price in eco_prices.items():

            keys.append([

                InlineKeyboardButton(
                    f"🟢 {gb} • {price:,}",
                    callback_data=f"eco_{gb}"
                )
            ])

        keys.append([

            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="buy"
            )
        ])

        await query.message.edit_text(
            "🇩🇪 پلن های اقتصادی",
            reply_markup=InlineKeyboardMarkup(keys)
        )

    # vip
    elif data == "vip":

        keys = []

        for gb, price in vip_prices.items():

            keys.append([

                InlineKeyboardButton(
                    f"🟢 {gb} • {price:,}",
                    callback_data=f"vip_{gb}"
                )
            ])

        keys.append([

            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="buy"
            )
        ])

        await query.message.edit_text(
            "💎 پلن های VIP",
            reply_markup=InlineKeyboardMarkup(keys)
        )

    # خرید اقتصادی
    elif data.startswith("eco_"):

        gb = data.replace("eco_", "")
        price = eco_prices[gb]

        waiting_receipt[user_id] = {
            "type": "buy",
            "plan": gb,
            "amount": price
        }

        text = f"""
🇩🇪 Economic Plan

📦 حجم:
{gb}

💵 مبلغ:
{price:,} تومان

💳 شماره کارت:

<code>{CARD_NUMBER}</code>

📤 بعد از پرداخت رسید ارسال کنید
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "💰 خرید از کیف پول",
                    callback_data=f"buywallet_eco_{gb}"
                )
            ],

            [
                InlineKeyboardButton(
                    "📋 کپی شماره کارت",
                    switch_inline_query_current_chat=CARD_NUMBER
                )
            ],

            [
                InlineKeyboardButton(
                    "💵 کپی مبلغ",
                    switch_inline_query_current_chat=str(price)
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="eco"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    # خرید vip
    elif data.startswith("vip_"):

        gb = data.replace("vip_", "")
        price = vip_prices[gb]

        waiting_receipt[user_id] = {
            "type": "buy",
            "plan": gb,
            "amount": price
        }

        text = f"""
💎 VIP Plan

📦 حجم:
{gb}

💵 مبلغ:
{price:,} تومان

💳 شماره کارت:

<code>{CARD_NUMBER}</code>

📤 بعد از پرداخت رسید ارسال کنید
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "💰 خرید از کیف پول",
                    callback_data=f"buywallet_vip_{gb}"
                )
            ],

            [
                InlineKeyboardButton(
                    "📋 کپی شماره کارت",
                    switch_inline_query_current_chat=CARD_NUMBER
                )
            ],

            [
                InlineKeyboardButton(
                    "💵 کپی مبلغ",
                    switch_inline_query_current_chat=str(price)
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="vip"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    # خرید با کیف پول اقتصادی
    elif data.startswith("buywallet_eco_"):

        gb = data.replace("buywallet_eco_", "")
        price = eco_prices[gb]

        if user_wallets[user_id] < price:

            await query.message.edit_text(
                "❌ موجودی شما کافی نیست"
            )

            return

        user_wallets[user_id] -= price 
        save_data("balances.json", user_wallets)
        
        pending_config_user[user_id] = user_id

        await context.bot.send_message(
            ADMIN_ID,
            f"""
🛒 خرید جدید با کیف پول

👤 {query.from_user.first_name}

📦 {gb}

💵 {price:,} تومان
"""
        )

        await context.bot.send_message(
            SECOND_ADMIN_ID,
            f"""
🛒 خرید جدید با کیف پول

👤 {query.from_user.first_name}

📦 {gb}

💵 {price:,} تومان
"""
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            """
✅ خرید انجام شد

⏳ منتظر ارسال کانفیگ باشید
""",
            reply_markup=keyboard
        )

    # خرید با کیف پول vip
    elif data.startswith("buywallet_vip_"):

        gb = data.replace("buywallet_vip_", "")
        price = vip_prices[gb]

        if user_wallets[user_id] < price:

            await query.message.edit_text(
                "❌ موجودی شما کافی نیست"
            )

            return

        user_wallets[user_id] -= price
        save_data("balances.json", user_wallets)

        pending_config_user[user_id] = user_id

        await context.bot.send_message(
            ADMIN_ID,
            f"""
🛒 خرید جدید با کیف پول

👤 {query.from_user.first_name}

📦 {gb}

💵 {price:,} تومان
"""
        )

        await context.bot.send_message(
            SECOND_ADMIN_ID,
            f"""
🛒 خرید جدید با کیف پول

👤 {query.from_user.first_name}

📦 {gb}

💵 {price:,} تومان
"""
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            """
✅ خرید انجام شد

⏳ منتظر ارسال کانفیگ باشید
""",
            reply_markup=keyboard
        )


    # تست رایگان
    elif data == "free_test":

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            "❌ در حال حاضر اکانت تست موجود نیست",
            reply_markup=keyboard
        )

    # کد هدیه
    elif data == "gift":

        gift_wait[user_id] = True

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            "🎁 کد هدیه وارد کنید",
            reply_markup=keyboard
        )


    # تایید کد هدیه
    elif data.startswith("gift_accept_"):

        target_id = int(data.replace("gift_accept_", ""))

        volume = pending_gifts.get(target_id, "نامشخص")

        waiting_config[query.from_user.id] = target_id

        await context.bot.send_message(
            chat_id=target_id,
            text="✅ کد هدیه شما با موفقیت تایید شد\n⏳ در حال بررسی است و منتظر کانفینگ باشید"
        )

        await query.message.reply_text(
            "📤 کانفینگ کاربر را ارسال کنید"
        )

        await query.answer("تایید شد")

    # رد کد هدیه
    elif data.startswith("gift_reject_"):

        target_id = int(data.replace("gift_reject_", ""))

        await context.bot.send_message(
            chat_id=target_id,
            text="❌ کد هدیه شما توسط مدیر رد شد"
        )

        await query.answer("رد شد")



    # پیام همگانی
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

                    username = chat.username if chat.username else "ندارد"

                    users_buttons.append([

                        InlineKeyboardButton(
                            f"{username} | {uid}",
                            callback_data=f"pm_{uid}"
                        )

                    ])

                except:

                    users_buttons.append([

                        InlineKeyboardButton(
                            f"کاربر | {uid}",
                            callback_data=f"pm_{uid}"
                        )

                    ])

        except:

            pass

        users_buttons.append([

    InlineKeyboardButton(
        "📢 ارسال پیام به کل کاربران",
        callback_data="send_all_users"
    )

])

users_buttons.append([

    InlineKeyboardButton(
        "🔍 جستجوی کاربر",
        callback_data="find_user"
    )

])
        
        users_buttons.append([

            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="home"
            )

        ])

        keyboard = InlineKeyboardMarkup(users_buttons)

        await query.message.edit_text(
            "📢 یک کاربر انتخاب کنید یا ارسال همگانی بزنید",
            reply_markup=keyboard
        )

    elif data == "send_all_users":

        broadcast_wait[user_id] = True

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="broadcast"
                )
            ]
        ])

        await query.message.edit_text(
            "📢 پیام خود را برای کل کاربران ارسال کنید",
            reply_markup=keyboard
        )

    elif data.startswith("pm_"):

        target_id = int(data.replace("pm_", ""))

        private_message_wait[user_id] = target_id

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="broadcast"
                )
            ]
        ])

        await query.message.edit_text(
            f"✉️ پیام خود را برای کاربر {target_id} ارسال کنید",
            reply_markup=keyboard
        )


    # تعرفه
    elif data == "prices":

        text = """
سلام همکار گرامی 😃

🟣 هر گیگ 190 تومان

ID : @mak_11q

🟢 آنلاین
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🛒 خرید سرویس",
                    callback_data="buy"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            reply_markup=keyboard
        )

    # آموزش
    elif data == "help":

        text = """
📚 آموزش اتصال

1️⃣ برنامه V2rayNG نصب کنید

2️⃣ کانفیگ را کپی کنید

3️⃣ داخل برنامه Paste کنید

4️⃣ Connect بزنید
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
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

    # ارسال کانفیگ
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
🎉 کانفیگ شما آماده شد

<code>{update.message.text}</code>

🚀 اتصال پرسرعت و پایدار
""",
            parse_mode="HTML"
        )

        await update.message.reply_text(
            "✅ کانفیگ ارسال شد"
        )

        del pending_config_user[
            list(pending_config_user.keys())[-1]
        ]

        return


    # کد هدیه
    if user_id in gift_wait:

        code = update.message.text.strip()

        if user_id not in used_gifts:
            used_gifts[user_id] = []
            save_data("gifts.json", used_gifts)

        if code in used_gifts[user_id]:

            await update.message.reply_text(
                "❌ شما قبلاً از این کد هدیه استفاده کرده‌اید"
            )

            return

        if code == "mam4di":

            used_gifts[user_id].append(code)
            save_data("gifts.json", used_gifts)

            pending_gifts[user_id] = "1 گیگ"

            keyboard = InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "✅ تایید",
                        callback_data=f"gift_accept_{user_id}"
                    ),

                    InlineKeyboardButton(
                        "❌ رد کردن",
                        callback_data=f"gift_reject_{user_id}"
                    )
                ]
            ])

            await context.bot.send_message(
                ADMIN_ID,
                f"""
🎁 کد هدیه جدید ثبت شد

👤 نام:
{update.effective_user.first_name}

🆔 یوزرنیم:
@{update.effective_user.username}

📌 آیدی:
{user_id}

🎁 کد هدیه:
mam4di

📦 حجم:
1 گیگ
""",
                reply_markup=keyboard
            )

            await update.message.reply_text(
                "✅ کد هدیه شما با موفقیت ثبت شد\n📦 حجم کد هدیه شما 1 گیگ میباشد\n⏳ بعد تایید مدیر کانفینگ شما ارسال خواهد شد"
            )

            del gift_wait[user_id]

            return

        elif code == "mam4di_1k":

            used_gifts[user_id].append(code)
            save_data("gifts.json", used_gifts)

            pending_gifts[user_id] = "2 گیگ"

            keyboard = InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "✅ تایید",
                        callback_data=f"gift_accept_{user_id}"
                    ),

                    InlineKeyboardButton(
                        "❌ رد کردن",
                        callback_data=f"gift_reject_{user_id}"
                    )
                ]
            ])

            await context.bot.send_message(
                ADMIN_ID,
                f"""
🎁 کد هدیه جدید ثبت شد

👤 نام:
{update.effective_user.first_name}

🆔 یوزرنیم:
@{update.effective_user.username}

📌 آیدی:
{user_id}

🎁 کد هدیه:
mam4di_1k

📦 حجم:
2 گیگ
""",
                reply_markup=keyboard
            )

            await update.message.reply_text(
                "✅ کد هدیه شما با موفقیت ثبت شد\n📦 حجم کد هدیه شما 2 گیگ میباشد\n⏳ بعد تایید مدیر کانفینگ شما ارسال خواهد شد"
            )

            del gift_wait[user_id]

            return

        else:

    await update.message.reply_text(
        "❌ کد هدیه نامعتبر است"
    )

    if user_id in gift_wait:
        del gift_wait[user_id]

    return



    # ارسال کانفیگ توسط مدیر
    if user_id in waiting_config:

        target_user = waiting_config[user_id]

        await context.bot.send_message(
            chat_id=target_user,
            text=update.message.text
        )

        await update.message.reply_text(
            "✅ کانفینگ با موفقیت ارسال شد"
        )

        del waiting_config[user_id]

        return

    # پیام همگانی
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
                "✅ پیام شما با موفقیت برای کاربران ارسال شد"
            )

        except:

            await update.message.reply_text(
                "❌ لیست کاربران پیدا نشد"
            )

        del broadcast_wait[user_id]

        return



    # پیام خصوصی مدیر
    if user_id in private_message_wait:

        target_user = private_message_wait[user_id]

        await context.bot.send_message(
            chat_id=target_user,
            text=update.message.text
        )

        await update.message.reply_text(
            "✅ پیام شما با موفقیت ارسال شد"
        )

        del private_message_wait[user_id]

        return


    # مبلغ کیف پول
    if user_id in wallet_wait:

        try:
            amount = int(update.message.text)

        except:

            await update.message.reply_text(
                "❌ فقط عدد وارد کنید"
            )

            return

        waiting_receipt[user_id] = {
            "type": "wallet",
            "amount": amount
        }

        text = f"""
💰 افزایش موجودی کیف پول

💵 مبلغ:
{amount:,} تومان

💳 شماره کارت:

<code>{CARD_NUMBER}</code>

📤 بعد از واریز رسید ارسال کنید
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "📋 کپی شماره کارت",
                    switch_inline_query_current_chat=CARD_NUMBER
                )
            ],

            [
                InlineKeyboardButton(
                    "💵 کپی مبلغ",
                    switch_inline_query_current_chat=str(amount)
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
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

        txt = f"شارژ کیف پول\n{info['amount']:,} تومان"

    else:

        txt = f"{info['plan']} | {info['amount']:,} تومان"

    caption = f"""
📥 رسید جدید

👤 {update.effective_user.first_name}

🆔 @{update.effective_user.username}

📌 ID:
{user_id}

🛒 اطلاعات:
{txt}
"""

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "✅ تایید",
                callback_data=f"accept_{user_id}"
            ),

            InlineKeyboardButton(
                "❌ رد",
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
                "🔙 بازگشت",
                callback_data="home"
            )
        ]
    ])

    await update.message.reply_text(
        "✅ رسید شما ثبت شد\n⏳ منتظر تایید مدیریت باشید",
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
