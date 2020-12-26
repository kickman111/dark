from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup


BUTTON1_HELP = "🚩Поддержка"
BUTTON2_PRODUCTS = "♻Товары"
BUTTON3_TOWN = "🏠В магазин"
BUTTON4_PAYMENT = "💲Оплата"
BUTTON5_FORWARD = "🔙Назад"
BUTTON6_CONTEST = "🎁Конкурс"


def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON3_TOWN),
        ],
        [
            KeyboardButton(BUTTON1_HELP),
        ],
        [
            KeyboardButton(BUTTON6_CONTEST),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

def get_forward_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON5_FORWARD),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )