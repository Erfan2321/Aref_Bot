from os import getenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters

CHANNEL_ID = "TEST12_For_Bot"

# فعلاً به جای دیتابیس
users_data = {}

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # بررسی عضویت در کانال
    member = await context.bot.get_chat_member("@" + CHANNEL_ID, user_id)
    if member.status not in ["member", "administrator", "creator"]:
        await update.message.reply_text(f"🔒 برای استفاده از بات باید اول عضو کانال بشی:\nhttps://t.me/{CHANNEL_ID}")
        return

    await update.message.reply_text(
        f"سلام {update.effective_user.first_name} 👋\nبه بات خوش اومدی!\n"
    )

# پروفایل (منوی انتخاب)
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users_data.setdefault(user_id, {})

    keyboard = [
        [InlineKeyboardButton("✏️ نام", callback_data="set_firstname")],
        [InlineKeyboardButton("✏️ نام خانوادگی", callback_data="set_lastname")],
        [InlineKeyboardButton("📱 شماره تماس", callback_data="set_phone")],
        [InlineKeyboardButton("🏫 پایه تحصیلی", callback_data="set_grade")],
        [InlineKeyboardButton("📚 رشته تحصیلی", callback_data="set_field")],
        [InlineKeyboardButton("🌆 شهر", callback_data="set_city")],
        [InlineKeyboardButton("👀 نمایش پروفایل", callback_data="show_profile")]
    ]

    await update.message.reply_text("📌 کدوم بخش پروفایلتو میخوای تغییر بدی؟",
                                    reply_markup=InlineKeyboardMarkup(keyboard))

# -------------------------------
# هندل کردن انتخاب از منوی پروفایل
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    action = query.data

    if action.startswith("set_"):
        field = action.split("_")[1]
        context.user_data["waiting_for"] = field
        await query.edit_message_text(f"لطفاً مقدار {field} رو وارد کن:")
    elif action == "show_profile":
        profile_data = users_data.get(user_id, {})
        text = "👤 پروفایل شما:\n"
        for k, v in profile_data.items():
            text += f"- {k}: {v}\n"
        if not profile_data:
            text = "پروفایل شما خالیه ❌"
        await query.edit_message_text(text)


# گرفتن ورودی کاربر برای پروفایل
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if "waiting_for" in context.user_data:
        field = context.user_data.pop("waiting_for")
        value = update.message.text
        users_data.setdefault(user_id, {})[field] = value
        await update.message.reply_text(f"✅ {field} با موفقیت ذخیره شد.\nاز /profile میتونی ادامه بدی.")


# اجرا
def main():

    app = Application.builder().token(getenv("BOT_API_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()