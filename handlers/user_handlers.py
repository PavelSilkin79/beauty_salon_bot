from datetime import datetime, timedelta
from aiogram import Router
from aiogram.types import  CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters.state import StateFilter
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, \
    get_user_locale
from lexicon.lexicon import LEXICON
from keyboards.keyboards import create_inline_kb, time_selection_keyboard
from database.database import users_db


router = Router()

# Создание состояний
class BookingState(StatesGroup):
    service = State()
    master = State()
    data = State()
    time = State()

@router.message(CommandStart(), StateFilter(default_state))
async def send_welcome(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username

    # Добавляем данные пользователа в словпарь
    users_db[user_id] = {'user_name': user_name}
    await message.answer(text=LEXICON['/start'], reply_markup=create_inline_kb(1, 'main_menu'))

# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=f'{LEXICON['/help']}')

# Этот хэндлер будет срабатывать на команду "/sign_up"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='sign_up'))
async def process_sign_up_command(message: Message):
    await message.answer(text=LEXICON['price_list'], reply_markup=create_inline_kb(1, 'M', 'P', 'K', 'back'))    

# Этот хэндлер будет срабатывать на команду "/price"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='price'))
async def process_price_command(message: Message):
    await message.answer(text=LEXICON['price_list'], reply_markup=create_inline_kb(1, 'M', 'P', 'K', 'back'))  

# Этот хэндлер будет срабатывать на команду "/price"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='promotions'))
async def process_promotions_command(message: Message):
    await message.answer(text=LEXICON['promotions_1'], reply_markup=create_inline_kb(1, 'back'))  

# Этот хэндлер будет срабатывать на команду "/contacts"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='contacts'))
async def process_promotions_command(message: Message):
    await message.answer(text=LEXICON['contacts'], reply_markup=create_inline_kb(1, 'phone', 'address', 'website', 'instagram'))       

@router.callback_query(lambda c: c.data == 'main_menu')
async def main_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['main_menu'], reply_markup=create_inline_kb(1, 'book_service', '/price', 'promotions_2', 'contacts'))

@router.callback_query(lambda c: c.data == 'book_service')
async def book_service(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text=LEXICON['price_list'], reply_markup=create_inline_kb(1, 'M', 'P', 'K', 'back'))
    await state.set_state(BookingState.service)

@router.callback_query(StateFilter(BookingState.service))
async def choose_service(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(service=callback_query.data)
    await callback_query.message.edit_text("Выберите мастера:", reply_markup=create_inline_kb(1, 'master_1', 'master_2'))
    await state.set_state(BookingState.master)

@router.callback_query(StateFilter(BookingState.master))
async def choose_master(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(master=callback_query.data)
    await callback_query.message.answer("📅Выберите дату удобную дла Вас:", reply_markup=await SimpleCalendar(locale=await get_user_locale(callback_query.from_user)).start_calendar())
    await state.set_state(BookingState.data)

@router.callback_query(SimpleCalendarCallback.filter(), StateFilter(BookingState.data))
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(locale=await get_user_locale(callback_query.from_user), show_alerts=True)
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date=date.strftime('%d/%m/%Y'))
        await callback_query.message.answer(f"Вы выбрали {date.strftime('%d/%m/%Y')}. Теперь выберите время:", reply_markup=time_selection_keyboard())
        await state.set_state(BookingState.time)

@router.callback_query( StateFilter(BookingState.time)) # Обработчик выбора времени
async def choose_time(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(time=callback_query.data)
        # Получите данные записи из user_data
    user_data = await state.get_data()
    service = user_data['service']
    master = user_data['master']
    date = user_data['date']
    time = callback_query.data.split('_')[1]
    await callback_query.message.answer(f"Вы записаны на {service} к {master} на {date} в {time}.")
    await state.clear()  

@router.callback_query(lambda c: c.data == '/price')
async def price_list(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['price_list'], reply_markup=create_inline_kb(1, 'M', 'P', 'K', 'back'))

@router.callback_query(lambda c: c.data == 'M')
async def price_list(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['m_text'], reply_markup=create_inline_kb(1, 'YES', 'NO', 'back'))

@router.callback_query(lambda c: c.data == 'P')
async def price_list(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['price_list'], reply_markup=create_inline_kb(1, 'M', 'P', 'K', 'back')) 

@router.callback_query(lambda c: c.data == 'K')
async def price_list(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['price_list'], reply_markup=create_inline_kb(1, 'M', 'P', 'K', 'back'))       


@router.callback_query(lambda c: c.data == 'promotions_2')
async def promotions(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['promotions_1'], reply_markup=create_inline_kb(1, 'back'))

@router.callback_query(lambda c: c.data == 'back')
async def promotions(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['main_menu'], reply_markup=create_inline_kb(1, 'book_service', '/price', 'promotions_2', 'contacts'))    

@router.callback_query(lambda c: c.data == 'contacts')
async def contacts(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Контакты:", reply_markup=create_inline_kb(1, 'phone', 'address', 'website', 'instagram'))

@router.callback_query(lambda c: c.data == 'contacts')
async def contacts(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Контакты:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Телефон салона", callback_data="phone")],
        [InlineKeyboardButton(text="Адрес салона", callback_data="address")],
        [InlineKeyboardButton(text="Сайт", callback_data="website")],
        [InlineKeyboardButton(text="Instagram", callback_data="instagram")],
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")]
    ]))

#router.callback_query(lambda c: c.data in ['phone', 'address', 'website', 'instagram'])
#async def contact_info(callback_query: CallbackQuery):
#    info = {
#        'phone': "Телефон салона: +7 123 456 7890",
#        'address': "Адрес салона: ул. Примерная, д. 1",
#        'website': "Сайт: http://example.com",
#        'instagram': "Instagram: https://instagram.com/example"
#    }
#   await callback_query.message.answer(info[callback_query.data])
