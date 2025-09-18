from os import getenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from CommandType import CommandType
from User import User

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


# نمایش منوی پروفایل
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users_data.setdefault(user_id, User(user_id))

    user = users_data[user_id]

    keyboard = [
        [InlineKeyboardButton(f"✏ نام = {user.firstname}" if user.firstname else "✏️ نام",
                              callback_data=CommandType.SET_FIRSTNAME.value)],
        [InlineKeyboardButton(f"✏ نام خانوادگی = {user.lastname}" if user.lastname else "✏️ نام خانوادگی",
                              callback_data=CommandType.SET_LASTNAME.value)],
        [InlineKeyboardButton(f"📱 شماره تماس = {user.phone}" if user.phone else "📱 شماره تماس",
                              callback_data=CommandType.SET_PHONE.value)],
        [InlineKeyboardButton(f"🏫 پایه تحصیلی = {user.grade}" if user.grade else "🏫 پایه تحصیلی",
                              callback_data=CommandType.SET_GRADE.value)],
        [InlineKeyboardButton(f"📚 رشته تحصیلی = {user.field}" if user.field else "📚 رشته تحصیلی",
                              callback_data=CommandType.SET_FIELD.value)],
        [InlineKeyboardButton(f"🌆 شهر = {user.city}" if user.city else "🌆 شهر",
                              callback_data=CommandType.SET_CITY.value)],
        [InlineKeyboardButton("👀 نمایش پروفایل", callback_data=CommandType.SHOW_PROFILE.value)]
    ]

    await update.message.reply_text(
        "📌 کدوم بخش پروفایلتو میخوای تغییر بدی؟",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# -------------------------------
# هندل کردن انتخاب از منوی پروفایل
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    action = query.data

    # نمایش پروفایل
    if action == CommandType.SHOW_PROFILE.value:
        user = users_data[user_id]
        await query.edit_message_text(str(user))

    # یکی از فیلدهای پروفایل
    else:
        field = action.replace("set_", "")  # مثلاً "firstname"
        context.user_data["waiting_for"] = field
        await query.edit_message_text(f"لطفاً مقدار {field} رو وارد کن:")


# -------------------------------
# گرفتن ورودی کاربر برای پروفایل
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if "waiting_for" in context.user_data:
        field = context.user_data.pop("waiting_for")
        value = update.message.text

        user = users_data.setdefault(user_id, User(user_id))
        setattr(user, field, value)

        await update.message.reply_text(
            f"✅ {field} با موفقیت ذخیره شد.\nاز /profile میتونی ادامه بدی."
        )


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