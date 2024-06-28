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
    back = State()
    info = State()
    info_1 = State()
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
    await message.answer(text=LEXICON['main_menu'], reply_markup=create_inline_kb(1, 'book_service', '/price', 'promotions_2', 'contacts'))    

# Этот хэндлер будет срабатывать на команду "/price"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='price'))
async def process_price_command(message: Message):
    await message.answer(text=LEXICON['price_list'], reply_markup=create_inline_kb(1, 'back'))  

# Этот хэндлер будет срабатывать на команду "/promotions"
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
    await callback_query.message.edit_text(text=LEXICON['price_list'], reply_markup=create_inline_kb(1, 'Маникюр', 'Педикюр', 'Комплекс', 'back'))
    await state.set_state(BookingState.service)
        

@router.callback_query(StateFilter(BookingState.service))
async def m_list(callback_query: CallbackQuery, state: FSMContext): 
    if callback_query.data == 'back':
                # Возвращаемся к BookingState.service, сохраняя информацию 
        await state.update_data(service='back')
        await state.set_state(BookingState.service)
        # Возвращаемся к BookingState.service
        await callback_query.message.edit_text(text=LEXICON['main_menu'], reply_markup=create_inline_kb(1, 'book_service', '/price', 'promotions_2', 'contacts'))
        return  
    await state.update_data(service=callback_query.data) 
    await callback_query.message.edit_text(text=LEXICON['m_text'], reply_markup=create_inline_kb(1, 'Снятие гель-лака', 'Без снятия', 'back'))
    await state.set_state(BookingState.info)


@router.callback_query(StateFilter(BookingState.info))
async def yes_list(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'back':
                # Возвращаемся к BookingState.service, сохраняя информацию 
        await state.update_data(service='back')
        await state.set_state(BookingState.service)
        # Возвращаемся к BookingState.service
        await callback_query.message.edit_text(text=LEXICON['main_menu'], reply_markup=create_inline_kb(1, 'book_service', '/price', 'promotions_2', 'contacts'))
        return 
    await state.update_data(info=callback_query.data)
    await callback_query.message.edit_text(text=LEXICON['m_text_2'], reply_markup=create_inline_kb(1, 'Покрытие', 'Без покрытия', 'back'))
    await state.set_state(BookingState.info_1)


@router.callback_query(StateFilter(BookingState.info_1))
async def yes_list(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'back':
                # Возвращаемся к BookingState.service, сохраняя информацию 
        await state.update_data(service='back')
        await state.set_state(BookingState.service)
        # Возвращаемся к BookingState.service
        await callback_query.message.edit_text(text=LEXICON['main_menu'], reply_markup=create_inline_kb(1, 'book_service', '/price', 'promotions_2', 'contacts'))
        return 
    await state.update_data(info_1=callback_query.data)
    await callback_query.message.edit_text(text=LEXICON['m_text_3'], reply_markup=create_inline_kb(1, 'Мастер маникюря и педикюра_1', 'Мастер маникюря и педикюра_2', 'back'))
    await state.set_state(BookingState.master)    


@router.callback_query(StateFilter(BookingState.master))
async def choose_master(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'back':
                # Возвращаемся к BookingState.service, сохраняя информацию 
        await state.update_data(service='back')
        await state.set_state(BookingState.service)
        # Возвращаемся к BookingState.service
        await callback_query.message.edit_text(text=LEXICON['main_menu'], reply_markup=create_inline_kb(1, 'book_service', '/price', 'promotions_2', 'contacts'))
        return 
    await state.update_data(master=callback_query.data)
    await callback_query.message.edit_text("📅Выберите дату удобную дла Вас:", reply_markup=await SimpleCalendar(locale=await get_user_locale(callback_query.from_user)).start_calendar())
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
    info = user_data['info']
    info_1 = user_data['info_1']
    master = user_data['master']
    date = user_data['date']
    time = callback_query.data.split('_')[1]
    await callback_query.message.answer(f"Спасибо!👍 Вы записаны на услуги: \n{info}\n {info_1}\n {service}\n {master}\n на {date} в {time}.{LEXICON['finish']}")
    await state.clear()  


@router.callback_query(lambda c: c.data == '/price')
async def price_list(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['price_list'], reply_markup=create_inline_kb(1, 'back'))


@router.callback_query(lambda c: c.data == 'promotions_2')
async def promotions(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['promotions_1'], reply_markup=create_inline_kb(1, 'back'))


@router.callback_query(lambda c: c.data == 'back')
async def back(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=LEXICON['main_menu'], reply_markup=create_inline_kb(1, 'book_service', '/price', 'promotions_2', 'contacts'))    


@router.callback_query(lambda c: c.data == 'contacts')
async def contacts(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Контакты:", reply_markup=create_inline_kb(1, 'phone', 'address', 'website', 'instagram', 'back'))



#router.callback_query(lambda c: c.data in ['phone', 'address', 'website', 'instagram'])
#async def contact_info(callback_query: CallbackQuery):
#    info = {
#        'phone': "Телефон салона: +7 123 456 7890",
#        'address': "Адрес салона: ул. Примерная, д. 1",
#        'website': "Сайт: http://example.com",
#        'instagram': "Instagram: https://instagram.com/example"
#    }
#   await callback_query.message.answer(info[callback_query.data])
