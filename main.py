from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

TOKEN = os.getenv("BOT_TOKEN")

TOTAL = 9

ALL_USERS = [
    "adinamizaba323",
    "osn_zenky",
    "amelinda19",
    "nb_noel",
    "OSN_CLAUDIA",
    "OSN_MERIDA",
    "MeoMeoa0",
    "shenlongpr",
    "osn_olia"
]


NAME_USERS = [
    "DINAMIZABA",
    "ZENKY",
    "AMELINDA",
    "NOEL",
    "CLAUDIA",
    "MERIDA",
    "BLOOM",
    "SHENLONG",
    "OLIA"
]

USER_NAME_MAP = dict(zip(ALL_USERS, NAME_USERS))

members_clicked = set()

full = False


def full_command(update, context):
    global members_clicked, full
    full = True
    update.message.reply_text(f"✅ Đã đủ tất cả!")
    # Reset bộ đếm để có thể bắt đầu lượt mới nếu cần
    members_clicked.clear()
    full = False  # Sau khi báo xong, cho phép nhận lượt mới

def handle_message(update, context):
    global members_clicked, full

    text = update.message.text.strip()
    user = update.effective_user
    username = user.username or user.first_name

    if text == "1":
        members_clicked.add(username)
        if full:
            return 

        missing_users = [u for u in ALL_USERS if u not in members_clicked]
        missing_names = [USER_NAME_MAP.get(u, u) for u in missing_users]

        count = len(members_clicked)
        msg = f"Số người đã điểm danh: {count}/{TOTAL}"

        if missing_names:
            msg += "\nCòn thiếu: " + ", ".join(missing_names)
        else:
            msg += "\n✅ Đã đủ tất cả mọi người!"

        update.message.reply_text(msg)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Thêm lệnh /full
    dp.add_handler(CommandHandler("full", full_command))

    # Bắt tất cả tin nhắn
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("Bot đang chạy...")
    updater.idle()

if __name__ == "__main__":
    main()