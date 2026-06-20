import os
import json
import requests
import uuid as uuid_lib
import re as re_mod

CE_CHART="📊"
CE_FREE="🆓"
CE_CHECK="✅"
CE_DIAMOND="💎"
CE_TIME="⏳"


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

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "Pokemon_VPN"
SUPPORT_ID = "mak_11q"
ADMIN_ID = 7363962357
SECOND_ADMIN_ID = 8489061532
CARD_NUMBER = "6219861449318822"

# ─── تنظیمات پنل Nahan ───────────────────────────────────────────
NAHAN_URL = "https://proud-dew-0f73.itx-mm2di1000.workers.dev"
NAHAN_API_ROUTE = "sync"
NAHAN_API_ROUTE = "dash"
NAHAN_PASSWORD = "admin"

def nahan_build_sub_url(username: str) -> str:
    """
    پنل Nahan هیچ REST API خارجی برای ساخت کاربر ندارد.
    کاربر باید از داشبورد اضافه شود؛ سپس لینک سابسکریپشن این‌طور ساخته می‌شه:
      https://<worker>/<route>?sub=<username>
    این تابع فقط لینک اشتراک را می‌سازه.
    """
    return f"{NAHAN_URL}/{NAHAN_API_ROUTE}?sub={username}"

# ─── داده‌های حافظه‌ای (در RAM) ───────────────────────────────────
waiting_receipt     = {}
wallet_wait         = {}
user_wallets        = load_data("balances.json")
referrals           = load_data("referrals.json")
gift_wait           = {}
used_gifts          = load_data("gifts.json")
pending_gifts       = {}
broadcast_wait      = {}
private_message_wait= {}
trx_wait            = {}
trx_payment_data    = {}
payment_select      = {}
wallet_amount       = {}
banned_users        = load_data("banned_users.json")
ban_wait            = {}
unban_wait          = {}

# ─── ذخیره سفارش‌های در انتظار روی دیسک ─────────────────────────
ORDERS_FILE = "pending_orders.json"

def load_orders():
    return load_data(ORDERS_FILE)

def save_orders(orders):
    save_data(ORDERS_FILE, orders)

# ─── قیمت‌ها ──────────────────────────────────────────────────────
def get_trx_price_toman():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=tron&vs_currencies=usd",
            timeout=10
        ).json()
        trx_usd = float(r["tron"]["usd"])
        usdt = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=irr",
            timeout=10
        ).json()
        usdt_irr = float(usdt["tether"]["irr"])
        return (trx_usd * usdt_irr) / 10
    except:
        return 3000

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
    "📊 320G | ⏳ 180D | 💰 1390T": 1390000,
}

wireguard_prices = {
    "📊 36G | ⏳ 30D | 💰 459T | 1👤": 459000,
    "📊 78G | ⏳ 60D | 💰 766T | 1👤": 766000,
    "📊 127G | ⏳ 90D | 💰 991T | 1👤": 991000,
    "📊 300G | ⏳ 180D | 💰 1609T | 1👤": 1609000,
}

# ─── کمکی‌ها ──────────────────────────────────────────────────────
async def joined(user_id, bot):
    try:
        member = await bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def parse_plan(plan_name: str, default_gb=10, default_days=30):
    """حجم و روز را از نام پلن استخراج می‌کند"""
    gb = default_gb
    days = default_days
    m_gb = re_mod.search(r'(\d+)G', plan_name)
    m_day = re_mod.search(r'(\d+)D', plan_name)
    if m_gb:
        gb = int(m_gb.group(1))
    if m_day:
        days = int(m_day.group(1))
    return gb, days

def home_keys():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید سرویس", callback_data="buy")],
        [
            InlineKeyboardButton("💰 کیف پول", callback_data="wallet"),
            InlineKeyboardButton("📞 پشتیبانی", url=f"https://t.me/{SUPPORT_ID}")
        ],
        [
            InlineKeyboardButton("🎁 کد هدیه", callback_data="gift"),
            InlineKeyboardButton("🆓 تست اکانت رایگان", callback_data="free_test")
        ],
        [
            InlineKeyboardButton("👥 زیرمجموعه گیری", callback_data="referral"),
            InlineKeyboardButton("📋 تعرفه قیمت‌ها", callback_data="prices")
        ],
        [InlineKeyboardButton("📢 ارسال پیام همگانی", callback_data="broadcast")]
    ])

# ─── پیام تأیید کانفیگ برای کاربر ───────────────────────────────
def config_message(plan_name: str, gb: int, days: int, sub_url: str) -> str:
    return (
        f"✅ سرویس شما آماده است!\n\n"
        f"📦 پلن: {plan_name}\n"
        f"📊 حجم: {gb} گیگ\n"
        f"⏳ مدت: {days} روز\n\n"
        f"🔗 لینک اشتراک شما:\n"
        f"<code>{sub_url}</code>\n\n"
        f"📲 این لینک را در اپ وارد کنید\n"
        f"🚀 اتصال پرسرعت و پایدار\n\n"
        f"⚠️ <b>توجه:</b> ابتدا کاربر را در پنل با نام "
        f"<code>{sub_url.split('sub=')[-1]}</code> بسازید تا این لینک فعال شود."
    )

# ─── /start ───────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ok = await joined(update.effective_user.id, context.bot)
    if not ok:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ عضو شدم", callback_data="check_join")]
        ])
        await update.message.reply_text("❌ ابتدا عضو کانال شوید", reply_markup=keyboard)
        return

    user_id = update.effective_user.id

    if context.args:
        try:
            ref_code = context.args[0]
            if ref_code.isdigit() and int(ref_code) != user_id:
                referrals.setdefault(str(user_id), {})
                if not referrals[str(user_id)].get("referred_by"):
                    referrals[str(user_id)]["referred_by"] = int(ref_code)
                    user_wallets[str(int(ref_code))] = int(user_wallets.get(str(int(ref_code)), 0)) + 3000
                    referrals.setdefault(str(int(ref_code)), {})
                    referrals[str(int(ref_code))]["count"] = int(referrals[str(int(ref_code))].get("count", 0)) + 1
                    save_data("balances.json", user_wallets)
                    save_data("referrals.json", referrals)
        except:
            pass

    try:
        with open("users.txt", "a+", encoding="utf-8") as f:
            f.seek(0)
            users = f.read().splitlines()
            if str(user_id) not in users:
                f.write(f"{user_id}\n")
    except:
        pass

    if str(user_id) not in user_wallets and user_id not in user_wallets:
        user_wallets[str(user_id)] = 0
        save_data("balances.json", user_wallets)

    text = (
        "✨ به Pokémon VPN خوش اومدی\n\n"
        "🚀 سرویس های پرسرعت V2Ray\n"
        "🇩🇪 سرورهای پایدار آلمان\n"
        "⚡ سرعت بالا و پینگ عالی"
    )
    await update.message.reply_text(text, reply_markup=home_keys())

# ─── دکمه‌ها ──────────────────────────────────────────────────────
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data  = query.data
    await query.answer()

    user_id = query.from_user.id

    if data == "ban_user":
        ban_wait[user_id] = True
        await query.message.reply_text("آیدی عددی کاربر را وارد کنید:")
        return

    if data == "unban_user":
        unban_wait[user_id] = True
        await query.message.reply_text("آیدی عددی کاربر را وارد کنید:")
        return

    # اطمینان از وجود کیف پول
    uid_key = str(user_id)
    if uid_key not in user_wallets and user_id not in user_wallets:
        user_wallets[uid_key] = 0
        save_data("balances.json", user_wallets)

    def get_balance(uid):
        return int(user_wallets.get(str(uid), user_wallets.get(uid, 0)))

    def set_balance(uid, val):
        user_wallets[str(uid)] = val
        if uid in user_wallets:
            user_wallets[uid] = val
        save_data("balances.json", user_wallets)

    # ── تایید رسید ──────────────────────────────────────────────
    if data.startswith("accept_"):
        target_user = int(data.split("_")[1])

        # بارگذاری سفارش از دیسک (در صورت ری‌استارت)
        orders = load_orders()
        info = waiting_receipt.get(target_user) or orders.get(str(target_user))

        if not info:
            await query.answer("❌ اطلاعات سفارش یافت نشد (ممکن است منقضی شده باشد)", show_alert=True)
            return

        if info["type"] == "wallet":
            amount = info["amount"]
            new_bal = get_balance(target_user) + amount
            set_balance(target_user, new_bal)

            await context.bot.send_message(
                target_user,
                f"✅ کیف پول شما شارژ شد\n\n💰 مبلغ: {amount:,} تومان\n💵 موجودی جدید: {new_bal:,} تومان"
            )
            await query.answer("کیف پول شارژ شد ✅", show_alert=True)

        else:
            plan_name = info.get("plan", "")
            gb, days  = parse_plan(plan_name)
            username  = f"tg{target_user}"
            sub_url   = nahan_build_sub_url(username)

            # اطلاع به ادمین برای ساخت کاربر در پنل
            await context.bot.send_message(
                ADMIN_ID,
                f"🔔 <b>ساخت کاربر جدید در پنل</b>\n\n"
                f"👤 آیدی تلگرام: <code>{target_user}</code>\n"
                f"📦 پلن: {plan_name}\n"
                f"📊 حجم: {gb} گیگ | ⏳ {days} روز\n\n"
                f"▶️ نام کاربر در پنل:\n<code>{username}</code>\n\n"
                f"لینک اشتراک که برای کاربر ارسال شد:\n<code>{sub_url}</code>",
                parse_mode="HTML"
            )

            # ارسال لینک به کاربر (ادمین باید کاربر را در پنل بسازد)
            await context.bot.send_message(
                target_user,
                config_message(plan_name, gb, days, sub_url),
                parse_mode="HTML"
            )
            await query.answer("✅ تایید شد - اطلاع به ادمین ارسال شد", show_alert=True)

        # پاکسازی
        waiting_receipt.pop(target_user, None)
        orders.pop(str(target_user), None)
        save_orders(orders)
        return

    # ── رد رسید ─────────────────────────────────────────────────
    elif data.startswith("reject_"):
        target_user = int(data.split("_")[1])
        waiting_receipt.pop(target_user, None)
        orders = load_orders()
        orders.pop(str(target_user), None)
        save_orders(orders)
        await context.bot.send_message(
            target_user,
            "❌ پرداخت شما رد شد\n\n📞 با پشتیبانی تماس بگیرید"
        )

    # ── چک عضویت ────────────────────────────────────────────────
    elif data == "check_join":
        ok = await joined(query.from_user.id, context.bot)
        if ok:
            await query.message.edit_text(
                "✨ به Pokémon VPN خوش اومدی\n\n🚀 سرویس های پرسرعت V2Ray\n🇩🇪 سرورهای پایدار آلمان\n⚡ سرعت بالا و پینگ عالی",
                reply_markup=home_keys()
            )
        else:
            await query.answer("❌ هنوز عضو نشدی", show_alert=True)

    # ── خانه ────────────────────────────────────────────────────
    elif data == "home":
        await query.message.edit_text(
            "✨ به Pokémon VPN خوش اومدی\n\n🚀 سرویس های پرسرعت V2Ray\n🇩🇪 سرورهای پایدار آلمان\n⚡ سرعت بالا و پینگ عالی",
            reply_markup=home_keys()
        )

    # ── خرید ────────────────────────────────────────────────────
    elif data == "buy":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇩🇪 پلن اقتصادی", callback_data="eco")],
            [InlineKeyboardButton("💎 پلن VIP", callback_data="vip")],
            [InlineKeyboardButton("⚡ سرویس WireGuard", callback_data="wireguard")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="home")]
        ])
        await query.message.edit_text("🛒 نوع پلن را انتخاب کنید", reply_markup=keyboard)

    # ── کیف پول ─────────────────────────────────────────────────
    elif data == "wallet":
        bal = get_balance(user_id)
        text = f"💰 کیف پول شما\n\n👤 {query.from_user.first_name}\n\n💵 موجودی:\n{bal:,} تومان"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ شارژ کیف پول", callback_data="charge")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="home")]
        ])
        await query.message.edit_text(text, reply_markup=keyboard)

    elif data == "charge":
        wallet_wait[user_id] = True
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="wallet")]])
        await query.message.edit_text("مبلغ مورد نظر را وارد کنید", reply_markup=keyboard)

    # ── پلن‌ها ──────────────────────────────────────────────────
    elif data == "eco":
        keys = [[InlineKeyboardButton(f"🟢 {gb} • {price:,}", callback_data=f"eco_{gb}")] for gb, price in eco_prices.items()]
        keys.append([InlineKeyboardButton("🔙 بازگشت", callback_data="buy")])
        await query.message.edit_text("🇩🇪 پلن های اقتصادی", reply_markup=InlineKeyboardMarkup(keys))

    elif data == "wireguard":
        keys = [[InlineKeyboardButton(f"⚡ {gb} • {price:,}", callback_data=f"wg_{gb}")] for gb, price in wireguard_prices.items()]
        keys.append([InlineKeyboardButton("🔙 بازگشت", callback_data="buy")])
        await query.message.edit_text("⚡ پلن های WireGuard", reply_markup=InlineKeyboardMarkup(keys))

    elif data == "vip":
        keys = [[InlineKeyboardButton(f"🟢 {gb} • {price:,}", callback_data=f"vip_{gb}")] for gb, price in vip_prices.items()]
        keys.append([InlineKeyboardButton("🔙 بازگشت", callback_data="buy")])
        await query.message.edit_text("💎 پلن های VIP", reply_markup=InlineKeyboardMarkup(keys))

    # ── انتخاب روش پرداخت ───────────────────────────────────────
    elif data.startswith("eco_"):
        gb = data[4:]
        price = eco_prices.get(gb)
        if price is None: return
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 کارت به کارت", callback_data=f"card_eco_{gb}")],
            [InlineKeyboardButton("💎 پرداخت ارزی", callback_data=f"trx_eco_{gb}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="eco")]
        ])
        await query.message.edit_text("💳 روش پرداخت را انتخاب کنید", reply_markup=keyboard)

    elif data.startswith("wg_"):
        gb = data[3:]
        price = wireguard_prices.get(gb)
        if price is None: return
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 کارت به کارت", callback_data=f"card_wireguard_{gb}")],
            [InlineKeyboardButton("💎 پرداخت ارزی", callback_data=f"trx_wireguard_{gb}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="wireguard")]
        ])
        await query.message.edit_text("💳 روش پرداخت را انتخاب کنید", reply_markup=keyboard)

    elif data.startswith("vip_"):
        gb = data[4:]
        price = vip_prices.get(gb)
        if price is None: return
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 کارت به کارت", callback_data=f"card_vip_{gb}")],
            [InlineKeyboardButton("💎 پرداخت ارزی", callback_data=f"trx_vip_{gb}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="vip")]
        ])
        await query.message.edit_text("💳 روش پرداخت را انتخاب کنید", reply_markup=keyboard)

    # ── کارت به کارت ────────────────────────────────────────────
    elif data.startswith("card_eco_"):
        gb = data[9:]
        price = eco_prices.get(gb)
        if price is None: return
        _store_receipt(user_id, "buy", gb, price)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 خرید از کیف پول", callback_data=f"buywallet_eco_{gb}")],
            [InlineKeyboardButton("📋 کپی شماره کارت", switch_inline_query_current_chat=CARD_NUMBER)],
            [InlineKeyboardButton("💵 کپی مبلغ", switch_inline_query_current_chat=str(price))],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="eco")]
        ])
        await query.message.edit_text(
            f"🇩🇪 Economic Plan\n\n📦 حجم:\n{gb}\n\n💵 مبلغ:\n{price:,} تومان\n\n💳 شماره کارت:\n\n<code>{CARD_NUMBER}</code>\n\n📤 بعد از پرداخت رسید ارسال کنید",
            parse_mode="HTML", reply_markup=keyboard
        )

    elif data.startswith("card_vip_"):
        gb = data[9:]
        price = vip_prices.get(gb)
        if price is None: return
        _store_receipt(user_id, "buy", gb, price)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 خرید از کیف پول", callback_data=f"buywallet_vip_{gb}")],
            [InlineKeyboardButton("📋 کپی شماره کارت", switch_inline_query_current_chat=CARD_NUMBER)],
            [InlineKeyboardButton("💵 کپی مبلغ", switch_inline_query_current_chat=str(price))],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="vip")]
        ])
        await query.message.edit_text(
            f"💎 VIP Plan\n\n📦 حجم:\n{gb}\n\n💵 مبلغ:\n{price:,} تومان\n\n💳 شماره کارت:\n\n<code>{CARD_NUMBER}</code>\n\n📤 بعد از پرداخت رسید ارسال کنید",
            parse_mode="HTML", reply_markup=keyboard
        )

    elif data.startswith("card_wireguard_"):
        gb = data[15:]
        price = wireguard_prices.get(gb)
        if price is None: return
        _store_receipt(user_id, "buy", "WireGuard | " + gb, price)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 خرید از کیف پول", callback_data=f"buywallet_wireguard_{gb}")],
            [InlineKeyboardButton("📋 کپی شماره کارت", switch_inline_query_current_chat=CARD_NUMBER)],
            [InlineKeyboardButton("💵 کپی مبلغ", switch_inline_query_current_chat=str(price))],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="wireguard")]
        ])
        await query.message.edit_text(
            f"⚡ WireGuard\n\n📦 پلن:\n{gb}\n\n💵 مبلغ:\n{price:,} تومان\n\n💳 شماره کارت:\n\n<code>{CARD_NUMBER}</code>\n\n📤 بعد از پرداخت رسید ارسال کنید",
            parse_mode="HTML", reply_markup=keyboard
        )

    # ── پرداخت ارزی ─────────────────────────────────────────────
    elif data.startswith("trx_eco_"):
        gb = data[8:]
        price = eco_prices.get(gb)
        if price is None: return
        _store_receipt(user_id, "buy", gb, price)
        trx = round(price / get_trx_price_toman(), 2)
        await query.message.edit_text(
            f"💎 فاکتور پرداخت ارزی\n\n💳 معادل ریالی:\n{price:,} تومان\n\n💸 مبلغ ارزی قابل پرداخت:\n💰 {trx} TRX\n\n👇 آدرس کیف پول:\nفعلا ندارد\n\n⚠️ دقیقاً مبلغ ذکر شده را واریز کنید.\n\n✅ پس از واریز، عکس رسید بفرستید"
        )

    elif data.startswith("trx_vip_"):
        gb = data[8:]
        price = vip_prices.get(gb)
        if price is None: return
        _store_receipt(user_id, "buy", gb, price)
        trx = round(price / get_trx_price_toman(), 2)
        await query.message.edit_text(
            f"💎 فاکتور پرداخت ارزی\n\n💳 معادل ریالی:\n{price:,} تومان\n\n💸 مبلغ ارزی قابل پرداخت:\n💰 {trx} TRX\n\n👇 آدرس کیف پول:\nفعلا ندارد\n\n⚠️ دقیقاً مبلغ ذکر شده را واریز کنید.\n\n✅ پس از واریز، عکس رسید بفرستید"
        )

    elif data.startswith("trx_wireguard_"):
        gb = data[14:]
        price = wireguard_prices.get(gb)
        if price is None: return
        _store_receipt(user_id, "buy", "WireGuard | " + gb, price)
        trx = round(price / get_trx_price_toman(), 2)
        await query.message.edit_text(
            f"💎 فاکتور پرداخت ارزی\n\n💳 معادل ریالی:\n{price:,} تومان\n\n💸 مبلغ ارزی قابل پرداخت:\n💰 {trx} TRX\n\n👇 آدرس کیف پول:\nفعلا ندارد\n\n✅ پس از واریز، عکس رسید بفرستید"
        )

    # ── خرید با کیف پول ─────────────────────────────────────────
    elif data.startswith("buywallet_eco_"):
        gb = data[14:]
        price = eco_prices.get(gb)
        if price is None: return
        await _wallet_buy(query, context, user_id, gb, price, "eco", get_balance, set_balance)

    elif data.startswith("buywallet_vip_"):
        gb = data[14:]
        price = vip_prices.get(gb)
        if price is None: return
        await _wallet_buy(query, context, user_id, gb, price, "vip", get_balance, set_balance)

    elif data.startswith("buywallet_wireguard_"):
        gb = data[20:]
        price = wireguard_prices.get(gb)
        if price is None: return
        plan = "WireGuard | " + gb
        await _wallet_buy(query, context, user_id, gb, price, "wireguard", get_balance, set_balance, plan_override=plan)

    # ── تست رایگان ──────────────────────────────────────────────
    elif data == "free_test":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="home")]])
        await query.message.edit_text("❌ در حال حاضر اکانت تست موجود نیست", reply_markup=keyboard)

    # ── کد هدیه ─────────────────────────────────────────────────
    elif data == "gift":
        gift_wait[user_id] = True
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="home")]])
        await query.message.edit_text("🎁 کد هدیه وارد کنید", reply_markup=keyboard)

    elif data.startswith("gift_accept_"):
        target_id = int(data[12:])
        volume    = pending_gifts.get(target_id, "1 گیگ")
        gb, days  = parse_plan(volume, default_gb=1)
        username  = f"tg{target_id}"
        sub_url   = nahan_build_sub_url(username)

        await context.bot.send_message(
            ADMIN_ID,
            f"🎁 <b>ساخت کاربر هدیه در پنل</b>\n\n"
            f"👤 آیدی تلگرام: <code>{target_id}</code>\n"
            f"📦 حجم: {volume} | ⏳ {days} روز\n\n"
            f"▶️ نام کاربر در پنل:\n<code>{username}</code>\n\n"
            f"لینک اشتراک:\n<code>{sub_url}</code>",
            parse_mode="HTML"
        )

        await context.bot.send_message(
            target_id,
            config_message(f"هدیه {volume}", gb, days, sub_url),
            parse_mode="HTML"
        )
        await query.answer("تایید شد")

    elif data.startswith("gift_reject_"):
        target_id = int(data[12:])
        await context.bot.send_message(target_id, "❌ کد هدیه شما توسط مدیر رد شد")
        await query.answer("رد شد")

    # ── پیام همگانی ─────────────────────────────────────────────
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
                    uname = chat.username if chat.username else "ندارد"
                    users_buttons.append([InlineKeyboardButton(f"{uname} | {uid}", callback_data=f"pm_{uid}")])
                except:
                    users_buttons.append([InlineKeyboardButton(f"کاربر | {uid}", callback_data=f"pm_{uid}")])
        except:
            pass
        users_buttons.append([InlineKeyboardButton("📢 ارسال پیام به کل کاربران", callback_data="send_all_users")])
        users_buttons.append([InlineKeyboardButton("👤 مدیریت کاربر", callback_data="user_manage")])
        users_buttons.append([InlineKeyboardButton("🔙 بازگشت", callback_data="home")])
        await query.message.edit_text("📢 یک کاربر انتخاب کنید یا ارسال همگانی بزنید", reply_markup=InlineKeyboardMarkup(users_buttons))

    elif data == "user_manage":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚫 بن کردن کاربر", callback_data="ban_user")],
            [InlineKeyboardButton("✅ آن بن کردن کاربر", callback_data="unban_user")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="broadcast")]
        ])
        await query.message.edit_text("👤 مدیریت کاربران", reply_markup=keyboard)

    elif data == "send_all_users":
        broadcast_wait[user_id] = True
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="broadcast")]])
        await query.message.edit_text("📢 پیام خود را برای کل کاربران ارسال کنید", reply_markup=keyboard)

    elif data.startswith("pm_"):
        target_id = int(data[3:])
        private_message_wait[user_id] = target_id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="broadcast")]])
        await query.message.edit_text(f"✉️ پیام خود را برای کاربر {target_id} ارسال کنید", reply_markup=keyboard)

    # ── تعرفه ───────────────────────────────────────────────────
    elif data == "prices":
        text = "سلام همکار گرامی 😃\n\n🟣 هر گیگ 190 تومان\n\nID : @mak_11q\n\n🟢 آنلاین"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 خرید سرویس", callback_data="buy")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="home")]
        ])
        await query.message.edit_text(text, reply_markup=keyboard)

    # ── زیرمجموعه ───────────────────────────────────────────────
    elif data == "referral":
        count    = int(referrals.get(str(user_id), {}).get("count", 0))
        earned   = count * 3000
        ref_link = f"https://t.me/{context.bot.username}?start={user_id}"
        text = (
            f"👥 سیستم زیرمجموعه گیری\n\n"
            f"💰 پاداش هر دعوت: ۳۰۰۰ تومان\n\n"
            f"📊 تعداد دعوت‌ها: {count}\n"
            f"💵 مجموع پورسانت: {earned:,} تومان\n\n"
            f"🔗 لینک دعوت شما:\n{ref_link}\n\n"
            f"🎯 لینک را برای دوستان خود ارسال کنید."
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 بازگشت به منوی اصلی", callback_data="home")]])
        await query.message.edit_text(text, reply_markup=keyboard)

    # ── شارژ کیف پول ─────────────────────────────────────────────
    elif data.startswith("walletpay_card_"):
        amount = int(data[15:])
        _store_receipt(user_id, "wallet", None, amount)
        await query.message.edit_text(
            f"💳 فاکتور شارژ کیف پول\n\n💰 مبلغ:\n{amount:,} تومان\n\nشماره کارت:\n<code>{CARD_NUMBER}</code>\n\nپس از پرداخت عکس رسید را ارسال کنید.",
            parse_mode="HTML"
        )

    elif data.startswith("walletpay_trx_"):
        amount = int(data[14:])
        _store_receipt(user_id, "wallet", None, amount)
        trx = round(amount / get_trx_price_toman(), 2)
        await query.message.edit_text(
            f"💎 فاکتور پرداخت ارزی\n\n💳 معادل ریالی:\n{amount:,} تومان\n\n💸 مبلغ ارزی قابل پرداخت:\n{trx} TRX\n\n👇 آدرس کیف پول:\nفعلاً ندارد\n\n⚠️ دقیقاً مبلغ ذکر شده را واریز کنید.\n\n✅ پس از واریز، عکس رسید بفرستید"
        )


# ─── ذخیره سفارش در RAM + دیسک ───────────────────────────────────
def _store_receipt(user_id, rtype, plan, amount):
    info = {"type": rtype, "plan": plan, "amount": amount}
    waiting_receipt[user_id] = info
    orders = load_orders()
    orders[str(user_id)] = info
    save_orders(orders)


# ─── خرید با کیف پول ──────────────────────────────────────────────
async def _wallet_buy(query, context, user_id, gb, price, ptype, get_balance, set_balance, plan_override=None):
    bal = get_balance(user_id)
    if bal < price:
        await query.message.edit_text("❌ موجودی شما کافی نیست")
        return

    set_balance(user_id, bal - price)
    plan_name = plan_override if plan_override else gb
    gb_n, days = parse_plan(plan_name)
    username  = f"tg{user_id}"
    sub_url   = nahan_build_sub_url(username)

    notif = (
        f"🛒 خرید جدید با کیف پول\n\n"
        f"👤 {query.from_user.first_name}\n"
        f"🆔 {user_id}\n\n"
        f"📦 {plan_name}\n"
        f"💵 {price:,} تومان\n\n"
        f"▶️ نام کاربر در پنل:\n<code>{username}</code>\n\n"
        f"لینک اشتراک:\n<code>{sub_url}</code>"
    )
    await context.bot.send_message(ADMIN_ID, notif, parse_mode="HTML")
    await context.bot.send_message(SECOND_ADMIN_ID, notif, parse_mode="HTML")

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="home")]])
    await query.message.edit_text(
        config_message(plan_name, gb_n, days, sub_url),
        parse_mode="HTML",
        reply_markup=keyboard
    )


# ─── هندلر متن ────────────────────────────────────────────────────
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in banned_users or str(user_id) in banned_users:
        await update.message.reply_text("🚫 شما توسط مدیر بن شده‌اید و امکان استفاده از ربات را ندارید.")
        return

    if user_id in ban_wait:
        try:
            target = int(update.message.text)
            banned_users[str(target)] = True
            save_data("banned_users.json", banned_users)
            del ban_wait[user_id]
            await update.message.reply_text(f"✅ کاربر {target} بن شد.")
            try: await context.bot.send_message(target, "🚫 شما توسط مدیر بن شدید.")
            except: pass
        except:
            await update.message.reply_text("آیدی معتبر نیست.")
        return

    if user_id in unban_wait:
        try:
            target = int(update.message.text)
            banned_users.pop(str(target), None)
            save_data("banned_users.json", banned_users)
            del unban_wait[user_id]
            await update.message.reply_text(f"✅ کاربر {target} آن‌بن شد.")
            try: await context.bot.send_message(target, "✅ شما توسط مدیر آن‌بن شدید.")
            except: pass
        except:
            await update.message.reply_text("آیدی معتبر نیست.")
        return

    if user_id in gift_wait:
        code = update.message.text.strip()
        if user_id not in used_gifts:
            used_gifts[user_id] = []
            save_data("gifts.json", used_gifts)
        if code in used_gifts[user_id]:
            await update.message.reply_text("❌ شما قبلاً از این کد هدیه استفاده کرده‌اید")
            return

        gift_codes = {"mam4di": "1 گیگ", "mam4di_1k": "2 گیگ"}
        if code in gift_codes:
            used_gifts[user_id].append(code)
            save_data("gifts.json", used_gifts)
            volume = gift_codes[code]
            pending_gifts[user_id] = volume
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ تایید", callback_data=f"gift_accept_{user_id}"),
                InlineKeyboardButton("❌ رد کردن", callback_data=f"gift_reject_{user_id}")
            ]])
            await context.bot.send_message(
                ADMIN_ID,
                f"🎁 کد هدیه جدید ثبت شد\n\n👤 {update.effective_user.first_name}\n🆔 @{update.effective_user.username}\n📌 {user_id}\n\n🎁 کد: {code}\n📦 حجم: {volume}",
                reply_markup=keyboard
            )
            await update.message.reply_text(
                f"✅ کد هدیه ثبت شد\n📦 حجم: {volume}\n⏳ بعد تایید مدیر لینک ارسال می‌شود"
            )
            del gift_wait[user_id]
        else:
            await update.message.reply_text("❌ کد هدیه نامعتبر است")
            if user_id in gift_wait: del gift_wait[user_id]
        return

    if user_id in wallet_wait:
        try:
            amount = int(update.message.text.replace(",", ""))
            wallet_amount[user_id] = amount
            del wallet_wait[user_id]
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 کارت به کارت", callback_data=f"walletpay_card_{amount}")],
                [InlineKeyboardButton("💎 پرداخت ارزی", callback_data=f"walletpay_trx_{amount}")],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="wallet")]
            ])
            await update.message.reply_text("روش پرداخت را انتخاب کنید", reply_markup=keyboard)
        except:
            await update.message.reply_text("❌ مبلغ معتبر وارد کنید")
        return

    if user_id in broadcast_wait:
        try:
            with open("users.txt", "r", encoding="utf-8") as f:
                users = f.readlines()
            for u in users:
                try:
                    await context.bot.send_message(chat_id=int(u.strip()), text=update.message.text)
                except: pass
            await update.message.reply_text("✅ پیام شما با موفقیت برای کاربران ارسال شد")
        except:
            await update.message.reply_text("❌ لیست کاربران پیدا نشد")
        del broadcast_wait[user_id]
        return

    if user_id in private_message_wait:
        target_user = private_message_wait[user_id]
        await context.bot.send_message(chat_id=target_user, text=update.message.text)
        await update.message.reply_text("✅ پیام شما با موفقیت ارسال شد")
        del private_message_wait[user_id]
        return


# ─── هندلر عکس ────────────────────────────────────────────────────
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    orders = load_orders()
    info = waiting_receipt.get(user_id) or orders.get(str(user_id))
    if not info:
        return

    photo = update.message.photo[-1].file_id

    if info["type"] == "wallet":
        txt = f"شارژ کیف پول\n{info['amount']:,} تومان"
    else:
        txt = f"{info['plan']} | {info['amount']:,} تومان"

    caption = (
        f"📥 رسید جدید\n\n"
        f"👤 {update.effective_user.first_name}\n"
        f"🆔 @{update.effective_user.username}\n"
        f"📌 ID: {user_id}\n\n"
        f"🛒 اطلاعات:\n{txt}"
    )

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ تایید", callback_data=f"accept_{user_id}"),
        InlineKeyboardButton("❌ رد", callback_data=f"reject_{user_id}")
    ]])

    await context.bot.send_photo(ADMIN_ID, photo, caption=caption, reply_markup=keyboard)
    await context.bot.send_photo(SECOND_ADMIN_ID, photo, caption=caption, reply_markup=keyboard)

    keyboard2 = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="home")]])
    await update.message.reply_text("✅ رسید شما ثبت شد\n⏳ منتظر تایید مدیریت باشید", reply_markup=keyboard2)


# ─── main ─────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    print("Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
