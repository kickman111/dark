import datetime
from logging import getLogger

from telegram import Bot
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ParseMode
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request
import random
import re
import config
from bittrex import BittrexClient
from bittrex import BittrexError

from buttons import BUTTON1_HELP
from buttons import BUTTON2_PRODUCTS
from buttons import BUTTON3_TOWN
from buttons import BUTTON4_PAYMENT
from buttons import BUTTON5_FORWARD
from buttons import BUTTON6_CONTEST
from buttons import get_base_reply_keyboard
from buttons import get_forward_reply_keyboard


import Moscow
import Piter
import Novosibirsk
import Ekaterinburg

# config = load_config()

logger = getLogger(__name__)

# debug_requests = logger_factory(logger=logger)


# `callback_data` -- это то, что будет присылать TG при нажатии на каждую кнопку.
# Поэтому каждый идентификатор должен быть уникальным
CALLBACK_BUTTON1_LEFT = "callback_button1_left"
CALLBACK_BUTTON2_RIGHT = "callback_button2_right"
CALLBACK_BUTTON3_MORE = "callback_button3_more"
CALLBACK_BUTTON4_BACK = "callback_button4_back"
CALLBACK_BUTTON5_TIME = "callback_button5_time"
CALLBACK_BUTTON6_PRICE = "callback_button6_price"
CALLBACK_BUTTON7_PRICE = "callback_button7_price"
CALLBACK_BUTTON8_PRICE = "callback_button8_price"
CALLBACK_BUTTON9_PRICE = "callback_button9_price"
CALLBACK_BUTTON9_TOWN = "callback_button9_town"
CALLBACK_BUTTON10_TOWN = "callback_button10_town"
CALLBACK_BUTTON11_TOWN = "callback_button11_town"
CALLBACK_BUTTON12_TOWN = "callback_button12_town"


CALLBACK_BUTTON12_PRODUCT = "callback_button12_product"
CALLBACK_BUTTON13_PRODUCT = "callback_button13_product"
CALLBACK_BUTTON14_PRODUCT = "callback_button14_product"
CALLBACK_BUTTON15_PRODUCT = "callback_button15_product"
CALLBACK_BUTTON16_PRODUCT = "callback_button16_product"
CALLBACK_BUTTON17_PRODUCT = "callback_button17_product"
CALLBACK_BUTTON18_PRODUCT = "callback_button18_product"
CALLBACK_BUTTON19_PRODUCT = "callback_button19_product"
CALLBACK_BUTTON20_PRODUCT = "callback_button20_product"
CALLBACK_BUTTON21_PRODUCT = "callback_button21_product"
CALLBACK_BUTTON22_PRODUCT = "callback_button22_product"
CALLBACK_BUTTON23_PRODUCT = "callback_button23_product"
CALLBACK_BUTTON24_PRODUCT = "callback_button24_product"
CALLBACK_BUTTON25_PRODUCT = "callback_button25_product"
CALLBACK_BUTTON26_PRODUCT = "callback_button26_product"
CALLBACK_BUTTON27_PRODUCT = "callback_button27_product"

CALLBACK_BUTTON18_SEND = "callback_button18_send"


CALLBACK_BUTTON22_METRO_SPASSKAYA = "callback_button22_spasskaya"
CALLBACK_BUTTON23_METRO_SADOVAYA = "callback_button23_sadovaya"
CALLBACK_BUTTON24_METRO_DOSTOEVSKAYA = "callback_button24_dostoevskaya"


CALLBACK_BUTTON25_METRO_OKTYABRSKAYA = "callback_button25_oktyabrskaya"
CALLBACK_BUTTON26_METRO_ZAELCOVSKAYA = "callback_button26_zaelcovskaya"


CALLBACK_BUTTON_HIDE_KEYBOARD = "callback_button9_hide"

TITLES = {
    CALLBACK_BUTTON1_LEFT: "Выбери город ⚡️",
    CALLBACK_BUTTON2_RIGHT: "Выбери товар️🍏 ",
    CALLBACK_BUTTON3_MORE: "Ещё ➡️",
    CALLBACK_BUTTON4_BACK: "Назад ⬅️",
    CALLBACK_BUTTON5_TIME: "Время ⏰ ",
    CALLBACK_BUTTON6_PRICE: "BTC 💰",
    CALLBACK_BUTTON7_PRICE: "LTC 💰",
    CALLBACK_BUTTON8_PRICE: "ETH 💰",
    CALLBACK_BUTTON9_PRICE: "QIWI 💰",
    CALLBACK_BUTTON9_TOWN: "Москва",
    CALLBACK_BUTTON10_TOWN: "Питер",
    CALLBACK_BUTTON11_TOWN: "Новосибирск",
    CALLBACK_BUTTON12_TOWN: "Екатеринбург",

    CALLBACK_BUTTON12_PRODUCT: "❄Меф кристалл VHQ 1г 1500❄",
    CALLBACK_BUTTON13_PRODUCT: "❄Меф кристалл VHQ 2г 2700❄",
    CALLBACK_BUTTON14_PRODUCT: "❄Меф кристалл VHQ 5г 6000❄",
    CALLBACK_BUTTON15_PRODUCT: "⚡Альфа - PVP 1г 1700⚡",
    CALLBACK_BUTTON16_PRODUCT: "⚡Альфа - PVP 2г 3000⚡",
    CALLBACK_BUTTON17_PRODUCT: "🏃Амфетамин HQ 1г 1220🏃",
    CALLBACK_BUTTON18_PRODUCT: "🏃Амфетамин HQ 2г 2100🏃",
    CALLBACK_BUTTON19_PRODUCT: "💎MDMA кристаллы VHQ 1г 2500💎",
    CALLBACK_BUTTON20_PRODUCT: "💎MDMA кристаллы VHQ 2г 4200💎",
    CALLBACK_BUTTON21_PRODUCT: "🍬Ecstasy Marvel Superheroes 2шт 1750🍬",
    CALLBACK_BUTTON22_PRODUCT: "🍫Гашиш BlackRock Hash 1г 1550🍫",
    CALLBACK_BUTTON23_PRODUCT: "🍫Гашиш BlackRock Hash 2г 2430🍫",
    CALLBACK_BUTTON24_PRODUCT: "🎄Шишки OG KUSH 1г 1500🎄",
    CALLBACK_BUTTON25_PRODUCT: "🎄Шишки OG KUSH 2г 2200🎄",
    CALLBACK_BUTTON26_PRODUCT: "🎄Шишки Crystal Haze 1г 1650🎄",
    CALLBACK_BUTTON27_PRODUCT: "🎄Шишки Crystal Haze 2г 2300🎄",
    CALLBACK_BUTTON18_SEND: "Платеж отправлен 🚀 ",

    Moscow.CALLBACK_BUTTON1_CAO: "ЦАО",
    Moscow.CALLBACK_BUTTON2_NORTHERN: "САО",
    Moscow.CALLBACK_BUTTON3_NORTHEASTERN: "СВАО",
    Moscow.CALLBACK_BUTTON4_EASTERN: "ВАО",
    Moscow.CALLBACK_BUTTON5_SOUTHEASTERN: "ЮВАО",
    Moscow.CALLBACK_BUTTON6_SOUTHERN: "ЮАО",
    Moscow.CALLBACK_BUTTON7_SOUTHWESTERN: "ЮЗАО",
    Moscow.CALLBACK_BUTTON8_WESTERN: "ЗАО",
    Moscow.CALLBACK_BUTTON9_NORTHWESTERN: "СЗАО",

    Moscow.CALLBACK_BUTTON_METRO_TAGANSKAYA: "Таганская ",
    Moscow.CALLBACK_BUTTON_METRO_MAYAKOVSKAYA: "Маяковская ",
    Moscow.CALLBACK_BUTTON_METRO_TVERSKAYA: "Тверская ",
    Moscow.CALLBACK_BUTTON_METRO_BAUMANSKAYA: "Бауманская ",
    Moscow.CALLBACK_BUTTON_METRO_LUBANKA: "Лубянка ",
    Moscow.CALLBACK_BUTTON_METRO_PUSHKINSKAYA: "Пушкинская ",
    Moscow.CALLBACK_BUTTON_METRO_MARKSITSKAYA: "Маркситская ",
    Moscow.CALLBACK_BUTTON_METRO_PAVELECKAYA: "Павелецкая ",
    Moscow.CALLBACK_BUTTON_METRO_KURSKAYA: "Курская ",
    Moscow.CALLBACK_BUTTON_METRO_ARBATSKAYA: "Арбатская ",
    Moscow.CALLBACK_BUTTON_METRO_OHOTNIYRYAD: "Охотный ряд ",

    Moscow.CALLBACK_BUTTON_METRO_KIEVSKAYA: "Киевская",
    Moscow.CALLBACK_BUTTON_METRO_FILI: "Фили ",
    Moscow.CALLBACK_BUTTON_METRO_STUDENCHESKAYA: "Студенческая ",
    Moscow.CALLBACK_BUTTON_METRO_PIONERSKAYA: "Пионерская ",
    Moscow.CALLBACK_BUTTON_METRO_KUTUZOVSKAYA: "Кутузовская ",
    Moscow.CALLBACK_BUTTON_METRO_KRILATSKOE: "Крылатское ",
    Moscow.CALLBACK_BUTTON_METRO_MOLODEZNAYA: "Молодежная ",

    Moscow.CALLBACK_BUTTON_METRO_AEROPORT: "Аэропорт ",
    Moscow.CALLBACK_BUTTON_METRO_BEGOVAYA: "Беговая ",
    Moscow.CALLBACK_BUTTON_METRO_SOKOL: "Сокол ",
    Moscow.CALLBACK_BUTTON_METRO_DINAMO: "Динамо ",
    Moscow.CALLBACK_BUTTON_METRO_TIMIRYAZEVSKAYA: "Тимирязевская ",
    Moscow.CALLBACK_BUTTON_METRO_POLEZAEVSKAYA: "Полежаевская ",
    Moscow.CALLBACK_BUTTON_METRO_VOYKOVSKAYA: "Войковская",

    Moscow.CALLBACK_BUTTON_METRO_NOVOGIREEVO: "Новогиреево ",
    Moscow.CALLBACK_BUTTON_METRO_PEROVO: "Перово ",
    Moscow.CALLBACK_BUTTON_METRO_SCHELKOVSKAYA: "Щелковская ",
    Moscow.CALLBACK_BUTTON_METRO_IZMAYLOVSKAYA: "Измайловская ",
    Moscow.CALLBACK_BUTTON_METRO_VIHINO: "Выхино ",
    Moscow.CALLBACK_BUTTON_METRO_SOKOLNIKI: "Сокольники ",
    Moscow.CALLBACK_BUTTON_METRO_SEMENOVSKAYA: "Семеновская ",

    Moscow.CALLBACK_BUTTON_METRO_VDNH: "ВДНХ ",
    Moscow.CALLBACK_BUTTON_METRO_BABUSHKINSKAYA: "Бабушкинская ",
    Moscow.CALLBACK_BUTTON_METRO_OTRADNOE: "Отрадное ",
    Moscow.CALLBACK_BUTTON_METRO_ALEKSEEVSKAYA: "Алексеевская ",
    Moscow.CALLBACK_BUTTON_METRO_ALTUFEVO: "Алтуфьево ",
    Moscow.CALLBACK_BUTTON_METRO_MEDVEDKOVO: "Медведково ",
    Moscow.CALLBACK_BUTTON_METRO_VLADIKINO: "Владыкино ",

    Moscow.CALLBACK_BUTTON_METRO_PLANERNAYA: "Планерная ",
    Moscow.CALLBACK_BUTTON_METRO_SHODNENSKAYA: "Сходненская ",
    Moscow.CALLBACK_BUTTON_METRO_TUSHINSKAYA: "Тушинская ",
    Moscow.CALLBACK_BUTTON_METRO_SCHUKINSKAYA: "Щукинская ",

    Moscow.CALLBACK_BUTTON_METRO_AVIAMOTORNAYA: "Авиамоторная ",
    Moscow.CALLBACK_BUTTON_METRO_TEKSTILSCHIKI: "Текстильщики ",
    Moscow.CALLBACK_BUTTON_METRO_KUZMINKI: "Кузьминки ",
    Moscow.CALLBACK_BUTTON_METRO_RAZANSKIYPROSPECT: "Рязанский проспект ",
    Moscow.CALLBACK_BUTTON_METRO_DUBROVKA: "Дубровка ",
    Moscow.CALLBACK_BUTTON_METRO_PECHATNIKI: "Печатники ",
    Moscow.CALLBACK_BUTTON_METRO_LUBLINO: "Люблино ",

    Moscow.CALLBACK_BUTTON_METRO_SHABOLOVSKAYA: "Шаболовская ",
    Moscow.CALLBACK_BUTTON_METRO_AVTOZAVODSKAYA: "Автозаводская ",
    Moscow.CALLBACK_BUTTON_METRO_KASHIRSKAYA: "Каширская ",
    Moscow.CALLBACK_BUTTON_METRO_UZNAYA: "Южная ",
    Moscow.CALLBACK_BUTTON_METRO_NAGORNAYA: "Нагорная ",
    Moscow.CALLBACK_BUTTON_METRO_ANNINO: "Аннино ",
    Moscow.CALLBACK_BUTTON_METRO_DOMODEDOVSKAYA: "Домодедовская ",

    Moscow.CALLBACK_BUTTON_METRO_LENINSKIY: "Ленинский проспект ",
    Moscow.CALLBACK_BUTTON_METRO_YASENEVO: "Ясенево ",
    Moscow.CALLBACK_BUTTON_METRO_AKADEMICHESKAYA: "Академическая ",
    Moscow.CALLBACK_BUTTON_METRO_PROFSOUZNAYA: "Профсоюзная ",
    Moscow.CALLBACK_BUTTON_METRO_KAHOVSKAYA: "Каховская ",
    Moscow.CALLBACK_BUTTON_METRO_KALUZSKAYA: "Калужская ",
    Moscow.CALLBACK_BUTTON_METRO_KONKOVO: "Коньково ",

    Piter.CALLBACK_BUTTON1_Admiralteyskiy: "Адмиралтейский",
    Piter.CALLBACK_BUTTON2_Vasileostrovsiy: "Василеостровский",
    Piter.CALLBACK_BUTTON3_Viborgskiy: "Выборгский",
    Piter.CALLBACK_BUTTON4_Kalininskiy: "Калининский",
    Piter.CALLBACK_BUTTON5_Kirovskiy: "Кировский",
    Piter.CALLBACK_BUTTON6_Krasnogvardeyskiy: "Красногвардейский",
    Piter.CALLBACK_BUTTON7_Kronshtadskiy: "Кронштадский",
    Piter.CALLBACK_BUTTON8_Moscowskiy: "Московский",
    Piter.CALLBACK_BUTTON9_Nevskiy: "Невский",
    Piter.CALLBACK_BUTTON10_Petrogradskiy: "Петроградский",
    Piter.CALLBACK_BUTTON11_Primorskiy: "Приморский",
    Piter.CALLBACK_BUTTON12_Pushkinskiy: "Пушкинский",
    Piter.CALLBACK_BUTTON13_Frunzinskiy: "Фрунзенский",
    Piter.CALLBACK_BUTTON14_Centralniy: "Центральный",

    Piter.CALLBACK_BUTTON_METRO_ADMIRALTEYSKAYA: "Адмиралтейская",
    Piter.CALLBACK_BUTTON_METRO_SADOVAYA: "Садовая",
    Piter.CALLBACK_BUTTON_METRO_ZVENIGORODSKAYA: "Звенигородская",
    Piter.CALLBACK_BUTTON_METRO_NEVSKIYPROSPECT: "Невский проспект",
    Piter.CALLBACK_BUTTON_METRO_PRIMORSKAYA: "Приморская",
    Piter.CALLBACK_BUTTON_METRO_VASILEOSTROVSKAYA: "Василеостровская",
    Piter.CALLBACK_BUTTON_METRO_GAVAN: "Гавань",
    Piter.CALLBACK_BUTTON_METRO_UDELNAYA: "Удельная",
    Piter.CALLBACK_BUTTON_METRO_OZERKI: "Озерки",
    Piter.CALLBACK_BUTTON_METRO_PARNAS: "Парнас",
    Piter.CALLBACK_BUTTON_METRO_VIBORGSKAYA: "Выборгская",
    Piter.CALLBACK_BUTTON_METRO_LESNAYA: "Лесная",
    Piter.CALLBACK_BUTTON_METRO_GRAJDANSKIYPROSPECT: "Гражданский проспект",
    Piter.CALLBACK_BUTTON_METRO_POLITEHNICHESKAYA: "Политехническая",
    Piter.CALLBACK_BUTTON_METRO_PLOSCHADMUJESTVA: "Площадь Мужества",
    Piter.CALLBACK_BUTTON_METRO_NARVSKAYA: "Нарвская",
    Piter.CALLBACK_BUTTON_METRO_AVTOVO: "Автово",
    Piter.CALLBACK_BUTTON_METRO_NOVOCHERKASSKAYA: "Новочеркасская",
    Piter.CALLBACK_BUTTON_METRO_LADOJSKAYA: "Ладожская",
    Piter.CALLBACK_BUTTON_METRO_KRESTOVSKIYOSTROV: "Крестовский остров",
    Piter.CALLBACK_BUTTON_METRO_STARAYADEREVNYA: "Старая Деревня",
    Piter.CALLBACK_BUTTON_METRO_ELECTROSILA: "Электросила",
    Piter.CALLBACK_BUTTON_METRO_ZVEZDNAYA: "Звездная",
    Piter.CALLBACK_BUTTON_METRO_KUPCHINO: "Купчино",
    Piter.CALLBACK_BUTTON_METRO_ULICADIBENKO: "Улица Дыбенко",
    Piter.CALLBACK_BUTTON_METRO_PROSPECTBOLSHEVIKOV: "Проспект Большевиков",
    Piter.CALLBACK_BUTTON_METRO_GORKOVSKAYA: "Горковская",
    Piter.CALLBACK_BUTTON_METRO_ZENIT: "Зенит",
    Piter.CALLBACK_BUTTON_METRO_CHKALOVSKAYA: "Чкаловская",
    Piter.CALLBACK_BUTTON_METRO_CHERNAYARECHKA: "Черная Речка",
    Piter.CALLBACK_BUTTON_METRO_PIONERSKAYA: "Пионерская",
    Piter.CALLBACK_BUTTON_METRO_SHUSHARI: "Шушари",
    Piter.CALLBACK_BUTTON_METRO_BUHARESTSKAYA: "Бухарестская",
    Piter.CALLBACK_BUTTON_METRO_PROSPECTSLAVI: "Проспект Славы",
    Piter.CALLBACK_BUTTON_METRO_CHERNISHEVSKAYA: "Чернышевская",
    Piter.CALLBACK_BUTTON_METRO_GOSTINIYDVOR: "Гостинный Двор",
    Piter.CALLBACK_BUTTON_METRO_LIGOVSKIY: "Лиговский",

    Novosibirsk.CALLBACK_BUTTON1_Dzerzhinsky: "Дзержинский",
    Novosibirsk.CALLBACK_BUTTON2_Zeleznodorozny: "Железнодорожный",
    Novosibirsk.CALLBACK_BUTTON3_Zaelcovskiy: "Заельцовский",
    Novosibirsk.CALLBACK_BUTTON4_Leninsky: "Ленинский",
    Novosibirsk.CALLBACK_BUTTON5_Oktyabrsky: "Октябрьский",
    Novosibirsk.CALLBACK_BUTTON6_Pervomaysky: "Первомайский",

    Novosibirsk.CALLBACK_BUTTON_AREA_BEREZOVAYAROSCHA: "Березовая Роща",
    Novosibirsk.CALLBACK_BUTTON_AREA_ZOLOTAYANIVA: "Золотая Нива",
    Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADGARINAMIHAYLOVSKOGO: "Площадь Гарина Михайловского",
    Novosibirsk.CALLBACK_BUTTON_AREA_ZAELCOVSKAYA: "Заельцовская",
    Novosibirsk.CALLBACK_BUTTON_AREA_MARSHALAPOKRISHKINA: "Маршала Покрышкина",
    Novosibirsk.CALLBACK_BUTTON_AREA_STUDENCHESKAYA: "Студенческая",
    Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADMARKSA: "Площадь Маркса",
    Novosibirsk.CALLBACK_BUTTON_AREA_OKTYABRSKAYA: "Октябрьская",
    Novosibirsk.CALLBACK_BUTTON_AREA_KAMENSKAYA: "Каменская",
    Novosibirsk.CALLBACK_BUTTON_AREA_NIKITSKAYA: "Никитская",

    Ekaterinburg.CALLBACK_BUTTON1_VerhIsetskiy: "Верх-Исетский",
    Ekaterinburg.CALLBACK_BUTTON2_Zheleznodorozhniy: "Железнодорожный",
    Ekaterinburg.CALLBACK_BUTTON3_Kirovskiy: "Кировский",
    Ekaterinburg.CALLBACK_BUTTON4_Leninskiy: "Ленинский",
    Ekaterinburg.CALLBACK_BUTTON5_Oktyabrskiy: "Октябрьский",
    Ekaterinburg.CALLBACK_BUTTON6_Ordzhonikidzevskiy: "Орджоникидзевский",
    Ekaterinburg.CALLBACK_BUTTON7_Chkalovskiy: "Чкаловский",

    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHIROKAYARECHKA: "Широкая Речка",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORAKHRUSTALNAYA: "Гора Хрустальная",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LISTVENNIY: "Лиственный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PEREGON: "Перегон",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SVETLAYARECHKA: "Светлая Речка",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_AKADEMICHESKIY: "Академический",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VIZ: "ВИЗ",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ZARECHNIY: "Заречный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VOKZALNIY: "Вокзальный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORNOZAVODSKIY: "Горнозаводский",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PALKINO: "Палкино",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEMKLYUCHEI: "Семь Ключей",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_STARAYASORTIROVKA: "Старая Сортировка",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NOVAYASORTIROVKA: "Новая Сортировка",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEVERNIYPROMYSHLENNIY: "Северный Промышленный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SORTIROVOCHNIY: "Сортировочный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTUZGORODOK: "Втузгородок",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_IZOPLIT: "Изоплит",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KALINOVSKIY: "Калиновский",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMSOMOLSKIY: "Комсомольский",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PIONERSKIY: "Пионерский",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_CENTRALNIY: "Центральный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHARTASH: "Шарташ",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUGOZAPADNIY: "Югозападный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSKOVSKAYAGORKA: "Московская горка",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UNC: "УНЦ",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOLTSOVO: "Кольцово",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMPRESSORNIY: "Компрессорный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MALYIISTOK: "Малый Исток",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PARKOVIY: "Парковый",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SIBIRSKIY: "Сибирский",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SINIEKAMNI: "Синие Камни",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GLUBOKOE: "Глубокое",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSTOVKA: "Мостовка",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LECHEBNIY: "Лечебный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PTICEFABRIKA: "Птицефабрика",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_URALMASH: "Уралмаш",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELMASH: "Елмаш",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOZLOVSKIY: "Козловский",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_APPARATNIY: "Аппаратный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YAGODNIY: "Ягодный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_BOTANICHESKIY: "Ботанический",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTORCHERMET: "Вторчермет",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELIZAVET: "Елизавет",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NIZHNEISETSKIY: "Нижне-Исетский",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_RUDNIY: "Рудный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UKTUSSKIY: "Уктусский",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHIMMASH: "Химмаш",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUZHNIY: "Южный",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PRIISKOVIY: "Приисковый",
    Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHUTOR: "Хутор",



    CALLBACK_BUTTON22_METRO_SPASSKAYA: "Спасская ",
    CALLBACK_BUTTON23_METRO_SADOVAYA: "Садовая ",
    CALLBACK_BUTTON24_METRO_DOSTOEVSKAYA: "Достоевская ",



    CALLBACK_BUTTON25_METRO_OKTYABRSKAYA: "Октябрьская ",
    CALLBACK_BUTTON26_METRO_ZAELCOVSKAYA: "Заельцовская ",
    CALLBACK_BUTTON_HIDE_KEYBOARD: "Спрять клавиатуру 🍱 ",
}

# Глобально инициализируем клиент API Bittrex
client = BittrexClient()


def get_base_inline_keyboard():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_LEFT], callback_data=CALLBACK_BUTTON1_LEFT),
        ],
        # [
        #     InlineKeyboardButton(TITLES[CALLBACK_BUTTON_HIDE_KEYBOARD], callback_data=CALLBACK_BUTTON_HIDE_KEYBOARD),
        # ],
        # [
        #     InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_MORE], callback_data=CALLBACK_BUTTON3_MORE),
        # ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_base_inline_keyboard_products():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_RIGHT], callback_data=CALLBACK_BUTTON2_RIGHT),
        ],
        # [
        #     InlineKeyboardButton(TITLES[CALLBACK_BUTTON_HIDE_KEYBOARD], callback_data=CALLBACK_BUTTON_HIDE_KEYBOARD),
        # ],
        # [
        #     InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_MORE], callback_data=CALLBACK_BUTTON3_MORE),
        # ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_TAGANSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_TAGANSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_MAYAKOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_MAYAKOVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_PEROVO], callback_data=Moscow.CALLBACK_BUTTON_METRO_PEROVO),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro_cao():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_TAGANSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_TAGANSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_MAYAKOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_MAYAKOVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_TVERSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_TVERSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_BAUMANSKAYA],
                                 callback_data=Moscow.CALLBACK_BUTTON_METRO_BAUMANSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_LUBANKA],
                                 callback_data=Moscow.CALLBACK_BUTTON_METRO_LUBANKA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_PUSHKINSKAYA],
                                 callback_data=Moscow.CALLBACK_BUTTON_METRO_PUSHKINSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_MARKSITSKAYA],
                                 callback_data=Moscow.CALLBACK_BUTTON_METRO_MARKSITSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_PAVELECKAYA],
                                 callback_data=Moscow.CALLBACK_BUTTON_METRO_PAVELECKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_KURSKAYA],
                                 callback_data=Moscow.CALLBACK_BUTTON_METRO_KURSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_ARBATSKAYA],
                                 callback_data=Moscow.CALLBACK_BUTTON_METRO_ARBATSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_OHOTNIYRYAD],
                                 callback_data=Moscow.CALLBACK_BUTTON_METRO_OHOTNIYRYAD),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro_northern():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_AEROPORT], callback_data=Moscow.CALLBACK_BUTTON_METRO_AEROPORT),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_BEGOVAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_BEGOVAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_SOKOL], callback_data=Moscow.CALLBACK_BUTTON_METRO_SOKOLNIKI),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_DINAMO], callback_data=Moscow.CALLBACK_BUTTON_METRO_DINAMO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_TIMIRYAZEVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_TIMIRYAZEVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_POLEZAEVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_POLEZAEVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_VOYKOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_VOYKOVSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro_northeastern():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_VDNH], callback_data=Moscow.CALLBACK_BUTTON_METRO_VDNH),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_BABUSHKINSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_BABUSHKINSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_OTRADNOE], callback_data=Moscow.CALLBACK_BUTTON_METRO_OTRADNOE),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_ALEKSEEVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_ALEKSEEVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_ALTUFEVO], callback_data=Moscow.CALLBACK_BUTTON_METRO_ALTUFEVO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_MEDVEDKOVO], callback_data=Moscow.CALLBACK_BUTTON_METRO_MEDVEDKOVO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_VLADIKINO], callback_data=Moscow.CALLBACK_BUTTON_METRO_VLADIKINO),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro_eastern():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_NOVOGIREEVO], callback_data=Moscow.CALLBACK_BUTTON_METRO_NOVOGIREEVO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_IZMAYLOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_IZMAYLOVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_PEROVO], callback_data=Moscow.CALLBACK_BUTTON_METRO_PEROVO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_SCHELKOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_SCHELKOVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_VIHINO], callback_data=Moscow.CALLBACK_BUTTON_METRO_VIHINO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_SOKOLNIKI], callback_data=Moscow.CALLBACK_BUTTON_METRO_SOKOLNIKI),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_SEMENOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_SEMENOVSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro_southeastern():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_AVIAMOTORNAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_AVIAMOTORNAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_TEKSTILSCHIKI], callback_data=Moscow.CALLBACK_BUTTON_METRO_TEKSTILSCHIKI),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_RAZANSKIYPROSPECT], callback_data=Moscow.CALLBACK_BUTTON_METRO_RAZANSKIYPROSPECT),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_KUZMINKI], callback_data=Moscow.CALLBACK_BUTTON_METRO_KUZMINKI),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_DUBROVKA], callback_data=Moscow.CALLBACK_BUTTON_METRO_DUBROVKA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_PECHATNIKI], callback_data=Moscow.CALLBACK_BUTTON_METRO_PECHATNIKI),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_LUBLINO], callback_data=Moscow.CALLBACK_BUTTON_METRO_LUBLINO),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro_southern():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_SHABOLOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_SHABOLOVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_AVTOZAVODSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_AVTOZAVODSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_KASHIRSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_KASHIRSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_UZNAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_UZNAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_NAGORNAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_NAGORNAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_ANNINO], callback_data=Moscow.CALLBACK_BUTTON_METRO_ANNINO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_DOMODEDOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_DOMODEDOVSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro_southwestern():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_LENINSKIY], callback_data=Moscow.CALLBACK_BUTTON_METRO_LENINSKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_AKADEMICHESKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_AKADEMICHESKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_PROFSOUZNAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_PROFSOUZNAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_YASENEVO], callback_data=Moscow.CALLBACK_BUTTON_METRO_YASENEVO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_KALUZSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_KALUZSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_KONKOVO], callback_data=Moscow.CALLBACK_BUTTON_METRO_KONKOVO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_KAHOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_KAHOVSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro_western():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_KIEVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_KIEVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_FILI], callback_data=Moscow.CALLBACK_BUTTON_METRO_FILI),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_STUDENCHESKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_STUDENCHESKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_PIONERSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_PIONERSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_KUTUZOVSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_KUTUZOVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_KRILATSKOE], callback_data=Moscow.CALLBACK_BUTTON_METRO_KRILATSKOE),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_MOLODEZNAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_MOLODEZNAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_metro_northwestern():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_PLANERNAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_PLANERNAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_SHODNENSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_SHODNENSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_TUSHINSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_TUSHINSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON_METRO_SCHUKINSKAYA], callback_data=Moscow.CALLBACK_BUTTON_METRO_SCHUKINSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_moscow_area():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON1_CAO], callback_data=Moscow.CALLBACK_BUTTON1_CAO),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON2_NORTHERN], callback_data=Moscow.CALLBACK_BUTTON2_NORTHERN),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON3_NORTHEASTERN], callback_data=Moscow.CALLBACK_BUTTON3_NORTHEASTERN),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON4_EASTERN], callback_data=Moscow.CALLBACK_BUTTON4_EASTERN),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON5_SOUTHEASTERN], callback_data=Moscow.CALLBACK_BUTTON5_SOUTHEASTERN),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON6_SOUTHERN], callback_data=Moscow.CALLBACK_BUTTON6_SOUTHERN),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON7_SOUTHWESTERN], callback_data=Moscow.CALLBACK_BUTTON7_SOUTHWESTERN),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON8_WESTERN], callback_data=Moscow.CALLBACK_BUTTON8_WESTERN),
        ],
        [
            InlineKeyboardButton(TITLES[Moscow.CALLBACK_BUTTON9_NORTHWESTERN], callback_data=Moscow.CALLBACK_BUTTON9_NORTHWESTERN),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON22_METRO_SPASSKAYA], callback_data=CALLBACK_BUTTON22_METRO_SPASSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON23_METRO_SADOVAYA], callback_data=CALLBACK_BUTTON23_METRO_SADOVAYA),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON24_METRO_DOSTOEVSKAYA], callback_data=CALLBACK_BUTTON24_METRO_DOSTOEVSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_area():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON1_Admiralteyskiy], callback_data=Piter.CALLBACK_BUTTON1_Admiralteyskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON2_Vasileostrovsiy], callback_data=Piter.CALLBACK_BUTTON2_Vasileostrovsiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON3_Viborgskiy], callback_data=Piter.CALLBACK_BUTTON3_Viborgskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON4_Kalininskiy], callback_data=Piter.CALLBACK_BUTTON4_Kalininskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON5_Kirovskiy], callback_data=Piter.CALLBACK_BUTTON5_Kirovskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON6_Krasnogvardeyskiy], callback_data=Piter.CALLBACK_BUTTON6_Krasnogvardeyskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON7_Kronshtadskiy], callback_data=Piter.CALLBACK_BUTTON7_Kronshtadskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON8_Moscowskiy], callback_data=Piter.CALLBACK_BUTTON8_Moscowskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON9_Nevskiy], callback_data=Piter.CALLBACK_BUTTON9_Nevskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON10_Petrogradskiy], callback_data=Piter.CALLBACK_BUTTON10_Petrogradskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON11_Primorskiy],
                                 callback_data=Piter.CALLBACK_BUTTON11_Primorskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON12_Pushkinskiy],
                                 callback_data=Piter.CALLBACK_BUTTON12_Pushkinskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON13_Frunzinskiy],
                                 callback_data=Piter.CALLBACK_BUTTON13_Frunzinskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON14_Centralniy],
                                 callback_data=Piter.CALLBACK_BUTTON14_Centralniy),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_admiralteyskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_ADMIRALTEYSKAYA], callback_data=Piter.CALLBACK_BUTTON_METRO_ADMIRALTEYSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_SADOVAYA], callback_data=Piter.CALLBACK_BUTTON_METRO_SADOVAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_ZVENIGORODSKAYA], callback_data=Piter.CALLBACK_BUTTON_METRO_ZVENIGORODSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_NEVSKIYPROSPECT],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_NEVSKIYPROSPECT),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_vasileostrovsiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_PRIMORSKAYA], callback_data=Piter.CALLBACK_BUTTON_METRO_PRIMORSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_VASILEOSTROVSKAYA], callback_data=Piter.CALLBACK_BUTTON_METRO_VASILEOSTROVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_GAVAN], callback_data=Piter.CALLBACK_BUTTON_METRO_GAVAN),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_viborgskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_UDELNAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_UDELNAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_OZERKI],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_OZERKI),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_PARNAS],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_PARNAS),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_VIBORGSKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_VIBORGSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_LESNAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_LESNAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_kalininskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_GRAJDANSKIYPROSPECT],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_GRAJDANSKIYPROSPECT),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_POLITEHNICHESKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_POLITEHNICHESKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_PLOSCHADMUJESTVA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_PLOSCHADMUJESTVA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_kirovskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_NARVSKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_NARVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_AVTOVO],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_AVTOVO),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_krasnogvardeyskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_NOVOCHERKASSKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_NOVOCHERKASSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_LADOJSKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_LADOJSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_kronshtadskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_KRESTOVSKIYOSTROV],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_KRESTOVSKIYOSTROV),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_STARAYADEREVNYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_STARAYADEREVNYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_moscowskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_ELECTROSILA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_ELECTROSILA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_ZVEZDNAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_ZVEZDNAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_KUPCHINO],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_KUPCHINO),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_nevskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_ULICADIBENKO],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_ULICADIBENKO),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_PROSPECTBOLSHEVIKOV],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_PROSPECTBOLSHEVIKOV),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_petrogradskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_GORKOVSKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_GORKOVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_ZENIT],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_ZENIT),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_CHKALOVSKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_CHKALOVSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_primorskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_CHERNAYARECHKA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_CHERNAYARECHKA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_PIONERSKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_PIONERSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_pushkinskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_SHUSHARI],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_SHUSHARI),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_frunzinskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_BUHARESTSKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_BUHARESTSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_PROSPECTSLAVI],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_PROSPECTSLAVI),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_piter_metro_centralniy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_CHERNISHEVSKAYA],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_CHERNISHEVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_GOSTINIYDVOR],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_GOSTINIYDVOR),
        ],
        [
            InlineKeyboardButton(TITLES[Piter.CALLBACK_BUTTON_METRO_LIGOVSKIY],
                                 callback_data=Piter.CALLBACK_BUTTON_METRO_LIGOVSKIY),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_novosibirsk_area():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON1_Dzerzhinsky], callback_data=Novosibirsk.CALLBACK_BUTTON1_Dzerzhinsky),
        ],
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON2_Zeleznodorozny], callback_data=Novosibirsk.CALLBACK_BUTTON2_Zeleznodorozny),
        ],
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON3_Zaelcovskiy], callback_data=Novosibirsk.CALLBACK_BUTTON3_Zaelcovskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON4_Leninsky], callback_data=Novosibirsk.CALLBACK_BUTTON4_Leninsky),
        ],
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON5_Oktyabrsky], callback_data=Novosibirsk.CALLBACK_BUTTON5_Oktyabrsky),
        ],
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON6_Pervomaysky], callback_data=Novosibirsk.CALLBACK_BUTTON6_Pervomaysky),
        ],

    ]
    return InlineKeyboardMarkup(keyboard)

def get_novosibirsk_metro_dzerzhinsky():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_BEREZOVAYAROSCHA], callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_BEREZOVAYAROSCHA),
        ],
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_ZOLOTAYANIVA], callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_ZOLOTAYANIVA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_novosibirsk_metro_zeleznodorozny():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADGARINAMIHAYLOVSKOGO], callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADGARINAMIHAYLOVSKOGO),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_novosibirsk_metro_zaelcovskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_ZAELCOVSKAYA],
                                 callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_ZAELCOVSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_MARSHALAPOKRISHKINA],
                                 callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_MARSHALAPOKRISHKINA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_novosibirsk_metro_leninsky():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_STUDENCHESKAYA],
                                 callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_STUDENCHESKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADMARKSA],
                                 callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADMARKSA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_novosibirsk_metro_oktyabrsky():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_OKTYABRSKAYA],
                                 callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_OKTYABRSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_novosibirsk_metro_pervomaysky():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_KAMENSKAYA],
                                 callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_KAMENSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Novosibirsk.CALLBACK_BUTTON_AREA_NIKITSKAYA],
                                 callback_data=Novosibirsk.CALLBACK_BUTTON_AREA_NIKITSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ekaterinburg_area():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON1_VerhIsetskiy],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON1_VerhIsetskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON2_Zheleznodorozhniy],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON2_Zheleznodorozhniy),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON3_Kirovskiy],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON3_Kirovskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON4_Leninskiy],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON4_Leninskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON5_Oktyabrskiy],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON5_Oktyabrskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON6_Ordzhonikidzevskiy],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON6_Ordzhonikidzevskiy),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON7_Chkalovskiy],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON7_Chkalovskiy),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ekaterinburg_metro_verhisetskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHIROKAYARECHKA],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHIROKAYARECHKA),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORAKHRUSTALNAYA],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORAKHRUSTALNAYA),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LISTVENNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LISTVENNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PEREGON],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PEREGON),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SVETLAYARECHKA],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SVETLAYARECHKA),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VIZ],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ZARECHNIY),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ekaterinburg_metro_zheleznodorozhniy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VOKZALNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VOKZALNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORNOZAVODSKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORNOZAVODSKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PALKINO],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PALKINO),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEMKLYUCHEI],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEMKLYUCHEI),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_STARAYASORTIROVKA],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_STARAYASORTIROVKA),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NOVAYASORTIROVKA],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NOVAYASORTIROVKA),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SORTIROVOCHNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SORTIROVOCHNIY),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ekaterinburg_metro_kirovskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTUZGORODOK],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTUZGORODOK),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_IZOPLIT],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_IZOPLIT),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KALINOVSKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KALINOVSKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMSOMOLSKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMSOMOLSKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PIONERSKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PIONERSKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_CENTRALNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_CENTRALNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHARTASH],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHARTASH),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ekaterinburg_metro_Leninskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUGOZAPADNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUGOZAPADNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSKOVSKAYAGORKA],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSKOVSKAYAGORKA),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UNC],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UNC),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_AKADEMICHESKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_AKADEMICHESKIY),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ekaterinburg_metro_oktyabrskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOLTSOVO],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOLTSOVO),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMPRESSORNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMPRESSORNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MALYIISTOK],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MALYIISTOK),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PARKOVIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PARKOVIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SIBIRSKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SIBIRSKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SINIEKAMNI],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SINIEKAMNI),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GLUBOKOE],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GLUBOKOE),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSTOVKA],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSTOVKA),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LECHEBNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LECHEBNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PTICEFABRIKA],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PTICEFABRIKA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ekaterinburg_metro_ordzhonikidzevskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEVERNIYPROMYSHLENNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEVERNIYPROMYSHLENNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_URALMASH],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_URALMASH),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELMASH],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELMASH),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOZLOVSKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOZLOVSKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_APPARATNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_APPARATNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YAGODNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YAGODNIY),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ekaterinburg_metro_chkalovskiy():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_BOTANICHESKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_BOTANICHESKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTORCHERMET],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTORCHERMET),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELIZAVET],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELIZAVET),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NIZHNEISETSKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NIZHNEISETSKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_RUDNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_RUDNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UKTUSSKIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UKTUSSKIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHIMMASH],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHIMMASH),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUZHNIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUZHNIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PRIISKOVIY],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PRIISKOVIY),
        ],
        [
            InlineKeyboardButton(TITLES[Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHUTOR],
                                 callback_data=Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHUTOR),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_novosib_metro():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON25_METRO_OKTYABRSKAYA], callback_data=CALLBACK_BUTTON25_METRO_OKTYABRSKAYA),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON26_METRO_ZAELCOVSKAYA], callback_data=CALLBACK_BUTTON26_METRO_ZAELCOVSKAYA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
# def get_keyboard2():
#     """ Получить вторую страницу клавиатуры для сообщений
#         Возможно получить только при нажатии кнопки на первой клавиатуре
#     """
#     keyboard = [
#         [
#             InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_TIME], callback_data=CALLBACK_BUTTON5_TIME),
#         ],
#         [
#             InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_PRICE], callback_data=CALLBACK_BUTTON6_PRICE),
#             InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_PRICE], callback_data=CALLBACK_BUTTON7_PRICE),
#             InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_PRICE], callback_data=CALLBACK_BUTTON8_PRICE),
#         ],
#         [
#             InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
#         ],
#     ]
#     return InlineKeyboardMarkup(keyboard)

def get_keyboard2():
    """ Получить вторую страницу клавиатуры для сообщений
        Возможно получить только при нажатии кнопки на первой клавиатуре
    """
    keyboard = [
        # [
        #     InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_TIME], callback_data=CALLBACK_BUTTON5_TIME),
        # ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_PRICE], callback_data=CALLBACK_BUTTON6_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_PRICE], callback_data=CALLBACK_BUTTON7_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_PRICE], callback_data=CALLBACK_BUTTON8_PRICE),
            # InlineKeyboardButton(TITLES[CALLBACK_BUTTON9_PRICE], callback_data=CALLBACK_BUTTON9_PRICE),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_payments():
    """ Получить вторую страницу клавиатуры для сообщений
        Возможно получить только при нажатии кнопки на первой клавиатуре
    """
    keyboard = [
        # [
        #     InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_TIME], callback_data=CALLBACK_BUTTON5_TIME),
        # ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_PRICE], callback_data=CALLBACK_BUTTON6_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_PRICE], callback_data=CALLBACK_BUTTON7_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_PRICE], callback_data=CALLBACK_BUTTON8_PRICE),
            # InlineKeyboardButton(TITLES[CALLBACK_BUTTON9_PRICE], callback_data=CALLBACK_BUTTON9_PRICE),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON18_SEND], callback_data=CALLBACK_BUTTON18_SEND),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_towns():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON9_TOWN], callback_data=CALLBACK_BUTTON9_TOWN),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON10_TOWN], callback_data=CALLBACK_BUTTON10_TOWN),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON11_TOWN], callback_data=CALLBACK_BUTTON11_TOWN),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON12_TOWN], callback_data=CALLBACK_BUTTON12_TOWN),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_products():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON12_PRODUCT], callback_data=CALLBACK_BUTTON12_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON13_PRODUCT], callback_data=CALLBACK_BUTTON13_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON14_PRODUCT], callback_data=CALLBACK_BUTTON14_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON15_PRODUCT], callback_data=CALLBACK_BUTTON15_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON16_PRODUCT], callback_data=CALLBACK_BUTTON16_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON17_PRODUCT], callback_data=CALLBACK_BUTTON17_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON18_PRODUCT], callback_data=CALLBACK_BUTTON18_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON19_PRODUCT], callback_data=CALLBACK_BUTTON19_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON20_PRODUCT], callback_data=CALLBACK_BUTTON20_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON21_PRODUCT], callback_data=CALLBACK_BUTTON21_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON22_PRODUCT], callback_data=CALLBACK_BUTTON22_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON23_PRODUCT], callback_data=CALLBACK_BUTTON23_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON24_PRODUCT], callback_data=CALLBACK_BUTTON24_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON25_PRODUCT], callback_data=CALLBACK_BUTTON25_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON26_PRODUCT], callback_data=CALLBACK_BUTTON26_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON27_PRODUCT], callback_data=CALLBACK_BUTTON27_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# @debug_requests
def keyboard_callback_handler(update: Update, context: CallbackContext):
    """ Обработчик ВСЕХ кнопок со ВСЕХ клавиатур
    """
    query = update.callback_query
    data = query.data
    now = datetime.datetime.now()

    # Обратите внимание: используется `effective_message`
    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text
    if data == CALLBACK_BUTTON1_LEFT:
        # "Удалим" клавиатуру у прошлого сообщения
        # (на самом деле отредактируем его так, что текст останется тот же, а клавиатура пропадёт)
        # query.edit_message_text(
        #     text=current_text,
        query.edit_message_text(
            text='*Для начала заказа укажи свой город 🏠*',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_towns(),
        )
    elif data == CALLBACK_BUTTON2_RIGHT:
        # Показать следующий экран клавиатуры
        # (оставить тот же текст, но указать другой массив кнопок)
        query.edit_message_text(
            text=current_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_products(),
        )

        # выслать новое сообщение
        # context.bot.send_message(
        #     chat_id=chat_id,
        #     text="Новое сообщение\n\ncallback_query.data={}".format(data),
        #     reply_markup=get_products(),
        # )

    # elif data == CALLBACK_BUTTON2_RIGHT:
    #     # Отредактируем текст сообщения, но оставим клавиатуру
    #     query.edit_message_text(
    #         text="Успешно отредактировано в {}".format(now),
    #         reply_markup=get_base_inline_keyboard(),
    #     )
    elif data == CALLBACK_BUTTON3_MORE:
        # Показать следующий экран клавиатуры
        # (оставить тот же текст, но указать другой массив кнопок)
        query.edit_message_text(
            text=current_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON4_BACK:
        # Показать предыдущий экран клавиатуры
        # (оставить тот же текст, но указать другой массив кнопок)
        query.edit_message_text(
            text="*Выбери город 🏠*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON5_TIME:
        # Покажем новый текст и оставим ту же клавиатуру
        text = "*Точное время*\n\n{}".format(now)
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_keyboard2(),
        )
    elif data in (CALLBACK_BUTTON9_TOWN, CALLBACK_BUTTON10_TOWN, CALLBACK_BUTTON11_TOWN, CALLBACK_BUTTON12_TOWN):
        pair = {
            CALLBACK_BUTTON9_TOWN: "Москва",
            CALLBACK_BUTTON10_TOWN: "Питер",
            CALLBACK_BUTTON11_TOWN: "Новосибирск",
            CALLBACK_BUTTON12_TOWN: "Екатеринбург",

        }[data]

        try:
            text = "*Твой город:*\n\n*➡ {}*\n\n*Теперь выбери округ*".format(pair)
        except ValueError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        if pair == "Москва":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_area(),
            )
        elif pair == "Питер":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_area(),
            )
        elif pair == "Новосибирск":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_novosibirsk_area(),
            )
        elif pair == "Екатеринбург":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_ekaterinburg_area(),
            )
    elif data in (Moscow.CALLBACK_BUTTON1_CAO, Moscow.CALLBACK_BUTTON2_NORTHERN, Moscow.CALLBACK_BUTTON3_NORTHEASTERN,
                  Moscow.CALLBACK_BUTTON4_EASTERN, Moscow.CALLBACK_BUTTON5_SOUTHEASTERN, Moscow.CALLBACK_BUTTON6_SOUTHERN,
                  Moscow.CALLBACK_BUTTON7_SOUTHWESTERN, Moscow.CALLBACK_BUTTON8_WESTERN, Moscow.CALLBACK_BUTTON9_NORTHWESTERN):
        pair = {
            Moscow.CALLBACK_BUTTON1_CAO: "ЦАО",
            Moscow.CALLBACK_BUTTON2_NORTHERN: "САО",
            Moscow.CALLBACK_BUTTON3_NORTHEASTERN: "СВАО",
            Moscow.CALLBACK_BUTTON4_EASTERN: "ВАО",
            Moscow.CALLBACK_BUTTON5_SOUTHEASTERN: "ЮВАО",
            Moscow.CALLBACK_BUTTON6_SOUTHERN: "ЮАО",
            Moscow.CALLBACK_BUTTON7_SOUTHWESTERN: "ЮЗАО",
            Moscow.CALLBACK_BUTTON8_WESTERN: "ЗАО",
            Moscow.CALLBACK_BUTTON9_NORTHWESTERN: "СЗАО",
        }[data]

        try:
            text = "*Твой округ:*\n\n*➡ {}*\n\n*Теперь выбери метро*".format(pair)
        except ValueError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        if pair == "ЦАО":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_metro_cao(),
            )
        elif pair == "САО":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_metro_northern(),
            )
        elif pair == "СВАО":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_metro_northeastern(),
            )
        elif pair == "ЮВАО":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_metro_southeastern(),
            )
        elif pair == "ВАО":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_metro_eastern(),
            )
        elif pair == "ЮАО":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_metro_southern(),
            )
        elif pair == "ЮЗАО":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_metro_southwestern(),
            )
        elif pair == "ЗАО":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_metro_western(),
            )
        elif pair == "СЗАО":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_moscow_metro_northwestern(),
            )
    elif data in (Piter.CALLBACK_BUTTON1_Admiralteyskiy, Piter.CALLBACK_BUTTON2_Vasileostrovsiy, Piter.CALLBACK_BUTTON3_Viborgskiy,
                  Piter.CALLBACK_BUTTON4_Kalininskiy, Piter.CALLBACK_BUTTON5_Kirovskiy, Piter.CALLBACK_BUTTON6_Krasnogvardeyskiy,
                  Piter.CALLBACK_BUTTON7_Kronshtadskiy, Piter.CALLBACK_BUTTON8_Moscowskiy, Piter.CALLBACK_BUTTON9_Nevskiy,
                  Piter.CALLBACK_BUTTON10_Petrogradskiy, Piter.CALLBACK_BUTTON11_Primorskiy, Piter.CALLBACK_BUTTON12_Pushkinskiy,
                  Piter.CALLBACK_BUTTON13_Frunzinskiy, Piter.CALLBACK_BUTTON14_Centralniy):
        pair = {
            Piter.CALLBACK_BUTTON1_Admiralteyskiy: "Адмиралтейский",
            Piter.CALLBACK_BUTTON2_Vasileostrovsiy: "Василеостровский",
            Piter.CALLBACK_BUTTON3_Viborgskiy: "Выборгский",
            Piter.CALLBACK_BUTTON4_Kalininskiy: "Калининский",
            Piter.CALLBACK_BUTTON5_Kirovskiy: "Кировский",
            Piter.CALLBACK_BUTTON6_Krasnogvardeyskiy: "Красногвардейский",
            Piter.CALLBACK_BUTTON7_Kronshtadskiy: "Кронштадский",
            Piter.CALLBACK_BUTTON8_Moscowskiy: "Московский",
            Piter.CALLBACK_BUTTON9_Nevskiy: "Невский",
            Piter.CALLBACK_BUTTON10_Petrogradskiy: "Петроградский",
            Piter.CALLBACK_BUTTON11_Primorskiy: "Приморский",
            Piter.CALLBACK_BUTTON12_Pushkinskiy: "Пушкинский",
            Piter.CALLBACK_BUTTON13_Frunzinskiy: "Фрунзенский",
            Piter.CALLBACK_BUTTON14_Centralniy: "Центральный",
        }[data]

        try:
            text = "*Твой округ:*\n\n*➡ {}*\n\n*Теперь выбери метро*".format(pair)
        except ValueError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        if pair == "Адмиралтейский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_admiralteyskiy(),
            )
        elif pair == "Василеостровский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_vasileostrovsiy(),
            )
        elif pair == "Выборгский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_viborgskiy(),
            )
        elif pair == "Калининский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_kalininskiy(),
            )
        elif pair == "Кировский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_kirovskiy(),
            )
        elif pair == "Красногвардейский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_krasnogvardeyskiy(),
            )
        elif pair == "Кронштадский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_kronshtadskiy(),
            )
        elif pair == "Московский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_moscowskiy(),
            )
        elif pair == "Невский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_nevskiy(),
            )
        elif pair == "Петроградский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_petrogradskiy(),
            )
        elif pair == "Приморский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_primorskiy(),
            )
        elif pair == "Пушкинский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_pushkinskiy(),
            )
        elif pair == "Фрунзенский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_frunzinskiy(),
            )
        elif pair == "Центральный":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_piter_metro_centralniy(),
            )
    elif data in (Novosibirsk.CALLBACK_BUTTON1_Dzerzhinsky, Novosibirsk.CALLBACK_BUTTON2_Zeleznodorozny, Novosibirsk.CALLBACK_BUTTON3_Zaelcovskiy,
                  Novosibirsk.CALLBACK_BUTTON4_Leninsky, Novosibirsk.CALLBACK_BUTTON5_Oktyabrsky, Novosibirsk.CALLBACK_BUTTON6_Pervomaysky,
                  ):
        pair = {
            Novosibirsk.CALLBACK_BUTTON1_Dzerzhinsky: "Дзержинский",
            Novosibirsk.CALLBACK_BUTTON2_Zeleznodorozny: "Железнодорожный",
            Novosibirsk.CALLBACK_BUTTON3_Zaelcovskiy: "Заельцовский",
            Novosibirsk.CALLBACK_BUTTON4_Leninsky: "Ленинский",
            Novosibirsk.CALLBACK_BUTTON5_Oktyabrsky: "Октябрьский",
            Novosibirsk.CALLBACK_BUTTON6_Pervomaysky: "Первомайский",
        }[data]

        try:
            text = "*Твой округ:*\n\n*➡ {}*\n\n*Теперь выбери метро*".format(pair)
        except ValueError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        if pair == "Дзержинский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_novosibirsk_metro_dzerzhinsky(),
            )
        elif pair == "Железнодорожный":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_novosibirsk_metro_zeleznodorozny(),
            )
        elif pair == "Заельцовский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_novosibirsk_metro_zaelcovskiy(),
            )
        elif pair == "Ленинский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_novosibirsk_metro_leninsky(),
            )
        elif pair == "Октябрьский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_novosibirsk_metro_oktyabrsky(),
            )
        elif pair == "Первомайский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_novosibirsk_metro_pervomaysky(),
            )
    elif data in (Ekaterinburg.CALLBACK_BUTTON1_VerhIsetskiy, Ekaterinburg.CALLBACK_BUTTON2_Zheleznodorozhniy, Ekaterinburg.CALLBACK_BUTTON3_Kirovskiy,
                  Ekaterinburg.CALLBACK_BUTTON4_Leninskiy, Ekaterinburg.CALLBACK_BUTTON5_Oktyabrskiy, Ekaterinburg.CALLBACK_BUTTON6_Ordzhonikidzevskiy,
                  Ekaterinburg.CALLBACK_BUTTON7_Chkalovskiy):
        pair = {
            Ekaterinburg.CALLBACK_BUTTON1_VerhIsetskiy: "Верх-Исетский",
            Ekaterinburg.CALLBACK_BUTTON2_Zheleznodorozhniy: "Железнодорожный",
            Ekaterinburg.CALLBACK_BUTTON3_Kirovskiy: "Кировский",
            Ekaterinburg.CALLBACK_BUTTON4_Leninskiy: "Ленинский",
            Ekaterinburg.CALLBACK_BUTTON5_Oktyabrskiy: "Октябрьский",
            Ekaterinburg.CALLBACK_BUTTON6_Ordzhonikidzevskiy: "Орджоникидзевский",
            Ekaterinburg.CALLBACK_BUTTON7_Chkalovskiy: "Чкаловский",
        }[data]

        try:
            text = "*Твой округ:*\n\n*➡ {}*\n\n*Теперь выбери район*".format(pair)
        except ValueError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        if pair == "Верх-Исетский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_ekaterinburg_metro_verhisetskiy(),
            )
        elif pair == "Железнодорожный":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_ekaterinburg_metro_zheleznodorozhniy(),
            )
        elif pair == "Кировский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_ekaterinburg_metro_kirovskiy(),
            )
        elif pair == "Ленинский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_ekaterinburg_metro_Leninskiy(),
            )
        elif pair == "Октябрьский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_ekaterinburg_metro_oktyabrskiy(),
            )
        elif pair == "Орджоникидзевский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_ekaterinburg_metro_ordzhonikidzevskiy(),
            )
        elif pair == "Чкаловский":
            query.edit_message_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_ekaterinburg_metro_chkalovskiy(),
            )
    elif data in (Moscow.CALLBACK_BUTTON_METRO_TAGANSKAYA, Moscow.CALLBACK_BUTTON_METRO_MAYAKOVSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_PEROVO, Moscow.CALLBACK_BUTTON_METRO_TVERSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_BAUMANSKAYA, Moscow.CALLBACK_BUTTON_METRO_LUBANKA,
                  Moscow.CALLBACK_BUTTON_METRO_PUSHKINSKAYA, Moscow.CALLBACK_BUTTON_METRO_MARKSITSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_PAVELECKAYA, Moscow.CALLBACK_BUTTON_METRO_KURSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_ARBATSKAYA, Moscow.CALLBACK_BUTTON_METRO_OHOTNIYRYAD,
                  Moscow.CALLBACK_BUTTON_METRO_KIEVSKAYA, Moscow.CALLBACK_BUTTON_METRO_FILI,
                  Moscow.CALLBACK_BUTTON_METRO_STUDENCHESKAYA, Moscow.CALLBACK_BUTTON_METRO_PIONERSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_KUTUZOVSKAYA, Moscow.CALLBACK_BUTTON_METRO_KRILATSKOE,
                  Moscow.CALLBACK_BUTTON_METRO_MOLODEZNAYA, Moscow.CALLBACK_BUTTON_METRO_AEROPORT,
                  Moscow.CALLBACK_BUTTON_METRO_BEGOVAYA, Moscow.CALLBACK_BUTTON_METRO_SOKOL,
                  Moscow.CALLBACK_BUTTON_METRO_DINAMO, Moscow.CALLBACK_BUTTON_METRO_TIMIRYAZEVSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_POLEZAEVSKAYA, Moscow.CALLBACK_BUTTON_METRO_VOYKOVSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_NOVOGIREEVO, Moscow.CALLBACK_BUTTON_METRO_SCHELKOVSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_IZMAYLOVSKAYA, Moscow.CALLBACK_BUTTON_METRO_VIHINO,
                  Moscow.CALLBACK_BUTTON_METRO_SOKOLNIKI, Moscow.CALLBACK_BUTTON_METRO_SEMENOVSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_VDNH, Moscow.CALLBACK_BUTTON_METRO_BABUSHKINSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_OTRADNOE, Moscow.CALLBACK_BUTTON_METRO_ALEKSEEVSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_ALTUFEVO, Moscow.CALLBACK_BUTTON_METRO_MEDVEDKOVO,
                  Moscow.CALLBACK_BUTTON_METRO_VLADIKINO, Moscow.CALLBACK_BUTTON_METRO_PLANERNAYA,
                  Moscow.CALLBACK_BUTTON_METRO_SHODNENSKAYA, Moscow.CALLBACK_BUTTON_METRO_TUSHINSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_SCHUKINSKAYA, Moscow.CALLBACK_BUTTON_METRO_AVIAMOTORNAYA,
                  Moscow.CALLBACK_BUTTON_METRO_TEKSTILSCHIKI, Moscow.CALLBACK_BUTTON_METRO_KUZMINKI,
                  Moscow.CALLBACK_BUTTON_METRO_RAZANSKIYPROSPECT, Moscow.CALLBACK_BUTTON_METRO_DUBROVKA,
                  Moscow.CALLBACK_BUTTON_METRO_PECHATNIKI, Moscow.CALLBACK_BUTTON_METRO_LUBLINO,
                  Moscow.CALLBACK_BUTTON_METRO_SHABOLOVSKAYA, Moscow.CALLBACK_BUTTON_METRO_AVTOZAVODSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_KASHIRSKAYA, Moscow.CALLBACK_BUTTON_METRO_UZNAYA,
                  Moscow.CALLBACK_BUTTON_METRO_NAGORNAYA, Moscow.CALLBACK_BUTTON_METRO_ANNINO,
                  Moscow.CALLBACK_BUTTON_METRO_DOMODEDOVSKAYA, Moscow.CALLBACK_BUTTON_METRO_LENINSKIY,
                  Moscow.CALLBACK_BUTTON_METRO_YASENEVO, Moscow.CALLBACK_BUTTON_METRO_AKADEMICHESKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_PROFSOUZNAYA, Moscow.CALLBACK_BUTTON_METRO_KAHOVSKAYA,
                  Moscow.CALLBACK_BUTTON_METRO_KALUZSKAYA, Moscow.CALLBACK_BUTTON_METRO_KONKOVO,

                  Piter.CALLBACK_BUTTON1_Admiralteyskiy, Piter.CALLBACK_BUTTON2_Vasileostrovsiy,
                  Piter.CALLBACK_BUTTON3_Viborgskiy, Piter.CALLBACK_BUTTON4_Kalininskiy,
                  Piter.CALLBACK_BUTTON5_Kirovskiy, Piter.CALLBACK_BUTTON6_Krasnogvardeyskiy,
                  Piter.CALLBACK_BUTTON7_Kronshtadskiy, Piter.CALLBACK_BUTTON8_Moscowskiy,
                  Piter.CALLBACK_BUTTON9_Nevskiy, Piter.CALLBACK_BUTTON10_Petrogradskiy,
                  Piter.CALLBACK_BUTTON11_Primorskiy, Piter.CALLBACK_BUTTON12_Pushkinskiy,
                  Piter.CALLBACK_BUTTON13_Frunzinskiy, Piter.CALLBACK_BUTTON14_Centralniy,
                  Piter.CALLBACK_BUTTON_METRO_ADMIRALTEYSKAYA, Piter.CALLBACK_BUTTON_METRO_SADOVAYA,
                  Piter.CALLBACK_BUTTON_METRO_ZVENIGORODSKAYA, Piter.CALLBACK_BUTTON_METRO_NEVSKIYPROSPECT,
                  Piter.CALLBACK_BUTTON_METRO_PRIMORSKAYA, Piter.CALLBACK_BUTTON_METRO_VASILEOSTROVSKAYA,
                  Piter.CALLBACK_BUTTON_METRO_GAVAN, Piter.CALLBACK_BUTTON_METRO_UDELNAYA,
                  Piter.CALLBACK_BUTTON_METRO_OZERKI, Piter.CALLBACK_BUTTON_METRO_PARNAS,
                  Piter.CALLBACK_BUTTON_METRO_VIBORGSKAYA, Piter.CALLBACK_BUTTON_METRO_LESNAYA,
                  Piter.CALLBACK_BUTTON_METRO_GRAJDANSKIYPROSPECT, Piter.CALLBACK_BUTTON_METRO_POLITEHNICHESKAYA,
                  Piter.CALLBACK_BUTTON_METRO_PLOSCHADMUJESTVA, Piter.CALLBACK_BUTTON_METRO_NARVSKAYA,
                  Piter.CALLBACK_BUTTON_METRO_AVTOVO, Piter.CALLBACK_BUTTON_METRO_NOVOCHERKASSKAYA,
                  Piter.CALLBACK_BUTTON_METRO_LADOJSKAYA, Piter.CALLBACK_BUTTON_METRO_KRESTOVSKIYOSTROV,
                  Piter.CALLBACK_BUTTON_METRO_STARAYADEREVNYA, Piter.CALLBACK_BUTTON_METRO_ELECTROSILA,
                  Piter.CALLBACK_BUTTON_METRO_ZVEZDNAYA, Piter.CALLBACK_BUTTON_METRO_KUPCHINO,
                  Piter.CALLBACK_BUTTON_METRO_ULICADIBENKO, Piter.CALLBACK_BUTTON_METRO_PROSPECTBOLSHEVIKOV,
                  Piter.CALLBACK_BUTTON_METRO_GORKOVSKAYA, Piter.CALLBACK_BUTTON_METRO_ZENIT,
                  Piter.CALLBACK_BUTTON_METRO_CHKALOVSKAYA, Piter.CALLBACK_BUTTON_METRO_CHERNAYARECHKA,
                  Piter.CALLBACK_BUTTON_METRO_PIONERSKAYA, Piter.CALLBACK_BUTTON_METRO_SHUSHARI,
                  Piter.CALLBACK_BUTTON_METRO_BUHARESTSKAYA, Piter.CALLBACK_BUTTON_METRO_PROSPECTSLAVI,
                  Piter.CALLBACK_BUTTON_METRO_CHERNISHEVSKAYA, Piter.CALLBACK_BUTTON_METRO_GOSTINIYDVOR,
                  Piter.CALLBACK_BUTTON_METRO_LIGOVSKIY,

                  Novosibirsk.CALLBACK_BUTTON_AREA_BEREZOVAYAROSCHA, Novosibirsk.CALLBACK_BUTTON_AREA_KAMENSKAYA,
                  Novosibirsk.CALLBACK_BUTTON_AREA_MARSHALAPOKRISHKINA, Novosibirsk.CALLBACK_BUTTON_AREA_NIKITSKAYA,
                  Novosibirsk.CALLBACK_BUTTON_AREA_OKTYABRSKAYA, Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADGARINAMIHAYLOVSKOGO,
                  Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADMARKSA, Novosibirsk.CALLBACK_BUTTON_AREA_STUDENCHESKAYA,
                  Novosibirsk.CALLBACK_BUTTON_AREA_ZAELCOVSKAYA, Novosibirsk.CALLBACK_BUTTON_AREA_ZOLOTAYANIVA,

                  CALLBACK_BUTTON22_METRO_SPASSKAYA, CALLBACK_BUTTON23_METRO_SADOVAYA, CALLBACK_BUTTON24_METRO_DOSTOEVSKAYA,
                  CALLBACK_BUTTON25_METRO_OKTYABRSKAYA, CALLBACK_BUTTON26_METRO_ZAELCOVSKAYA):
        pair = {
            Moscow.CALLBACK_BUTTON_METRO_TAGANSKAYA: "Таганская ",
            Moscow.CALLBACK_BUTTON_METRO_MAYAKOVSKAYA: "Маяковская ",
            Moscow.CALLBACK_BUTTON_METRO_TVERSKAYA: "Тверская ",
            Moscow.CALLBACK_BUTTON_METRO_BAUMANSKAYA: "Бауманская ",
            Moscow.CALLBACK_BUTTON_METRO_LUBANKA: "Лубянка ",
            Moscow.CALLBACK_BUTTON_METRO_PUSHKINSKAYA: "Пушкинская ",
            Moscow.CALLBACK_BUTTON_METRO_MARKSITSKAYA: "Маркситская ",
            Moscow.CALLBACK_BUTTON_METRO_PAVELECKAYA: "Павелецкая ",
            Moscow.CALLBACK_BUTTON_METRO_KURSKAYA: "Курская ",
            Moscow.CALLBACK_BUTTON_METRO_ARBATSKAYA: "Арбатская ",
            Moscow.CALLBACK_BUTTON_METRO_OHOTNIYRYAD: "Охотный ряд ",

            Moscow.CALLBACK_BUTTON_METRO_KIEVSKAYA: "Киевская",
            Moscow.CALLBACK_BUTTON_METRO_FILI: "Фили ",
            Moscow.CALLBACK_BUTTON_METRO_STUDENCHESKAYA: "Студенческая ",
            Moscow.CALLBACK_BUTTON_METRO_PIONERSKAYA: "Пионерская ",
            Moscow.CALLBACK_BUTTON_METRO_KUTUZOVSKAYA: "Кутузовская ",
            Moscow.CALLBACK_BUTTON_METRO_KRILATSKOE: "Крылатское ",
            Moscow.CALLBACK_BUTTON_METRO_MOLODEZNAYA: "Молодежная ",

            Moscow.CALLBACK_BUTTON_METRO_AEROPORT: "Аэропорт ",
            Moscow.CALLBACK_BUTTON_METRO_BEGOVAYA: "Беговая ",
            Moscow.CALLBACK_BUTTON_METRO_SOKOL: "Сокол ",
            Moscow.CALLBACK_BUTTON_METRO_DINAMO: "Динамо ",
            Moscow.CALLBACK_BUTTON_METRO_TIMIRYAZEVSKAYA: "Тимирязевская ",
            Moscow.CALLBACK_BUTTON_METRO_POLEZAEVSKAYA: "Полежаевская ",
            Moscow.CALLBACK_BUTTON_METRO_VOYKOVSKAYA: "Войковская",

            Moscow.CALLBACK_BUTTON_METRO_NOVOGIREEVO: "Новогиреево ",
            Moscow.CALLBACK_BUTTON_METRO_PEROVO: "Перово ",
            Moscow.CALLBACK_BUTTON_METRO_SCHELKOVSKAYA: "Щелковская ",
            Moscow.CALLBACK_BUTTON_METRO_IZMAYLOVSKAYA: "Измайловская ",
            Moscow.CALLBACK_BUTTON_METRO_VIHINO: "Выхино ",
            Moscow.CALLBACK_BUTTON_METRO_SOKOLNIKI: "Сокольники ",
            Moscow.CALLBACK_BUTTON_METRO_SEMENOVSKAYA: "Семеновская ",

            Moscow.CALLBACK_BUTTON_METRO_VDNH: "ВДНХ ",
            Moscow.CALLBACK_BUTTON_METRO_BABUSHKINSKAYA: "Бабушкинская ",
            Moscow.CALLBACK_BUTTON_METRO_OTRADNOE: "Отрадное ",
            Moscow.CALLBACK_BUTTON_METRO_ALEKSEEVSKAYA: "Алексеевская ",
            Moscow.CALLBACK_BUTTON_METRO_ALTUFEVO: "Алтуфьево ",
            Moscow.CALLBACK_BUTTON_METRO_MEDVEDKOVO: "Медведково ",
            Moscow.CALLBACK_BUTTON_METRO_VLADIKINO: "Владыкино ",

            Moscow.CALLBACK_BUTTON_METRO_PLANERNAYA: "Планерная ",
            Moscow.CALLBACK_BUTTON_METRO_SHODNENSKAYA: "Сходненская ",
            Moscow.CALLBACK_BUTTON_METRO_TUSHINSKAYA: "Тушинская ",
            Moscow.CALLBACK_BUTTON_METRO_SCHUKINSKAYA: "Щукинская ",

            Moscow.CALLBACK_BUTTON_METRO_AVIAMOTORNAYA: "Авиамоторная ",
            Moscow.CALLBACK_BUTTON_METRO_TEKSTILSCHIKI: "Текстильщики ",
            Moscow.CALLBACK_BUTTON_METRO_KUZMINKI: "Кузьминки ",
            Moscow.CALLBACK_BUTTON_METRO_RAZANSKIYPROSPECT: "Рязанский проспект ",
            Moscow.CALLBACK_BUTTON_METRO_DUBROVKA: "Дубровка ",
            Moscow.CALLBACK_BUTTON_METRO_PECHATNIKI: "Печатники ",
            Moscow.CALLBACK_BUTTON_METRO_LUBLINO: "Люблино ",

            Moscow.CALLBACK_BUTTON_METRO_SHABOLOVSKAYA: "Шаболовская ",
            Moscow.CALLBACK_BUTTON_METRO_AVTOZAVODSKAYA: "Автозаводская ",
            Moscow.CALLBACK_BUTTON_METRO_KASHIRSKAYA: "Каширская ",
            Moscow.CALLBACK_BUTTON_METRO_UZNAYA: "Южная ",
            Moscow.CALLBACK_BUTTON_METRO_NAGORNAYA: "Нагорная ",
            Moscow.CALLBACK_BUTTON_METRO_ANNINO: "Аннино ",
            Moscow.CALLBACK_BUTTON_METRO_DOMODEDOVSKAYA: "Домодедовская ",

            Moscow.CALLBACK_BUTTON_METRO_LENINSKIY: "Ленинский проспект ",
            Moscow.CALLBACK_BUTTON_METRO_YASENEVO: "Ясенево ",
            Moscow.CALLBACK_BUTTON_METRO_AKADEMICHESKAYA: "Академическая ",
            Moscow.CALLBACK_BUTTON_METRO_PROFSOUZNAYA: "Профсоюзная ",
            Moscow.CALLBACK_BUTTON_METRO_KAHOVSKAYA: "Каховская ",
            Moscow.CALLBACK_BUTTON_METRO_KALUZSKAYA: "Калужская ",
            Moscow.CALLBACK_BUTTON_METRO_KONKOVO: "Коньково ",

            Piter.CALLBACK_BUTTON_METRO_ADMIRALTEYSKAYA: "Адмиралтейская ",
            Piter.CALLBACK_BUTTON_METRO_SADOVAYA: "Садовая ",
            Piter.CALLBACK_BUTTON_METRO_ZVENIGORODSKAYA: "Звенигородская ",
            Piter.CALLBACK_BUTTON_METRO_NEVSKIYPROSPECT: "Невский проспект ",
            Piter.CALLBACK_BUTTON_METRO_PRIMORSKAYA: "Приморская ",
            Piter.CALLBACK_BUTTON_METRO_VASILEOSTROVSKAYA: "Василеостровская ",
            Piter.CALLBACK_BUTTON_METRO_GAVAN: "Гавань ",
            Piter.CALLBACK_BUTTON_METRO_UDELNAYA: "Удельная ",
            Piter.CALLBACK_BUTTON_METRO_OZERKI: "Озерки ",
            Piter.CALLBACK_BUTTON_METRO_PARNAS: "Парнас ",
            Piter.CALLBACK_BUTTON_METRO_VIBORGSKAYA: "Выборгская ",
            Piter.CALLBACK_BUTTON_METRO_LESNAYA: "Лесная ",
            Piter.CALLBACK_BUTTON_METRO_GRAJDANSKIYPROSPECT: "Гражданский проспект ",
            Piter.CALLBACK_BUTTON_METRO_POLITEHNICHESKAYA: "Политехническая ",
            Piter.CALLBACK_BUTTON_METRO_PLOSCHADMUJESTVA: "Площадь Мужества ",
            Piter.CALLBACK_BUTTON_METRO_NARVSKAYA: "Нарвская ",
            Piter.CALLBACK_BUTTON_METRO_AVTOVO: "Автово ",
            Piter.CALLBACK_BUTTON_METRO_NOVOCHERKASSKAYA: "Новочеркасская ",
            Piter.CALLBACK_BUTTON_METRO_LADOJSKAYA: "Ладожская ",
            Piter.CALLBACK_BUTTON_METRO_KRESTOVSKIYOSTROV: "Крестовский остров ",
            Piter.CALLBACK_BUTTON_METRO_STARAYADEREVNYA: "Старая Деревня ",
            Piter.CALLBACK_BUTTON_METRO_ELECTROSILA: "Электросила ",
            Piter.CALLBACK_BUTTON_METRO_ZVEZDNAYA: "Звездная ",
            Piter.CALLBACK_BUTTON_METRO_KUPCHINO: "Купчино ",
            Piter.CALLBACK_BUTTON_METRO_ULICADIBENKO: "Улица Дыбенко ",
            Piter.CALLBACK_BUTTON_METRO_PROSPECTBOLSHEVIKOV: "Проспект Большевиков ",
            Piter.CALLBACK_BUTTON_METRO_GORKOVSKAYA: "Горковская ",
            Piter.CALLBACK_BUTTON_METRO_ZENIT: "Зенит ",
            Piter.CALLBACK_BUTTON_METRO_CHKALOVSKAYA: "Чкаловская ",
            Piter.CALLBACK_BUTTON_METRO_CHERNAYARECHKA: "Черная Речка ",
            Piter.CALLBACK_BUTTON_METRO_PIONERSKAYA: "Пионерская ",
            Piter.CALLBACK_BUTTON_METRO_SHUSHARI: "Шушари ",
            Piter.CALLBACK_BUTTON_METRO_BUHARESTSKAYA: "Бухарестская ",
            Piter.CALLBACK_BUTTON_METRO_PROSPECTSLAVI: "Проспект Славы ",
            Piter.CALLBACK_BUTTON_METRO_CHERNISHEVSKAYA: "Чернышевская ",
            Piter.CALLBACK_BUTTON_METRO_GOSTINIYDVOR: "Гостинный Двор ",
            Piter.CALLBACK_BUTTON_METRO_LIGOVSKIY: "Лиговский ",

            Novosibirsk.CALLBACK_BUTTON_AREA_STUDENCHESKAYA: "Студенческая",
            Novosibirsk.CALLBACK_BUTTON_AREA_KAMENSKAYA: "Каменская",
            Novosibirsk.CALLBACK_BUTTON_AREA_BEREZOVAYAROSCHA: "Березовая Роща",
            Novosibirsk.CALLBACK_BUTTON_AREA_MARSHALAPOKRISHKINA: "Маршала Покрышкина",
            Novosibirsk.CALLBACK_BUTTON_AREA_ZAELCOVSKAYA: "Заельцовская",
            Novosibirsk.CALLBACK_BUTTON_AREA_NIKITSKAYA: "Никитская",
            Novosibirsk.CALLBACK_BUTTON_AREA_ZOLOTAYANIVA: "Золотая Нива",
            Novosibirsk.CALLBACK_BUTTON_AREA_OKTYABRSKAYA: "Октябрьская",
            Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADMARKSA: "Площадь Маркса",
            Novosibirsk.CALLBACK_BUTTON_AREA_PLOSCHADGARINAMIHAYLOVSKOGO: "Площадь Гарина Михайловского",

            CALLBACK_BUTTON22_METRO_SPASSKAYA: "Спасская ",
            CALLBACK_BUTTON23_METRO_SADOVAYA: "Садовая ",
            CALLBACK_BUTTON24_METRO_DOSTOEVSKAYA: "Достоевская ",
            CALLBACK_BUTTON25_METRO_OKTYABRSKAYA: "Октябрьская ",
            CALLBACK_BUTTON26_METRO_ZAELCOVSKAYA: "Заельцовская ",
        }[data]

        try:
            text = "*Твое метро:*\n\n*➡ {}*\n\n*Теперь выбери товар*".format(pair)
        except ValueError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_products(),
        )
    elif data in (Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHIROKAYARECHKA,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORAKHRUSTALNAYA,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LISTVENNIY, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PEREGON,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SVETLAYARECHKA, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VIZ,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ZARECHNIY, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VOKZALNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORNOZAVODSKIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PALKINO,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEMKLYUCHEI,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_STARAYASORTIROVKA,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NOVAYASORTIROVKA,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SORTIROVOCHNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTUZGORODOK, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_IZOPLIT,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KALINOVSKIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMSOMOLSKIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PIONERSKIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_CENTRALNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHARTASH,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUGOZAPADNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSKOVSKAYAGORKA, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UNC,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_AKADEMICHESKIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOLTSOVO,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMPRESSORNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MALYIISTOK,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PARKOVIY, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SIBIRSKIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SINIEKAMNI, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GLUBOKOE,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSTOVKA, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LECHEBNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PTICEFABRIKA,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEVERNIYPROMYSHLENNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_URALMASH, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELMASH,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOZLOVSKIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_APPARATNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YAGODNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_BOTANICHESKIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTORCHERMET, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELIZAVET,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NIZHNEISETSKIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_RUDNIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UKTUSSKIY, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHIMMASH,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUZHNIY, Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PRIISKOVIY,
                  Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHUTOR):
        pair = {
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHIROKAYARECHKA: "Широкая Речка",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORAKHRUSTALNAYA: "Гора Хрустальная",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LISTVENNIY: "Лиственный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PEREGON: "Перегон",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SVETLAYARECHKA: "Светлая Речка",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_AKADEMICHESKIY: "Академический",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VIZ: "ВИЗ",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ZARECHNIY: "Заречный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VOKZALNIY: "Вокзальный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GORNOZAVODSKIY: "Горнозаводский",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PALKINO: "Палкино",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEMKLYUCHEI: "Семь Ключей",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_STARAYASORTIROVKA: "Старая Сортировка",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NOVAYASORTIROVKA: "Новая Сортировка",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SEVERNIYPROMYSHLENNIY: "Северный Промышленный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SORTIROVOCHNIY: "Сортировочный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTUZGORODOK: "Втузгородок",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_IZOPLIT: "Изоплит",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KALINOVSKIY: "Калиновский",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMSOMOLSKIY: "Комсомольский",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PIONERSKIY: "Пионерский",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_CENTRALNIY: "Центральный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SHARTASH: "Шарташ",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUGOZAPADNIY: "Югозападный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSKOVSKAYAGORKA: "Московская горка",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UNC: "УНЦ",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOLTSOVO: "Кольцово",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOMPRESSORNIY: "Компрессорный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MALYIISTOK: "Малый Исток",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PARKOVIY: "Парковый",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SIBIRSKIY: "Сибирский",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_SINIEKAMNI: "Синие Камни",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_GLUBOKOE: "Глубокое",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_MOSTOVKA: "Мостовка",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_LECHEBNIY: "Лечебный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PTICEFABRIKA: "Птицефабрика",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_URALMASH: "Уралмаш",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELMASH: "Елмаш",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KOZLOVSKIY: "Козловский",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_APPARATNIY: "Аппаратный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YAGODNIY: "Ягодный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_BOTANICHESKIY: "Ботанический",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_VTORCHERMET: "Вторчермет",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_ELIZAVET: "Елизавет",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_NIZHNEISETSKIY: "Нижне-Исетский",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_RUDNIY: "Рудный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_UKTUSSKIY: "Уктусский",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHIMMASH: "Химмаш",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_YUZHNIY: "Южный",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_PRIISKOVIY: "Приисковый",
            Ekaterinburg.CALLBACK_BUTTON_MICRORAYON_KHUTOR: "Хутор",
        }[data]

        try:
            text = "*Твой район:*\n\n*➡ {}*\n\n*Теперь выбери товар*".format(pair)
        except ValueError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_products(),
        )
    elif data in (CALLBACK_BUTTON12_PRODUCT, CALLBACK_BUTTON13_PRODUCT, CALLBACK_BUTTON14_PRODUCT,
                  CALLBACK_BUTTON15_PRODUCT, CALLBACK_BUTTON16_PRODUCT, CALLBACK_BUTTON17_PRODUCT,
                  CALLBACK_BUTTON18_PRODUCT, CALLBACK_BUTTON19_PRODUCT, CALLBACK_BUTTON20_PRODUCT,
                  CALLBACK_BUTTON21_PRODUCT, CALLBACK_BUTTON22_PRODUCT, CALLBACK_BUTTON23_PRODUCT,
                  CALLBACK_BUTTON24_PRODUCT, CALLBACK_BUTTON25_PRODUCT, CALLBACK_BUTTON26_PRODUCT,
                  CALLBACK_BUTTON27_PRODUCT):
        pair = {
            CALLBACK_BUTTON12_PRODUCT: "❄Меф кристалл VHQ 1г 1500❄",
            CALLBACK_BUTTON13_PRODUCT: "❄Меф кристалл VHQ 2г 2700❄",
            CALLBACK_BUTTON14_PRODUCT: "❄Меф кристалл VHQ 5г 6000❄",
            CALLBACK_BUTTON15_PRODUCT: "⚡Альфа - PVP 1г 1700⚡",
            CALLBACK_BUTTON16_PRODUCT: "⚡Альфа - PVP 2г 3000⚡",
            CALLBACK_BUTTON17_PRODUCT: "🏃Амфетамин HQ 1г 1220🏃",
            CALLBACK_BUTTON18_PRODUCT: "🏃Амфетамин HQ 2г 2100🏃",
            CALLBACK_BUTTON19_PRODUCT: "💎MDMA кристаллы VHQ 1г 2500💎",
            CALLBACK_BUTTON20_PRODUCT: "💎MDMA кристаллы VHQ 2г 4200💎",
            CALLBACK_BUTTON21_PRODUCT: "🍬Ecstasy Marvel Superheroes 2шт 1750🍬",
            CALLBACK_BUTTON22_PRODUCT: "🍫Гашиш BlackRock Hash 1г 1550🍫",
            CALLBACK_BUTTON23_PRODUCT: "🍫Гашиш BlackRock Hash 2г 2430🍫",
            CALLBACK_BUTTON24_PRODUCT: "🎄Шишки OG KUSH 1г 1500🎄",
            CALLBACK_BUTTON25_PRODUCT: "🎄Шишки OG KUSH 2г 2200🎄",
            CALLBACK_BUTTON26_PRODUCT: "🎄Шишки Crystal Haze 1г 1650🎄",
            CALLBACK_BUTTON27_PRODUCT: "🎄Шишки Crystal Haze 2г 2300🎄",
        }[data]
        try:
            text = "*Твой товар:*\n\n*➡ {}*\n\n*Теперь выбери способ оплаты*".format(pair)
        except ValueError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_keyboard2(),
        )
    elif data in (CALLBACK_BUTTON6_PRICE, CALLBACK_BUTTON7_PRICE, CALLBACK_BUTTON8_PRICE):
        pair = {
            CALLBACK_BUTTON6_PRICE: "USD-BTC",
            CALLBACK_BUTTON7_PRICE: "USD-LTC",
            CALLBACK_BUTTON8_PRICE: "USD-ETH",
        }[data]
        type_of_payment = {
            CALLBACK_BUTTON6_PRICE: 'BTC-кошелек: 1QJuPgPmfRVBJRwhBAfXmwHGepNNR7XfYW',
            CALLBACK_BUTTON7_PRICE: 'LCT-кошелек: LZjeR4umv5tz33bB4finjjFXpevjsqorB2',
            CALLBACK_BUTTON8_PRICE: 'ETH-кошелек: 0xec67b7ee2864375c8cbad989f1eb8108b1bfaff8',
        }[data]
        method_of_payment = {
            CALLBACK_BUTTON6_PRICE: 'Bitcoin',
            CALLBACK_BUTTON7_PRICE: 'Litecoin',
            CALLBACK_BUTTON8_PRICE: 'Etherium',
        }[data]
        try:
            current_price = client.get_last_price(pair=pair)
            lookfor = r'[0-9]{4}'
            result = re.findall(lookfor, current_text)
            calculation = int(result[0])/(current_price * 75)
            # text = "*Курс валюты:*\n\n*{}* = {}$".format(pair, current_price)
            order_number = random.randint(9998, 9999999)

            text = "Заказ *#{}* сформирован ⚡\n\n" \
                   "Ты выбрал метод оплаты: *{}*\n" \
                   "Текущий актуальный курс: *{}* 💲\n\n" \
                   "Пришли *{}* на\n\n*{}*\n\n" \
                   "После того, как совершил платеж, напиши номер кошелька, с которого производилась" \
                   " оплата в сообщении ниже👇 и нажми кнопку *\"Платеж отправлен 🚀\"* \n" \
                   "После того, как транзакция будет подтверждена мы пришлем тебе координаты точки ⏰\n" \
                .format(order_number, method_of_payment, current_price, calculation, type_of_payment)

        except BittrexError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_payments(),
        )
    elif data == CALLBACK_BUTTON9_PRICE:
        type_of_payment = {
            CALLBACK_BUTTON9_PRICE: 'QIWI-кошелек: 31232173981273918(проба)',
        }[data]
        method_of_payment = {
            CALLBACK_BUTTON9_PRICE: 'QIWI',
        }[data]
        order_number = random.randint(9998, 9999999)

        lookfor = r'[0-9]{4}'
        result = re.findall(lookfor, current_text)

        text = "Заказ *#{}* сформирован ⚡\n\n" \
               "Ты выбрал метод оплаты: *{}*\n" \
               "Пришли *{} ₽* на\n*{}*\n\n" \
               "После того, как совершил платеж, напиши номер кошелька, с которого производилась" \
               " оплата в сообщении ниже👇 и нажми кнопку *\"Платеж отправлен 🚀\"* \n" \
               "После того, как транзакция будет подтверждена мы пришлем тебе координаты точки ⏰\n" \
            .format(order_number, method_of_payment, result[0], type_of_payment)
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_payments(),
        )

    elif data == CALLBACK_BUTTON18_SEND:
        text = "*🍀 Проверяем наличие транзакции...*\n*Чутка подожди...*"
        context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardRemove(),
        )
    elif data == CALLBACK_BUTTON_HIDE_KEYBOARD:
        # Спрятать клавиатуру
        # Работает только при отправке нового сообщение
        # Можно было бы отредактировать, но тогда нужно точно знать что у сообщения не было кнопок
        context.bot.send_message(
            chat_id=chat_id,
            text="Спрятали клавиатуру\n\nНажмите /start чтобы вернуть её обратно",
            reply_markup=ReplyKeyboardRemove(),
        )


# @debug_requests
# def do_start(update: Update, context: CallbackContext):
#     update.message.reply_text(
#         text="Привет! Отправь мне что-нибудь",
#         reply_markup=get_base_reply_keyboard(),
#     )
# @debug_requests
def do_start(update: Update, context: CallbackContext):
    # функция для текста \start (не забываем подключить handler и dispatcher
    update.message.reply_text(
        text='Привет, *дорогой друг*! 🙋\n'
             'Рады видеть тебя в *Rick & Morty\'s candy shop*. Мы  поможем тебе хорошо провести время 💫 \n\n'
             '*Почему выбирают нас* 👇\n'
             '✅Самый качественный стафф✅\n'
             '✅Доступные цены✅\n'
             '✅Оперативность✅\n'
             '✅Удобство✅\n'
             '✅Поддержка 24/7✅\n'
             '🎁❗Не забывай про еженедельный конкурс, в котором участвуют ВСЕ❗🎁\n',

        # text='Привет, *дорогой друг*! 🙋\n'
        #      'Ты залетел в магазин *волшебства*, '
        #      'мы поможем тебе хорошо провести время 💫\n'
        #      'Для начала закупа напиши слово: *погнали*\n',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_base_reply_keyboard(),
    )

# @debug_requests
def do_help(update: Update, context: CallbackContext):
    text_help = "*📜Правила покупок в магазине:*\n\n"\
                "*🚩ВАЖНО!*\n\n"\
                "*🚫Запрещено дробить платежи*\n\n"\
                "*♻Если у тебя возникли проблемы с заказом, вопросы по оплате, " \
                "работе магазина - обращайся сюда*👉 @support"
    update.message.reply_text(
        text=text_help,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_base_inline_keyboard(),
    )
    do_forward(update=update, context=context)

def do_forward(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='*Чтобы выйти на главное меню, нажми* \"🔙Назад\"',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_forward_reply_keyboard(),
    )

# @debug_requests
def do_town(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='*Выбери свой город ✨*',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_base_inline_keyboard(),
    )
    do_forward(update=update, context=context)


# @debug_requests
def do_payment(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='BTC-кошелек: *1QJuPgPmfRVBJRwhBAfXmwHGepNNR7XfYW*\n'
             'ETH-кошелек: *0xec67b7ee2864375c8cbad989f1eb8108b1bfaff8*\n'
             'LCT-кошелек: *LZjeR4umv5tz33bB4finjjFXpevjsqorB2*\n\n',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_base_inline_keyboard(),
    )
    do_forward(update=update, context=context)

# @debug_requests
def do_products(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='🎁 *Список товаров в наличии:*\n\n- *Фен*\n- *МДМА*\n- *ДМА*\n- *Грибы*\n- *ЛСД*\n- *Мефедрон*\n\n\n'
             '*Для начала заказа укажи свой город 🏠*',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_base_inline_keyboard(),
    )
    do_forward(update=update, context=context)

def do_contest(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Каждую неделю мы разыгрываем *50000₽*.\n'
             'Для участия в конкурсе необходимо в течение недели *сделать 1 покупку* и '
             'совершить оплату с *BTC кошелька*. '
             'Ввести кошелек в окно после совершения оплаты и '
             'он автоматически будет зарегистрирован в конкурсе.\n\n\n'
             '*Для начала заказа укажи свой город 🏠*',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_base_inline_keyboard(),
    )
    do_forward(update=update, context=context)

# @debug_requests
# def do_time(update: Update, context: CallbackContext):
#     """ Узнать серверное время
#         Работает только на Unix-системах!
#     """
#     process = Popen(["date"], stdout=PIPE)
#     text, error = process.communicate()
#     # Может произойти ошибка вызова процесса (код возврата не 0)
#     if error:
#         text = "Произошла ошибка, время неизвестно"
#     else:
#         # Декодировать ответ команды из процесса
#         text = text.decode("utf-8")
#     update.message.reply_text(
#         text=text,
#         reply_markup=get_base_inline_keyboard(),
#     )


# @debug_requests
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    if text == BUTTON1_HELP:
        return do_help(update=update, context=context)
    elif text == BUTTON2_PRODUCTS:
        return do_products(update=update, context=context)
    elif text == BUTTON3_TOWN:
        return do_town(update=update, context=context)
    elif text == BUTTON4_PAYMENT:
        return do_payment(update=update, context=context)
    elif text == BUTTON5_FORWARD:
        return do_start(update=update, context=context)
    elif text == BUTTON6_CONTEST:
        return do_contest(update=update, context=context)
    else:
        if len(text) <= 10:
            reply_text = '*Выбери свой город ✨*'
            # "Ваш ID = {}\n\n{}".format(chat_id, text)
            update.message.reply_text(
                text=reply_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_base_inline_keyboard(),
            )

def main():
    logger.info("Запускаем бота...")

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token=config.BOT_TOKEN,
        request=req, )
    #     base_url=config.TG_API_URL,
    # )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info(f'Bot info: {info}')

    # Навесить обработчики команд
    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    products_handler = CommandHandler("products", do_products)
    town_handler = CommandHandler("town", do_town)
    payment_handler = CommandHandler("payment", do_payment)
    message_handler = MessageHandler(Filters.text, do_echo)
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(products_handler)
    updater.dispatcher.add_handler(town_handler)
    updater.dispatcher.add_handler(payment_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(buttons_handler)

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()

    logger.info("Закончили...")


if __name__ == '__main__':
    main()
