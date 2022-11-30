import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from Token import get_telegram_token
import model as m


# запись лога в csv файл
def log(update: Update, context: CallbackContext):
    file = open('db.csv', 'a')
    file.write(f'{update.effective_user.first_name},{update.effective_user.id}, {update.message.text}\n')
    file.close()


# обработка команды help
def help_command(update: Update, context: CallbackContext):
    log(update, context)
    update.message.reply_text(f"Привет, {update.effective_user.first_name}!"
                              "\nЯ бот-калькулятор, приятно познакомиться.\n"
                              "\nЯ умею производить простейшие арифметические операции с целыми, рациональными и "
                              "комплексными числами. \n "
                              "\nЖми на /start для запуска меню и выбирай тип калькулятора. \n"
                              "\nДальше просто следуй моим инструкциям. \n")


# калькулятор для работы с целыми числами
def calculator_int(update: Update, context: CallbackContext):
    log(update, context)
    msg = update.message.text
    print(msg)

    items = msg.split()
    x = int(items[1])
    act = items[2]
    y = int(items[3])
    m.init(x, y, act)
    update.message.reply_text(f'{x}{act}{y} = {m.do_it()}')


# калькулятор для работы с рациональными числами
def calculator_rat(update: Update, context: CallbackContext):
    log(update, context)
    msg = update.message.text
    print(msg)

    items = msg.split()
    x = float(items[1])
    act = items[2]
    y = float(items[3])
    m.init(x, y, act)
    update.message.reply_text(f'{x}{act}{y} = {m.do_it()}')


# калькулятор для работы с комплексными числами
def calculator_complex(update: Update, context: CallbackContext):
    log(update, context)
    msg = update.message.text
    print(msg)

    items = msg.split()
    x = complex(items[1])
    act = items[2]
    y = complex(items[3])
    m.init(x, y, act)
    update.message.reply_text(f'{x}{act}{y} = {m.do_it()}')


updater = Updater(get_telegram_token())


# обработка команды старт, Inline клавиатура
def start_command(update: Update, context: CallbackContext):
    button_a = telegram.InlineKeyboardButton('help, I need somebody', callback_data='button_a')
    button_b = telegram.InlineKeyboardButton('калькулятор целых чисел', callback_data='button_b')
    button_c = telegram.InlineKeyboardButton('калькулятор рациональных чисел', callback_data='button_c')
    button_d = telegram.InlineKeyboardButton('калькулятор комплексных чисел', callback_data='button_d')
    markup = telegram.InlineKeyboardMarkup(inline_keyboard=[[button_a], [button_b], [button_c], [button_d]])

    update.message.reply_text(f'Привет, {update.effective_user.first_name}.\n'
                              f'Нажми на нужную кнопку для начала работы',
                              reply_markup=markup)
    return callback


# обработка нажатия клавиш клавиатуры
def callback(update: Update, context: CallbackContext):
    query = update.callback_query
    variant = query.data
    if variant == 'button_a':
        query.answer()
        query.edit_message_text(text='Хочешь узнать, что я умею? Жми на /help')

    if variant == 'button_b':
        query.answer()
        query.edit_message_text(text='Чтобы калькулятор целых чисел работал верно,'
                                     'введи /calcI операнд X символ операции операнд Y. \nНапример: /calcI 2 + 2'
                                     '\nОперацию выдели пробелом с двух сторон')

    if variant == 'button_c':
        query.answer()
        query.edit_message_text(text='Чтобы калькулятор рациональных чисел работал верно,'
                                     'введи /calcR операнд X символ операции операнд Y. \nНапример: /calcR 3.5 + 1.5'
                                     '\nОперацию выдели пробелом с двух сторон')

    if variant == 'button_d':
        query.answer()
        query.edit_message_text(text='Чтобы калькулятор комплексных чисел работал верно,'
                                     'введи /calcC операнд X символ операции операнд Y. \nНапример: /calcC (4+1j) + ('
                                     '5+3j) '
                                     '\nКомлексные числа записывай в скобках и без пробелов.'
                                     '\nОперацию выдели пробелом с двух сторон')


updater.dispatcher.add_handler(CommandHandler('help', help_command))
updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(CommandHandler('calcI', calculator_int))
updater.dispatcher.add_handler(CommandHandler('calcC', calculator_complex))
updater.dispatcher.add_handler(CommandHandler('calcR', calculator_rat))
updater.dispatcher.add_handler(CallbackQueryHandler(callback=callback, pattern=None, run_async=False)
                               )

print('To cancel Ctr + C')
updater.start_polling()
updater.idle()
