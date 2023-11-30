# Import necessary libraries
import telebot
import requests
import os

# Load Telegram bot token from environment
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Replace 'YOUR_TOKEN' with TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Define the API endpoint
api_url = 'https://api.coinconvert.net/convert/'

# Define start command handler
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome to the Crypto Converter Bot! 💰\n\n"
                                      "I'm here to help you convert crypto coins to USD. Use /convert to get started.")

# Define convert command handler
@bot.message_handler(commands=['convert'])
def handle_convert(message):
    bot.send_message(message.chat.id, "Please enter the coin name and amount in the format: /convert coin_name amount 🔄")

# Define help command handler
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Welcome to the Crypto Converter Bot! 💰\n\n"
                                      "To convert coins, use the /convert command followed by the coin name and amount.\n"
                                      "For example: /convert btc 1.5 🔄")

# Define text message handler
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text.startswith('/convert'):
        try:
            _, coin, amount = message.text.split()
            amount = float(amount)

            # Make API request
            response = requests.get(f'{api_url}{coin.lower()}/usd?amount={amount}')
            data = response.json()

            # Check API response status
            status = data.get('status', 'error')

            if status == 'success':
                # Extract conversion result
                result = data.get(coin.upper(), 'Error in conversion.')

                # Send the result to the user
                bot.send_message(message.chat.id, f"💱 Conversion result: {amount} {coin.upper()} = {result} USD")
            else:
                bot.send_message(message.chat.id, "⚠️ Error in conversion. Please try again.")
        except ValueError:
            bot.send_message(message.chat.id, "❌ Invalid input. Please use the format: /convert coin_name amount 🔄")

# Run the bot
bot.polling()
