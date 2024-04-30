# import asyncio
# import telegram
import time
from telegram import Update, ForceReply
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
import database

token = "본인 토큰"

chat = ""

# 몇 가지 명령 핸들러를 정의합니다. 일반적으로 업데이트와 컨텍스트의 두 인수를 받습니다.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start 명령이 실행되면 메시지를 보냅니다."""
    temp = database.count_user()
    if temp >= 50:
        await update.message.reply_html(
            rf"사용자 등록이 마감되었습니다. 다음에 다시 시도해주세요."
            ,
            )
        print("사용자 등록 마감. 등록된 사융자 수: ", temp)
    else:
        user = update.effective_user
        chat_id = update.effective_chat.id
        #print('chat_id:', chat_id)
        database.insert_user(chat_id)
        await update.message.reply_html(
            #안녕하세요, {user.mention_html()}님.
            rf"위버스알림봇을 시작합니다. 명령어를 입력하거나 클릭하세요. "
            "\n\n/update 알림 등록/삭제 방법"
            "\n/help 도움말"
            "\n\n공지✔ 및 LIVE🔴 알림은 제공되지 않습니다."
            ,
            )


def get_msg():
    print('chat:', chat)




async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """업데이트 명령이 실행되면 메시지를 보냅니다."""
    chat_id = update.effective_chat.id
    if database.select_data(chat_id) == '0':
        await update.message.reply_text("채팅창에 /start 를 입력해 사용자 정보를 등록 후 사용할 수 있습니다."
                                        "알림봇은 채팅방코드 외 개인정보는 수집하지 않습니다.")
    else:
        await update.message.reply_text("✅알림 등록 또는 삭제 방법\n\n채팅창에 그룹명(영문)+활동명(한글)을 입력하세요. (여러 건 등록을 원하는 경우 / 추가)\n"
                                        "예1) andteam죠\n"
                                        "예2) qwer시연/riize성찬/riize원빈"
                                        "\n\n✅현재 설정 가능한 아티스트"
                                        "\nandteam\nboynextdoor\nenhypen\nnctwish\nriize\ntreasure\nqwer"
                                        )


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """도움말 명령이 실행되면 메시지를 보냅니다."""
    chat_id = update.effective_chat.id
    if database.select_data(chat_id) == '0':
        await update.message.reply_text("채팅창에 /start 를 입력해 사용자 정보를 등록 후 사용할 수 있습니다."
                                        "알림봇은 채팅방코드 외 개인정보는 수집하지 않습니다.")
    else:
        global chat
        if chat == "":
            await update.message.reply_text("아티스트명을 입력하세요.")
        else:
            temp = chat.split('/')
            print(temp, "add", time.strftime('%Y.%m.%d %H:%M:%S'))
            for i in temp:
                if database.select_artist_YN(i) == '0':
                    print(i,'는 지원하지 않는 아티스트입니다.')
                    await update.message.reply_text(i+" 는 지원되지 않는 아티스트입니다.\n")
                else:
                    if (database.delete_artist_list(i, chat_id) == 0) or (database.insert_artist_list(i, chat_id) == 0):
                        await update.message.reply_text(i + " 등록 과정에서 오류 발생. 관리자 문의 바랍니다.")
                    else:
                        await update.message.reply_text(i+" 등록되었습니다.\n")
            temp = database.select_artist_list(chat_id)
            await update.message.reply_text("✅현재 알림 설정된 아티스트\n"+temp)
        chat = ""


async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """알림삭제 명령이 실행되면 메시지를 보냅니다."""
    chat_id = update.effective_chat.id
    if database.select_data(chat_id) == '0':
        await update.message.reply_text("채팅창에 /start 를 입력해 사용자 정보를 등록 후 사용할 수 있습니다."
                                        "알림봇은 채팅방코드 외 개인정보는 수집하지 않습니다.")
    else:
        global chat
        if chat == "":
            await update.message.reply_text("아티스트명을 입력하세요.")
        else:
            temp = chat.split('/')
            print(temp, "delete", time.strftime('%Y.%m.%d %H:%M:%S'))
            for i in temp:
                if database.select_artist_YN(i) == '0':
                    print(i,'는 지원하지 않는 아티스트입니다.')
                    await update.message.reply_text(i + " 는 지원되지 않는 아티스트입니다.\n")
                else:
                    if database.delete_artist_list(i, chat_id) == 0:
                        await update.message.reply_text(i + " 삭제 과정에서 오류 발생. 관리자 문의 바랍니다.")
                    else:
                        await update.message.reply_text(i + " 삭제되었습니다.")
            temp = database.select_artist_list(chat_id)
            await update.message.reply_text("✅현재 알림 설정된 아티스트\n"+temp)
        chat = ""



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """사용자 메시지를 에코합니다."""
    chat_id = update.effective_chat.id
    if database.select_data(chat_id) == '0':
        await update.message.reply_text("채팅창에 /start 를 입력해 사용자 정보를 등록 후 사용할 수 있습니다."
                                        "알림봇은 채팅방코드 외 개인정보는 수집하지 않습니다.")
    else:
        global chat
        chat = update.message.text.strip().lower()
        print('받은 메시지:', chat, time.strftime('%Y.%m.%d %H:%M:%S'))
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        print('chatid:', chat_id)
        print('userid:', user_id)
        await update.message.reply_text(chat + " 아티스트를 추가하려면 /add, 삭제하려면 /delete 를 입력하세요.")



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """도움말 명령이 실행되면 메시지를 보냅니다."""
    chat_id = update.effective_chat.id
    if database.select_data(chat_id) == '0':
        await update.message.reply_text("채팅창에 /start 를 입력해 사용자 정보를 등록 후 사용할 수 있습니다."
                                        "알림봇은 채팅방코드 외 개인정보는 수집하지 않습니다.")
    else:
        await update.message.reply_text("✅알림이 오지 않을 경우\n"
                                        "✔휴대폰 전원을 껐다 켜기\n"
                                        "✔텔레그램 알림 설정 확인\n"
                                        "✅관리자 문의\n"
                                        "✔twitter: sasisu9876 \n"
                                        )


# 애플리케이션을 생성하고 봇의 토큰을 전달합니다.

app = ApplicationBuilder().token(token).build()

# 다른 명령에 대해 - 텔레그램으로 답변하기
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("update", update_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("add", add_command))
app.add_handler(CommandHandler("delete", delete_command))

# 텔레그램에서 메시지를 에코합니다.
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# 사용자가 Ctrl-C를 누를 때까지 봇을 실행합니다.
app.run_polling()

