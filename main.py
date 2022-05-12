import os
import logging

import telegram
from strings import *;

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, constants
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


Q_NUM = 4
Q1, Q2, Q3, Q4, RESULT = range(Q_NUM+1)

def generate_question_state(question_id: int, next_state: int):
    async def state(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
        if (question_id-1 >= 0):
            user = update.message.from_user
            try:
                ans = int(update.message.text[0]) - 1
                context.user_data[f"ans_{question_id-1}"] = questions[question_id-1].tokens[ans]
            except KeyError as e:
                await update.message.reply_text(
                    "Сталась якась помилка на нашому боці. Вибачте. Спробуйте знову через пару хвилин.",
                    parse_mode='MARKDOWN_V2',
                    reply_markup=ReplyKeyboardMarkup([["/start"]], one_time_keyboard=True)
                )
                return ConversationHandler.END
            except ValueError as e:
                await update.message.reply_text(
                    "Сталась якась помилка на нашому боці. Вибачте. Спробуйте знову через пару хвилин.",
                    parse_mode='MARKDOWN_V2',
                    reply_markup=ReplyKeyboardMarkup([["/start"]], one_time_keyboard=True)
                )
                return ConversationHandler.END

        ordered_answers = [str(i+1) + ". " + ans for i,ans in enumerate(questions[question_id].answers)];
        
        reply_keyboard = [[option] for option in ordered_answers]
        msg = questions[question_id].text + "\n\n" + "\n".join(ordered_answers)

        await update.message.reply_text(
            msg,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder=f"Питання {question_id}"
            ),
        )

        return next_state
    return state;

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Почнімо✨"]]

    await update.message.reply_text(
        welcome_text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )

    return Q1


async def show_result(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    try:
        ans = int(update.message.text[0]) - 1
        context.user_data[f"ans_{Q4}"] = questions[Q4].tokens[ans]
    except KeyError as e:
        await update.message.reply_text(
            "Сталась якась помилка на нашому боці. Вибачте. Спробуйте знову через пару хвилин.",
            parse_mode=constants.ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup([["/start"]], one_time_keyboard=True)
        )
        return ConversationHandler.END
    except ValueError as e:
        await update.message.reply_text(
            "Сталась якась помилка на нашому боці. Вибачте. Спробуйте знову через пару хвилин.",
            parse_mode=constants.ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup([["/start"]], one_time_keyboard=True)
        )
        return ConversationHandler.END

    await update.message.reply_text(
        default_ans[0],
        parse_mode=constants.ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )

    for i in range(Q_NUM):
        token = context.user_data[f"ans_{i}"]
        if token > 0:
            await update.message.reply_text(
                special_ans[token],
                parse_mode=constants.ParseMode.HTML
            )
    
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = os.environ.get("TOKEN", "none")
    if (TOKEN == "none"):
        raise ValueError("Sorry, no telegram bot api token found. Aborting.")

    application = ApplicationBuilder().token(TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), MessageHandler(filters.ALL, start)],
        states={
            Q1: [MessageHandler(filters.ALL, generate_question_state(Q1, Q2))],
            Q2: [MessageHandler(filters.TEXT, generate_question_state(Q2, Q3))],
            Q3: [MessageHandler(filters.TEXT, generate_question_state(Q3, Q4))],
            Q4: [MessageHandler(filters.TEXT, generate_question_state(Q4, RESULT))],
            RESULT: [MessageHandler(filters.TEXT, show_result)]
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()