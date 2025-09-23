from os import getenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

from CommandType import CommandType
from User import User  # فقط برای نمایش پروفایل (فرمت خروجی)

# --- DB imports ---
from db import SessionLocal
from db.crud import get_or_create_user, update_user_field

CHANNEL_ID = "TEST12_For_Bot"

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
    telegram_id = update.effective_user.id
    with SessionLocal() as db:
        u = get_or_create_user(db, telegram_id)

        keyboard = [
            [InlineKeyboardButton(f"✏ نام = {u.firstname}" if u.firstname else "✏️ نام",
                                  callback_data=CommandType.SET_FIRSTNAME.value)],
            [InlineKeyboardButton(f"✏ نام خانوادگی = {u.lastname}" if u.lastname else "✏️ نام خانوادگی",
                                  callback_data=CommandType.SET_LASTNAME.value)],
            [InlineKeyboardButton(f"📱 شماره تماس = {u.phone}" if u.phone else "📱 شماره تماس",
                                  callback_data=CommandType.SET_PHONE.value)],
            [InlineKeyboardButton(f"🏫 پایه تحصیلی = {u.grade}" if u.grade else "🏫 پایه تحصیلی",
                                  callback_data=CommandType.SET_GRADE.value)],
            [InlineKeyboardButton(f"📚 رشته تحصیلی = {u.field}" if u.field else "📚 رشته تحصیلی",
                                  callback_data=CommandType.SET_FIELD.value)],
            [InlineKeyboardButton(f"🌆 شهر = {u.city}" if u.city else "🌆 شهر",
                                  callback_data=CommandType.SET_CITY.value)],
            [InlineKeyboardButton("👀 نمایش پروفایل", callback_data=CommandType.SHOW_PROFILE.value)]
        ]

    await update.message.reply_text(
        "📌 کدوم بخش پروفایلتو میخوای تغییر بدی؟",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# هندل کردن انتخاب از منوی پروفایل
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    telegram_id = query.from_user.id
    action = query.data

    if action == CommandType.SHOW_PROFILE.value:
        # خروجی نمایش پروفایل با کلاس User فعلی (فقط برای فرمت متن)
        with SessionLocal() as db:
            u = get_or_create_user(db, telegram_id)
            temp = User(telegram_id)
            temp.firstname = u.firstname
            temp.lastname = u.lastname
            temp.phone = u.phone
            temp.grade = u.grade
            temp.field = u.field
            temp.city = u.city
            await query.edit_message_text(str(temp))
    else:
        field = action.replace("set_", "")  # مثلاً "firstname"  (از CommandType) :contentReference[oaicite:4]{index=4}
        context.user_data["waiting_for"] = field
        await query.edit_message_text(f"لطفاً مقدار {field} رو وارد کن:")

# گرفتن ورودی کاربر برای پروفایل
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if "waiting_for" in context.user_data:
        field = context.user_data.pop("waiting_for")
        value = update.message.text

        with SessionLocal() as db:
            update_user_field(db, telegram_id, field, value)

        await update.message.reply_text(
            f"✅ {field} با موفقیت ذخیره شد.\nاز /profile می‌تونی ادامه بدی."
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
