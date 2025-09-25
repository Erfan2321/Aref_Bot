import logging
from datetime import time
from os import getenv

from telegram import Update, Poll

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    JobQueue,
    filters,
    ChatMemberHandler, PollAnswerHandler,
)

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)


async def check_group_validity(update: Update, context: CallbackContext) -> bool:
    """
    این تابع باید چک کنه آیا ادمین مورد نظر تو گروه هست یا نه
    فعلاً خالیه.
    """
    # TODO: چک کردن ادمین‌ها
    return True
async def save_student_feedback(user_id: int, feedback: bool):
    """
    نتیجه نظرسنجی دانش‌آموز رو توی دیتابیس ذخیره کنه
    فعلاً خالیه.
    """
    # TODO: سیو توی دیتابیس
    pass
async def get_counselor_id() -> int:
    """
    آیدی عددی مشاور رو از دیتابیس بخونه
    فعلاً خالیه.
    """
    # TODO: خواندن از دیتابیس
    return 1010942742

# ====== هندلرها ======

async def on_bot_added(update: Update, context: CallbackContext):
    """وقتی ربات به گروه اضافه شد"""
    if update.my_chat_member.new_chat_member.status in ["member", "administrator"]:
        is_valid = await check_group_validity(update, context)
        if not is_valid:
            chat_id = update.effective_chat.id
            await context.bot.leave_chat(chat_id)
async def weekly_group_report(context: CallbackContext):
    """جمعه‌ها ساعت ۰۰:۰۰ گزارش هفتگی تو گروه"""
    chat_id = context.job.chat_id

    counselor_id = await get_counselor_id()

    # TODO: آمار پیام/ویس/ویدیو مسیج/ری‌اکشن مشاور در این گروه حساب بشه
    text = (
        f"📊 گزارش هفتگی مشاور (ID: {counselor_id})\n\n"
        f"- تعداد پیام‌ها: ...\n"
        f"- تعداد ویس: ...\n"
        f"- تعداد ویدیو مسیج: ...\n"
        f"- تعداد ری‌اکشن: ...\n"
    )

    await context.bot.send_message(chat_id = chat_id, text = text)
async def weekly_student_poll(context: CallbackContext):
    """جمعه‌ها ساعت ۰۰:۰۰ نظرسنجی برای دانش‌آموز"""
    user_id = context.job.chat_id
    question = "آیا جلسه مشاوره این هفته شما برگزار شد؟"
    options = ["بله", "خیر"]

    msg = await context.bot.send_poll(
        chat_id = user_id,
        question = question,
        options = options,
        is_anonymous = False
    )

    # ذخیره پیام برای پردازش جواب بعداً
    payload = {
        msg.poll.id: {
            "user_id": user_id,
            "message_id": msg.message_id
        }
    }
    context.bot_data.update(payload)
async def poll_answer_handler(update: Update, context: CallbackContext):
    """ذخیره نتیجه نظرسنجی دانش‌آموز"""
    answer = update.poll_answer
    poll_id = answer.poll_id
    user_id = context.bot_data[poll_id]["user_id"]

    if answer.option_ids:
        chosen = answer.option_ids[0]  # 0 = بله, 1 = خیر
        feedback = True if chosen == 0 else False
        await save_student_feedback(user_id, feedback)

# ====== MAIN ======
async def get_chat_id(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Chat ID: {chat_id}")


def main():
    job_queue = JobQueue()

    application = (
        Application.builder()
        .token(getenv("BOT_API_TOKEN"))
        .job_queue(job_queue)   # اینجا job_queue رو دستی ست می‌کنیم
        .build()
    )

    print("Job queue:", application.job_queue)

    # هندلرها
    application.add_handler(PollAnswerHandler(poll_answer_handler))
    application.add_handler(CommandHandler("chatid", get_chat_id))

    # زمان‌بندی هفتگی
    report_time = time(hour = 0, minute = 0, second = 0)

    group_chat_id = 1010942742
    student_user_id = 5230466459

    application.job_queue.run_daily(
        weekly_group_report,
        time = report_time,
        days = (5,),  # شنبه ۰۰:۰۰
        chat_id = group_chat_id
    )

    application.job_queue.run_daily(
        weekly_student_poll,
        time = report_time,
        days = (5,),
        chat_id = student_user_id
    )

    application.run_polling()
if __name__ == "__main__":
    main()
