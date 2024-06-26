from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON

# Создание клавиатур:
#def main_menu_keyboard():
#    buttons = [
#        [InlineKeyboardButton(text="Запись на услугу", callback_data="book_service")],
#        [InlineKeyboardButton(text="Прайс-лист", callback_data="price_list")],
#        [InlineKeyboardButton(text="Акции", callback_data="promotions")],
#        [InlineKeyboardButton(text="Контакты", callback_data="contacts")]
#    ]
#    return InlineKeyboardMarkup(inline_keyboard=buttons)

#def service_selection_keyboard():
#    buttons = [
#        [InlineKeyboardButton(text="Услуга 1", callback_data="service_1")],
#        [InlineKeyboardButton(text="Услуга 2", callback_data="service_2")],
#        [InlineKeyboardButton(text=LEXICON['back'], callback_data="main_menu")]
#    ]
#    return InlineKeyboardMarkup(inline_keyboard=buttons)

#def master_selection_keyboard():
#   buttons = [
#        [InlineKeyboardButton(text="Мастер 1", callback_data="master_1")],
#        [InlineKeyboardButton(text="Мастер 2", callback_data="master_2")],
#        [InlineKeyboardButton(text=LEXICON['back'], callback_data="book_service")]
#    ]
#    return InlineKeyboardMarkup(inline_keyboard=buttons)

#def time_selection_keyboard():
#    buttons = [
#        [InlineKeyboardButton(text="Время 2", callback_data="time_2")],
#        [InlineKeyboardButton(text=LEXICON['back'], callback_data="book_service")]
#    ]
#    return InlineKeyboardMarkup(inline_keyboard=buttons)

#def price_list_keyboard():
#    buttons = [
#        [InlineKeyboardButton(text=LEXICON['back'], callback_data="main_menu")]
#    ]
#    return InlineKeyboardMarkup(inline_keyboard=buttons)

#def promotions_keyboard():
#    buttons = [
#        [InlineKeyboardButton(text=LEXICON['back'], callback_data="main_menu")]
#    ]
#    return InlineKeyboardMarkup(inline_keyboard=buttons)
def time_selection_keyboard():
    buttons = [
        [InlineKeyboardButton(text="10:00", callback_data="time_10:00")],
        [InlineKeyboardButton(text="14:00", callback_data="time_14:00")],
        [InlineKeyboardButton(text="Назад", callback_data="choose_master")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def contacts_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Телефон салона", callback_data="phone")],
        [InlineKeyboardButton(text="Адрес салона", callback_data="address")],
        [InlineKeyboardButton(text="Сайт", callback_data="website")],
        [InlineKeyboardButton(text="Instagram", callback_data="instagram")],
        [InlineKeyboardButton(text=LEXICON['back'], callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Функция для генерации инлайн-клавиатур "на лету"
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            # Проверяем наличие слова в словаре
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()