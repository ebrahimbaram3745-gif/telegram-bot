import os
import json

from flask import Flask
from threading import Thread

app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is running"

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
import json
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
    " 1G |  30D |  50T": 50000,
    " 2G |  30D |  95T": 95000,
    " 3G |  30D |  140T": 140000,
    " 4G |  30D |  190T": 190000,
    " 5G |  30D |  235T": 235000,
    " 6G |  30D |  287T": 287000,
    " 7G |  30D |  340T": 340000,
    " 8G |  30D |  387T": 387000,
    " 9G |  30D |  438T": 438000,
    " 10G |  30D |  490T": 490000,
}

vip_prices = {
    " 70G |  30D |  690T": 690000,
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
                "  ",
                callback_data="buy"
            )
        ],

        [
            InlineKeyboardButton(
                "  ",
                callback_data="wallet"
            ),

            InlineKeyboardButton(
                " ",
                url=f"https://t.me/{SUPPORT_ID}"
            )
        ],

        [
            InlineKeyboardButton(
                "  ",
                callback_data="gift"
            ),

            InlineKeyboardButton(
                "   ",
                callback_data="free_test"
            )
        ],

        [
            InlineKeyboardButton(
                "  ",
                callback_data="help"
            ),

            InlineKeyboardButton(
                "  ",
                callback_data="prices"
            )
        ],

        [
            InlineKeyboardButton(
                "   ",
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
                    "   ",
                    url=f"https://t.me/{CHANNEL_USERNAME}"
                )
            ],

            [
                InlineKeyboardButton(
                    "  ",
                    callback_data="check_join"
                )
            ]
        ])

        await update.message.reply_text(
            "    ",
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

    text = """
  Pokmon VPN  

    V2Ray
   
     
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

    #  
    if data.startswith("accept_"):

        target_user = int(data.split("_")[1])

        info = waiting_receipt.get(target_user)

        if info and info["type"] == "wallet":

            amount = info["amount"]

            user_wallets[target_user] += amount

            await context.bot.send_message(
                target_user,
                f"""
     

 :
{amount:,} 

  :
{user_wallets[target_user]:,} 
"""
            )

            await query.answer(
                "    ",
                show_alert=True
            )

        else:

            pending_config_user[target_user] = target_user

            await context.bot.send_message(
                target_user,
                """
    

     
"""
            )

            await query.answer(
                "  ",
                show_alert=True
            )

    #  
    elif data.startswith("reject_"):

        target_user = int(data.split("_")[1])

        await context.bot.send_message(
            target_user,
            """
    

    
"""
        )

    #  
    elif data == "check_join":

        ok = await joined(
            query.from_user.id,
            context.bot
        )

        if ok:

            text = """
  Pokmon VPN  

    V2Ray
   
     
"""

            await query.message.edit_text(
                text,
                reply_markup=home_keys()
            )

        else:

            await query.answer(
                "   ",
                show_alert=True
            )

    # 
    elif data == "home":

        text = """
  Pokmon VPN  

    V2Ray
   
     
"""

        await query.message.edit_text(
            text,
            reply_markup=home_keys()
        )

    # 
    elif data == "buy":

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "  ",
                    callback_data="eco"
                )
            ],

            [
                InlineKeyboardButton(
                    "  VIP",
                    callback_data="vip"
                )
            ],

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            "     ",
            reply_markup=keyboard
        )

    #  
    elif data == "wallet":

        text = f"""
   

 {query.from_user.first_name}

 :
{user_wallets[user_id]:,} 
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "  ",
                    callback_data="charge"
                )
            ],

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            reply_markup=keyboard
        )

    #  
    elif data == "charge":

        wallet_wait[user_id] = True

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="wallet"
                )
            ]
        ])

        await query.message.edit_text(
            "     ",
            reply_markup=keyboard
        )

    # 
    elif data == "eco":

        keys = []

        for gb, price in eco_prices.items():

            keys.append([

                InlineKeyboardButton(
                    f" {gb}  {price:,}",
                    callback_data=f"eco_{gb}"
                )
            ])

        keys.append([

            InlineKeyboardButton(
                " ",
                callback_data="buy"
            )
        ])

        await query.message.edit_text(
            "   ",
            reply_markup=InlineKeyboardMarkup(keys)
        )

    # vip
    elif data == "vip":

        keys = []

        for gb, price in vip_prices.items():

            keys.append([

                InlineKeyboardButton(
                    f" {gb}  {price:,}",
                    callback_data=f"vip_{gb}"
                )
            ])

        keys.append([

            InlineKeyboardButton(
                " ",
                callback_data="buy"
            )
        ])

        await query.message.edit_text(
            "   VIP",
            reply_markup=InlineKeyboardMarkup(keys)
        )

    #  
    elif data.startswith("eco_"):

        gb = data.replace("eco_", "")
        price = eco_prices[gb]

        waiting_receipt[user_id] = {
            "type": "buy",
            "plan": gb,
            "amount": price
        }

        text = f"""
 Economic Plan

 :
{gb}

 :
{price:,} 

  :

<code>{CARD_NUMBER}</code>

      
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "    ",
                    callback_data=f"buywallet_eco_{gb}"
                )
            ],

            [
                InlineKeyboardButton(
                    "   ",
                    switch_inline_query_current_chat=CARD_NUMBER
                )
            ],

            [
                InlineKeyboardButton(
                    "  ",
                    switch_inline_query_current_chat=str(price)
                )
            ],

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="eco"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    #  vip
    elif data.startswith("vip_"):

        gb = data.replace("vip_", "")
        price = vip_prices[gb]

        waiting_receipt[user_id] = {
            "type": "buy",
            "plan": gb,
            "amount": price
        }

        text = f"""
 VIP Plan

 :
{gb}

 :
{price:,} 

  :

<code>{CARD_NUMBER}</code>

      
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "    ",
                    callback_data=f"buywallet_vip_{gb}"
                )
            ],

            [
                InlineKeyboardButton(
                    "   ",
                    switch_inline_query_current_chat=CARD_NUMBER
                )
            ],

            [
                InlineKeyboardButton(
                    "  ",
                    switch_inline_query_current_chat=str(price)
                )
            ],

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="vip"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    #     
    elif data.startswith("buywallet_eco_"):

        gb = data.replace("buywallet_eco_", "")
        price = eco_prices[gb]

        if user_wallets[user_id] < price:

            await query.message.edit_text(
                "    "
            )

            return

        user_wallets[user_id] -= price

        pending_config_user[user_id] = user_id

        await context.bot.send_message(
            ADMIN_ID,
            f"""
     

 {query.from_user.first_name}

 {gb}

 {price:,} 
"""
        )

        await context.bot.send_message(
            SECOND_ADMIN_ID,
            f"""
     

 {query.from_user.first_name}

 {gb}

 {price:,} 
"""
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            """
   

    
""",
            reply_markup=keyboard
        )

    #     vip
    elif data.startswith("buywallet_vip_"):

        gb = data.replace("buywallet_vip_", "")
        price = vip_prices[gb]

        if user_wallets[user_id] < price:

            await query.message.edit_text(
                "    "
            )

            return

        user_wallets[user_id] -= price

        pending_config_user[user_id] = user_id

        await context.bot.send_message(
            ADMIN_ID,
            f"""
     

 {query.from_user.first_name}

 {gb}

 {price:,} 
"""
        )

        await context.bot.send_message(
            SECOND_ADMIN_ID,
            f"""
     

 {query.from_user.first_name}

 {gb}

 {price:,} 
"""
        )

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            """
   

    
""",
            reply_markup=keyboard
        )


    #  
    elif data == "free_test":

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            "       ",
            reply_markup=keyboard
        )

    #  
    elif data == "gift":

        gift_wait[user_id] = True

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            "    ",
            reply_markup=keyboard
        )


    #   
    elif data.startswith("gift_accept_"):

        target_id = int(data.replace("gift_accept_", ""))

        volume = pending_gifts.get(target_id, "")

        waiting_config[query.from_user.id] = target_id

        await context.bot.send_message(
            chat_id=target_id,
            text="       \n        "
        )

        await query.message.reply_text(
            "     "
        )

        await query.answer(" ")

    #   
    elif data.startswith("gift_reject_"):

        target_id = int(data.replace("gift_reject_", ""))

        await context.bot.send_message(
            chat_id=target_id,
            text="       "
        )

        await query.answer(" ")



    #  
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

                    username = chat.username if chat.username else ""

                    users_buttons.append([

                        InlineKeyboardButton(
                            f"{username} | {uid}",
                            callback_data=f"pm_{uid}"
                        )

                    ])

                except:

                    users_buttons.append([

                        InlineKeyboardButton(
                            f" | {uid}",
                            callback_data=f"pm_{uid}"
                        )

                    ])

        except:

            pass

        users_buttons.append([

            InlineKeyboardButton(
                "     ",
                callback_data="send_all_users"
            )

        ])

        users_buttons.append([

            InlineKeyboardButton(
                " ",
                callback_data="home"
            )

        ])

        keyboard = InlineKeyboardMarkup(users_buttons)

        await query.message.edit_text(
            "        ",
            reply_markup=keyboard
        )

    elif data == "send_all_users":

        broadcast_wait[user_id] = True

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="broadcast"
                )
            ]
        ])

        await query.message.edit_text(
            "        ",
            reply_markup=keyboard
        )

    elif data.startswith("pm_"):

        target_id = int(data.replace("pm_", ""))

        private_message_wait[user_id] = target_id

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="broadcast"
                )
            ]
        ])

        await query.message.edit_text(
            f"      {target_id}  ",
            reply_markup=keyboard
        )


    # 
    elif data == "prices":

        text = """
   

   190 

ID : @mak_11q

 
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "  ",
                    callback_data="buy"
                )
            ],

            [
                InlineKeyboardButton(
                    " ",
                    callback_data="home"
                )
            ]
        ])

        await query.message.edit_text(
            text,
            reply_markup=keyboard
        )

    # 
    elif data == "help":

        text = """
  

1  V2rayNG  

2    

3   Paste 

4 Connect 
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    " ",
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

    #  
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
    

<code>{update.message.text}</code>

    
""",
            parse_mode="HTML"
        )

        await update.message.reply_text(
            "   "
        )

        del pending_config_user[
            list(pending_config_user.keys())[-1]
        ]

        return


    #  
    if user_id in gift_wait:

        code = update.message.text.strip()

        if user_id not in used_gifts:
            used_gifts[user_id] = []

        if code in used_gifts[user_id]:

            await update.message.reply_text(
                "        "
            )

            return

        if code == "mam4di":

            used_gifts[user_id].append(code)

            save_data("gifts.json", used_gifts)

            pending_gifts[user_id] = "1 "

            keyboard = InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        " ",
                        callback_data=f"gift_accept_{user_id}"
                    ),

                    InlineKeyboardButton(
                        "  ",
                        callback_data=f"gift_reject_{user_id}"
                    )
                ]
            ])

            await context.bot.send_message(
                ADMIN_ID,
                f"""
     

 :
{update.effective_user.first_name}

 :
@{update.effective_user.username}

 :
{user_id}

  :
mam4di

 :
1 
""",
                reply_markup=keyboard
            )

            await update.message.reply_text(
                "       \n     1  \n        "
            )

            del gift_wait[user_id]

            return

        elif code == "mam4di_1k":

            used_gifts[user_id].append(code)

            save_data("gifts.json", used_gifts)

            pending_gifts[user_id] = "2 "

            keyboard = InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        " ",
                        callback_data=f"gift_accept_{user_id}"
                    ),

                    InlineKeyboardButton(
                        "  ",
                        callback_data=f"gift_reject_{user_id}"
                    )
                ]
            ])

            await context.bot.send_message(
                ADMIN_ID,
                f"""
     

 :
{update.effective_user.first_name}

 :
@{update.effective_user.username}

 :
{user_id}

  :
mam4di_1k

 :
2 
""",
                reply_markup=keyboard
            )

            await update.message.reply_text(
                "       \n     2  \n        "
            )

            del gift_wait[user_id]

            return

        else:

            await update.message.reply_text(
                "    "
            )

            return



    #    
    if user_id in waiting_config:

        target_user = waiting_config[user_id]

        await context.bot.send_message(
            chat_id=target_user,
            text=update.message.text
        )

        await update.message.reply_text(
            "     "
        )

        del waiting_config[user_id]

        return

    #  
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
                "        "
            )

        except:

            await update.message.reply_text(
                "    "
            )

        del broadcast_wait[user_id]

        return



    #   
    if user_id in private_message_wait:

        target_user = private_message_wait[user_id]

        await context.bot.send_message(
            chat_id=target_user,
            text=update.message.text
        )

        await update.message.reply_text(
            "      "
        )

        del private_message_wait[user_id]

        return


    #   
    if user_id in wallet_wait:

        try:
            amount = int(update.message.text)

        except:

            await update.message.reply_text(
                "    "
            )

            return

        waiting_receipt[user_id] = {
            "type": "wallet",
            "amount": amount
        }

        text = f"""
    

 :
{amount:,} 

  :

<code>{CARD_NUMBER}</code>

      
"""

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "   ",
                    switch_inline_query_current_chat=CARD_NUMBER
                )
            ],

            [
                InlineKeyboardButton(
                    "  ",
                    switch_inline_query_current_chat=str(amount)
                )
            ],

            [
                InlineKeyboardButton(
                    " ",
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

        txt = f"  \n{info['amount']:,} "

    else:

        txt = f"{info['plan']} | {info['amount']:,} "

    caption = f"""
  

 {update.effective_user.first_name}

 @{update.effective_user.username}

 ID:
{user_id}

 :
{txt}
"""

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                " ",
                callback_data=f"accept_{user_id}"
            ),

            InlineKeyboardButton(
                " ",
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
                " ",
                callback_data="home"
            )
        ]
    ])

    await update.message.reply_text(
        "    \n    ",
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
