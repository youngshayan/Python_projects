import telebot
import requests

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = 'your API'

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Binance API base URL
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/24hr'


def get_crypto_info(symbol):
    try:
        # Request data from Binance API
        response = requests.get(BINANCE_API_URL, params={'symbol': symbol.upper()})
        data = response.json()

        if response.status_code == 200:
            # Extract desired data
            price = data.get('lastPrice')
            price_change = data.get('priceChangePercent')
            high_price = data.get('highPrice')
            low_price = data.get('lowPrice')

            # Format the message
            info = (
                f"Symbol: {symbol.upper()}\n"
                f"Price: {price}\n"
                f"24h Change: {price_change}%\n"
                f"24h High: {high_price}\n"
                f"24h Low: {low_price}\n"
            )
            return info
        else:
            return "Error: Invalid cryptocurrency symbol or issue with Binance API."

    except Exception as e:
        return f"An error occurred: {str(e)}"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Welcome to the Crypto Price Bot! Send a cryptocurrency symbol like 'BTCUSDT' to get the current price and info.")


@bot.message_handler(func=lambda message: True)
def send_crypto_info(message):
    symbol = message.text.strip().upper()
    info = get_crypto_info(symbol)
    bot.reply_to(message, info)


# Start polling for updates from Telegram
bot.polling()
