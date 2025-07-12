import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import os

# Replace with your OpenAI API key and Telegram bot token
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")

openai.api_key = OPENAI_API_KEY

def start(update, context):
    update.message.reply_text(
        "🌟 Welcome to the Tarot Bot! Ask any question and I'll draw a card for you. ✨"
    )

def tarot_reading(update, context):
    user_question = update.message.text

    # Let AI determine if it's a question or not
    # Determine if it's a question using a simple heuristic
    # Use OpenAI to determine if the message is a question
    question_check_prompt = (
        "Is the following message a question? Reply with only 'yes' or 'no'.\n"
        f"Message: {user_question}"
    )
    try:
        check_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that only answers 'yes' or 'no'."},
                {"role": "user", "content": question_check_prompt}
            ],
            max_tokens=3,
            temperature=0,
            n=1,
        )
        is_question = check_response.choices[0].message.content.strip().lower() == "yes"
    except Exception:
        is_question = False

    prompt = (
        "You are a wise and insightful tarot reader. When the user asks a question, draw one specific tarot card (choose from the real Major or Minor Arcana), name the card, and give a unique, thoughtful, and practical interpretation that offers genuine guidance for the user's situation. "
        "Avoid generic or vague answers—tailor your response to the user's question, and include mystical details, symbolism, and actionable advice and use easily understandable language. Include how much % yes or no in the end of reading\n"
        f"User message: {user_question}\n"
        "Bot:"
    )

    if is_question:
        update.message.reply_text("🔮 Shuffling the cards and focusing on your message... Let's see what the cards reveal! ✨")

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are a tarot reader bot."},
            {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.8,
            n=1,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Sorry, I couldn't get a tarot reading at the moment. 🃏\nError: {str(e)}"

    update.message.reply_text(reply)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, tarot_reading))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
