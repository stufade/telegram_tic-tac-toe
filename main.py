from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from Classes.Game import Game
import config
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def makeBotButtons():
    keyboard = [InlineKeyboardButton(text="Easy 🐣", callback_data="bot easy"),
                InlineKeyboardButton(text="Hard 🤖", callback_data="bot hard")]

    return InlineKeyboardMarkup([keyboard])


def start(update, context):
    games[update.effective_chat.id] = Game()
    update.message.reply_text("Hi! Choose difficulty!", reply_markup=makeBotButtons())


def play(update, context):
    gameID = update.effective_chat.id

    games[gameID].inGame = True
    update.message.reply_text(games[gameID].message, reply_markup=games[gameID].showButtons())


def on_message(update, context):
    update.message.reply_text("If you want to end the game use /end. \nIf you want to see the game use /play.")


def callBackHandler(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data
    gameID = update.effective_chat.id

    if data == "-1":
        return
    elif data.isnumeric():
        games[gameID].makeBothMoves(query)
    elif data.startswith("game"):
        action = data.split(" ")[1]
        if action == "play":
            games[gameID].inGame = True
            query.edit_message_text(games[gameID].message, reply_markup=games[gameID].showButtons())
        elif action == "end":
            games[gameID].inGame = False
            query.edit_message_text("Game Over! Try again.", reply_markup=games[gameID].showButtons(useless=True))
            games[gameID].resetAll()
        elif action == "change":
            games[gameID].inGame = False
            query.edit_message_text("Hi! Choose difficulty!", reply_markup=makeBotButtons())
    elif data.startswith("bot"):
        action = data.split(" ")[1]
        games[gameID].difficulty = action
        games[gameID].inGame = True
        query.edit_message_text(games[gameID].message, reply_markup=games[gameID].showButtons())


def endGameHandler(update, context):
    gameID = update.effective_chat.id

    if not games[gameID].inGame:
        update.message.reply_text("The game has not started yet.\nUse /play")
    else:
        games[gameID].inGame = False
        games[gameID].resetAll()
        update.message.reply_text("Use /play to start a new game.")


games = {}


def main():
    token = config.token
    bot = Bot(token)
    print(bot.get_me())

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('play', play))
    dispatcher.add_handler(CommandHandler("end", endGameHandler))
    dispatcher.add_handler(MessageHandler(Filters.text, on_message))
    dispatcher.add_handler(CallbackQueryHandler(callBackHandler))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
