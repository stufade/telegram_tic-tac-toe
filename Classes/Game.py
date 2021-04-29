import time
from random import randrange
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from minimax import smartAIMove


class Game:
    filler = "⬜️"
    userMoveSign = "❌"
    AIMoveSign = "⭕️"

    def __init__(self):
        self.desk = [[self.filler, self.filler, self.filler],
                     [self.filler, self.filler, self.filler],
                     [self.filler, self.filler, self.filler]]
        self.inGame = False
        self.message = "Choose one cell!"
        self.difficulty = "easy"
        self.depth = 9

    def makeBothMoves(self, query: CallbackQuery):
        canContine = self.userMove(query)

        if not canContine:
            return

        time.sleep(0.5)

        if self.difficulty == "easy":
            self.easyAIMove(query)
        elif self.difficulty == "hard":
            self.hardAIMove(query)

    def userMove(self, query: CallbackQuery) -> bool:
        move = int(query.data)
        row = move // 3
        column = move % 3

        if not self.inGame or self.desk[row][column] != self.filler:
            return False

        self.desk[row][column] = self.userMoveSign

        if self.checkWinGame():
            query.edit_message_text("Game Over! You won!",
                                    reply_markup=self.showButtons(True))
            self.resetAll()
            return False
        elif self.checkDrawGame():
            query.edit_message_text("Game Over! It's a draw!",
                                    reply_markup=self.showButtons(True))
            self.resetAll()
            return False
        else:
            self.message = f"Selected option: {int(query.data) + 1}"
            self.depth -= 1
            query.edit_message_text(self.message, reply_markup=self.showButtons())
            return True

    def hardAIMove(self, query: CallbackQuery) -> bool:
        x, y = smartAIMove(self.desk, self.depth)
        self.desk[x][y] = self.AIMoveSign

        if self.checkDrawGame():
            query.edit_message_text("Game Over! It's a draw!",
                                    reply_markup=self.showButtons(True))
            self.resetAll()
            return False
        elif self.checkWinGame():
            query.edit_message_text("Game Over! Bot won!",
                                    reply_markup=self.showButtons(True))
            self.resetAll()
            return False
        else:
            self.message = f"Selected option: {x * 3 + y + 1}"
            query.edit_message_text(self.message, reply_markup=self.showButtons())
            self.depth -= 1
            return True

    def easyAIMove(self, query: CallbackQuery) -> bool:
        if not self.inGame:
            return False

        x = randrange(3)
        y = randrange(3)

        while self.desk[x][y] != self.filler:
            x = randrange(3)
            y = randrange(3)

        self.desk[x][y] = self.AIMoveSign

        if self.checkDrawGame():
            query.edit_message_text("Game Over! It's a draw!",
                                    reply_markup=self.showButtons(True))
            self.resetAll()
            return False
        elif self.checkWinGame():
            query.edit_message_text("Game Over! Bot won!",
                                    reply_markup=self.showButtons(True))
            self.resetAll()
            return False
        else:
            self.message = f"Selected option: {x * 3 + y + 1}"
            query.edit_message_text(self.message, reply_markup=self.showButtons())
            self.depth -= 1
            return True

    def checkWinGame(self):
        winSituations = [
            [[0, 0], [0, 1], [0, 2]],
            [[1, 0], [1, 1], [1, 2]],
            [[2, 0], [2, 1], [2, 2]],
            [[0, 0], [1, 0], [2, 0]],
            [[0, 1], [1, 1], [2, 1]],
            [[0, 2], [1, 2], [2, 2]],
            [[0, 0], [1, 1], [2, 2]],
            [[0, 2], [1, 1], [2, 0]]
        ]

        for line in winSituations:
            x0, y0 = line[0]
            x1, y1 = line[1]
            x2, y2 = line[2]
            if self.desk[x0][y0] == self.desk[x1][y1] == self.desk[x2][y2] != self.filler:
                return True

        return False

    def checkDrawGame(self):
        for i in range(3):
            for j in range(3):
                if self.desk[i][j] == self.filler:
                    return False

        return True

    def deskReset(self):
        self.desk = [[self.filler, self.filler, self.filler],
                     [self.filler, self.filler, self.filler],
                     [self.filler, self.filler, self.filler]]

    def resetAll(self):
        self.message = "Choose one cell!"
        self.deskReset()
        self.inGame = False
        self.depth = 9

    def showButtons(self, useless=False):
        keyboard = []

        for i in range(3):
            line = []

            if useless:
                for j in range(3):
                    cell = InlineKeyboardButton(self.desk[i][j], callback_data="-1")
                    line.append(cell)
            else:
                for j in range(3):
                    cell = InlineKeyboardButton(self.desk[i][j], callback_data=f"{i * 3 + j}")
                    line.append(cell)

            keyboard.append(line)

        if not useless:
            keyboard.append([InlineKeyboardButton("End the game 🔚", callback_data="game end")])
        else:
            keyboard.append([InlineKeyboardButton("Try\nagain", callback_data="game play"),
                             InlineKeyboardButton("Change\nAI", callback_data="game change")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        return reply_markup
