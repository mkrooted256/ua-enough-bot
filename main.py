import os
import logging
from tkinter.messagebox import QUESTION

from sympy import ordered
from strings import *;

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
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
Q1, Q2, Q3, Q4, RESULT = range(Q_NUM)

def generate_question_state(question_id: int, next_state: int):
    async def state(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
        if (question_id-1 >= 0):
            user = update.message.from_user
            ans = int(update.message.text[0])
            try:
                context.user_data[f"ans_{question_id-1}"] = questions[question_id-1].tokens[ans]
            except KeyError as e:
                pass

        ordered_answers = [str(i) + ". " + ans for i,ans in enumerate(questions[question_id].answers)];
        
        reply_keyboard = ordered_answers
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
    ans = int(update.message.text[0])
    try:
        context.user_data[f"ans_{question_id-1}"] = questions[question_id-1].tokens[ans]
    except KeyError as e:
        pass

    await update.message.reply_text(
        default_ans,
        reply_markup=ReplyKeyboardRemove
    )

    for i in range(Q_NUM):
        token = context.user_data[f"ans_{i}"]
        if token > 0:
            update.message.reply_text(special_ans[token])
    
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = os.environ.get("TOKEN", "none")
    if (TOKEN == "none"):
        raise ValueError("Sorry, no telegram bot api token found. Aborting.")

    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            Q1: generate_question_state(Q1, Q2),
            Q2: generate_question_state(Q2, Q3),
            Q3: generate_question_state(Q3, Q4),
            Q4: generate_question_state(Q4, RESULT),
            RESULT: show_result
        }
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()