from enum import nonmember
from os import getenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from CommandType import CommandType
from DetaSaver import users_data
from UserHandler import User, UserField

CHANNEL_ID = "TEST12_For_Bot"

SET_FIRSTNAME, SET_LASTNAME, SET_PHONE, SET_GRADE, SET_FIELD, SET_CITY, PROFILE_INPUT, PROFILE_MENU = range(8)
MAIN_MENU = 100


async def check_for_join (update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):

    member = await context.bot.get_chat_member("@" + CHANNEL_ID, user_id)

    if member.status not in ["member", "administrator", "creator"]:
        await update.message.reply_text(f"🔒 برای استفاده از بات باید اول عضو کانال بشی:\nhttps://t.me/{CHANNEL_ID}")
        return False
    return True
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await check_for_join(update, context, user_id):
        return ConversationHandler.END

    keyboard = [
        [KeyboardButton("👤 پروفایل")],
        [KeyboardButton("ℹ️ راهنما")],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard = True,
        one_time_keyboard = True
    )

    await update.message.reply_text(
        "به ربات خوش اومدی 🌹\nیه بخش انتخاب کن:",
        reply_markup = reply_markup
    )
    return MAIN_MENU
async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    if not await check_for_join(update, context, update.effective_user.id):
        return ConversationHandler.END
    if text == "👤 پروفایل":
        return await show_profile(update, context)
    elif text == "ℹ️ راهنما":
        await update.message.reply_text("ℹ️ اینجا متن راهنما میاد...")
        return ConversationHandler.END
    return MAIN_MENU
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ عملیات لغو شد.")
    return ConversationHandler.END

#      قسمت پروفایل

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await check_for_join(update, context, user_id):
        return ConversationHandler.END

    users_data.setdefault(user_id, User(user_id))

    user = users_data[user_id]

    keyboard = [
        [InlineKeyboardButton(f"✏ نام = {user.firstname}" if user.firstname else "✏️ نام",
                              callback_data = CommandType.SET_FIRSTNAME.value)],
        [InlineKeyboardButton(f"✏ نام خانوادگی = {user.lastname}" if user.lastname else "✏️ نام خانوادگی",
                              callback_data = CommandType.SET_LASTNAME.value)],
        [InlineKeyboardButton(f"📱 شماره تماس = {user.phone}" if user.phone else "📱 شماره تماس",
                              callback_data = CommandType.SET_PHONE.value)],
        [InlineKeyboardButton(f"🏫 پایه تحصیلی = {user.grade}" if user.grade else "🏫 پایه تحصیلی",
                              callback_data = CommandType.SET_GRADE.value)],
        [InlineKeyboardButton(f"📚 رشته تحصیلی = {user.field}" if user.field else "📚 رشته تحصیلی",
                              callback_data = CommandType.SET_FIELD.value)],
        [InlineKeyboardButton(f"🌆 شهر = {user.city}" if user.city else "🌆 شهر",
                              callback_data=CommandType.SET_CITY.value)],
        [InlineKeyboardButton("👀 نمایش پروفایل", callback_data = CommandType.SHOW_PROFILE.value)],
        [InlineKeyboardButton("بازگشت", callback_data = CommandType.CANCEL.value)]
    ]

    if update.message:
        await update.message.reply_text(
            "📌 کدوم بخش پروفایلتو میخوای تغییر بدی؟",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "📌 کدوم بخش پروفایلتو میخوای تغییر بدی؟",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    return PROFILE_INPUT
async def profile_button_handler (update: Update, context: ContextTypes.DEFAULT_TYPE) :

    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    action = query.data

    if not await check_for_join(update, context, user_id):
        return ConversationHandler.END

    elif action == CommandType.CANCEL.value:
        await query.edit_message_text("عملیات لغو شد❌")
        return ConversationHandler.END
    elif action == CommandType.SET_FIRSTNAME.value:
        keyboard = [[InlineKeyboardButton("↩️ بازگشت", callback_data=CommandType.CANCEL.value)]]
        await query.edit_message_text("لطفاً نام خودت رو وارد کن:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SET_FIRSTNAME
    elif action == CommandType.SET_LASTNAME.value:
        keyboard = [[InlineKeyboardButton("↩️ بازگشت", callback_data=CommandType.CANCEL.value)]]
        await query.edit_message_text("لطفاً نام خانوادگی خودت رو وارد کن:",reply_markup=InlineKeyboardMarkup(keyboard))
        return SET_LASTNAME
    elif action == CommandType.SET_PHONE.value:
        keyboard = [[InlineKeyboardButton("↩️ بازگشت", callback_data=CommandType.CANCEL.value)]]
        await query.edit_message_text("لطفاً شماره تماس خودت رو وارد کن:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SET_PHONE
    elif action == CommandType.SET_GRADE.value:
        keyboard = [[InlineKeyboardButton("↩️ بازگشت", callback_data=CommandType.CANCEL.value)]]
        await query.edit_message_text("لطفاً پایه تحصیلی خودت رو وارد کن:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SET_GRADE
    elif action == CommandType.SET_FIELD.value:
        keyboard = [[InlineKeyboardButton("↩️ بازگشت", callback_data=CommandType.CANCEL.value)]]
        await query.edit_message_text("لطفاً رشته تحصیلی خودت رو وارد کن:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SET_FIELD
    elif action == CommandType.SET_CITY.value:
        keyboard = [[InlineKeyboardButton("↩️ بازگشت", callback_data=CommandType.CANCEL.value)]]
        await query.edit_message_text("لطفاً شهر خودت رو وارد کن:", reply_markup=InlineKeyboardMarkup(keyboard))
        return SET_CITY
    return None

async def set_user_field(update: Update, context: ContextTypes.DEFAULT_TYPE, field : UserField) :
    user = users_data[update.effective_user.id]

    if update.message.text == CommandType.CANCEL.value:
        await update.message.reply_text("عملیات لغو شد❌")
        return ConversationHandler.END
    if field.name == UserField.firstname.name:
        user.firstname = update.message.text
        await update.message.reply_text("✅ نام ذخیره شد.")
    elif field.name == UserField.lastname.name:
        user.lastname = update.message.text
        await update.message.reply_text("✅ نام خانوادگی ذخیره شد.")
    elif field.name == UserField.phone.name:
        user.phone = update.message.text
        await update.message.reply_text("✅ شماره تماس ذخیره شد.")
    elif field.name == UserField.grade.name:
        user.grade = update.message.text
        await update.message.reply_text("✅ پایه تحصیلی ذخیره شد.")
    elif field.name == UserField.city.name:
        user.city = update.message.text
        await update.message.reply_text("✅ شهر ذخیره شد.")
    elif field.name == UserField.field.name:
        user.field = update.message.text
        await update.message.reply_text("ً✅ رشته تحصیلی ذخیره شد.")

    return PROFILE_MENU

async def set_firstname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_user_field(update, context, UserField.firstname)
async def set_lastname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_user_field(update, context, UserField.lastname)
async def set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_user_field(update, context, UserField.phone)
async def set_grade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_user_field(update, context, UserField.grade)
async def set_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_user_field(update, context, UserField.field)
async def set_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_user_field(update, context, UserField.city)


def build_profile_conversation() -> ConversationHandler:
    return ConversationHandler(
        entry_points = [CommandHandler(CommandType.PROFILE.value, show_profile)],
        states = {
            PROFILE_MENU: [CallbackQueryHandler(show_profile)],
            PROFILE_INPUT: [CallbackQueryHandler(profile_button_handler)],

            SET_FIRSTNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_firstname),
                CallbackQueryHandler(profile_button_handler, pattern=f"^{CommandType.CANCEL.value}$")
            ],
            SET_LASTNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_lastname),
                CallbackQueryHandler(profile_button_handler, pattern=f"^{CommandType.CANCEL.value}$")
            ],
            SET_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_phone),
                CallbackQueryHandler(profile_button_handler, pattern=f"^{CommandType.CANCEL.value}$")
            ],
            SET_GRADE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_grade),
                CallbackQueryHandler(profile_button_handler, pattern=f"^{CommandType.CANCEL.value}$")
            ],
            SET_FIELD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_field),
                CallbackQueryHandler(profile_button_handler, pattern=f"^{CommandType.CANCEL.value}$")
            ],
            SET_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_city),
                CallbackQueryHandler(profile_button_handler, pattern=f"^{CommandType.CANCEL.value}$")
            ],
        },
        fallbacks = [CommandHandler("cancel", cancel)],
        allow_reentry = True,
    )
def build_start_conversation() -> ConversationHandler:
    return  ConversationHandler(
        entry_points = [CommandHandler("start", start)],
        states = {
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)],
        },
        fallbacks = [],
        allow_reentry = True,
    )


def main():
    app = Application.builder().token(getenv("BOT_API_TOKEN")).build()

    app.add_handler(build_profile_conversation())
    app.add_handler(build_start_conversation())
    app.run_polling()

if __name__ == "__main__":
    main()