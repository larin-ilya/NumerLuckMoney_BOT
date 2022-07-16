#БОТ ДЛЯ ПОДСЧЕТА ДЕНЕЖНОГО ЧИСЛА

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor 
import re, time
 

storage = MemoryStorage()
TOKEN = "напишите ваш токен сюда"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


#функция проверки на цифры
async def check_int_return(message):
    try:
        int(message.text) 
        return True
    except ValueError:
        return False


@dp.message_handler(content_types=["video"])
async def video_file_id(message: types.Message):
    await bot.send_message(message.from_user.id, "Ваше id video")
    await message.answer(message.video.file_id)

###машина состояний:
class Вопросы(StatesGroup):
    спросили_день = State()
    спросили_месяц = State()
    спросили_год = State()



#[HELP]
@dp.message_handler(commands=['help'], state=None)
async def хэлп(message: types.Message):
     await message.answer(" и н ф о р м а ц и я ")
     await bot.send_video (chat_id=message.from_user.id, video='BAACAgIAAxkBAAIGDmLS7wN3s9b65OAiVfOOu06hMMr-AALgGwACmxCYSqYz2od5fnvPKQQ') #BAACAgIAAxkBAAIC32LSSDuh512WSCIoV9JhCSoZ1kg7AAK1GAACXoSYSigZEbz17Nb ID ФАЙЛА
     await message.answer("мужик расказывает как происходит расчет денежного кода")
    #старт и первый вопрос:
@dp.message_handler(commands=['start'])
async def proces_vopros1(message: types.Message):
    await message.answer("БОТ ДЛЯ ПОДСЧЕТА ДЕНЕЖНОГО ЧИСЛА ")
    await message.answer(" По дате рождения. ")
    await message.answer("  ВВЕДИТЕ ДЕНЬ:")
    await Вопросы.спросили_день.set()

@dp.message_handler(state=Вопросы.спросили_день)
async def процес_вопрос2(message: types.Message, state: FSMContext):
     if re.match(r"^[0-9]+$", message.text): #проверка на числовое значение

         await state.update_data(День=message.text)
         await message.answer("Отлично! Теперь ВВЕДИТЕ МЕСЯЦ (цифрами)")
         await Вопросы.next() #  
     else:
                return await message.reply("нужно написать цифрами, попробуйте еще раз;"), await message.answer("ВВЕДИТЕ ДЕНЬ (цифрами):")
                    

@dp.message_handler(state=Вопросы.спросили_месяц)
async def процес_вопрос3(message: types.Message, state: FSMContext):
    if re.match(r"^[0-9]+$", message.text): #проверка на числовое значение
        await state.update_data(Месяц=message.text)
        await message.answer("Отлично! Теперь ВВЕДИТЕ ГОД")
        await Вопросы.next() #  
    else:
                return await message.reply("нужно написать цифрами, попробуйте еще раз;"), await message.answer("ВВЕДИТЕ МЕСЯЦ (цифрами):")

@dp.message_handler(state=Вопросы.спросили_год)
async def процес_завершение(message: types.Message, state: FSMContext):
    if re.match(r"^[0-9]+$", message.text): #проверка на числовое значение
        await state.update_data(Год=message.text)
        data = await state.get_data()
        await message.answer(f"день: {data['День']}\n"
                             f"месяц: {data['Месяц']}\n"
                             f"год: {data['Год']}")
    else:
                return await message.reply("нужно написать цифрами, попробуйте еще раз;"), await message.answer("ВВЕДИТЕ ГОД (цифрами):")
    print(f" {data['День']}.{data['Месяц']}.{data['Год']}")
    den= int(data['День'])
    mesyac= int(data['Месяц'])

    god= int(data['Год'])
    #делаем списки из чисел дат:
    строка_из_числа = str(den)
    список_из_дня = []
    for digit in строка_из_числа:
        список_из_дня.append (int(digit))     #список_из_дня = [(den//(10**i))%10 for i in range(math.ceil(math.log(den, 10))-1, -1, -1)]
    
    строка_из_числа = str(mesyac)
    список_из_месяца = []
    for digit in строка_из_числа:
        список_из_месяца.append (int(digit))    #список_из_месяца = [(mesyac//(10**i))%10 for i in range(math.ceil(math.log(mesyac, 10))-1, -1, -1)]
    
    строка_из_числа = str(god)
    список_из_года = []
    for digit in строка_из_числа:
        список_из_года.append (int(digit))      #список_из_года = [(god//(10**i))%10 for i in range(math.ceil(math.log(god, 10))-1, -1, -1)]

    #заменяем девятки на нули с помощью математическ.библиотеки:
    for i, n in enumerate(список_из_дня):
        if n == 9:
            список_из_дня[i] = 0

    for i, n in enumerate(список_из_месяца):
        if n == 9:
            список_из_месяца[i] = 0

    for i, n in enumerate(список_из_года):
        if n == 9:
            список_из_года[i] = 0

            """
    #выводим списки:
    print(список_из_дня)
    print(список_из_месяца)
    print(список_из_года)
    """

    #складываем числа из списков
    сумма_чисел_из_дня = sum(список_из_дня)
    сумма_чисел_из_месяца = sum(список_из_месяца)
    сумма_чисел_из_года = sum(список_из_года)

    """
    #выводим суммы чисел:
    print(сумма_чисел_из_дня)
    print(сумма_чисел_из_месяца)
    print(сумма_чисел_из_года)
    """
    #делаем список_из_суммы_чисел_из_года, т.к. там двузначные числа-и получаем сумму_из_списка_из_суммы_чисел_из_года:
    строка_из_числа = str(сумма_чисел_из_года)
    список_из_суммы_чисел_из_года = []
    for digit in строка_из_числа:
        список_из_суммы_чисел_из_года.append (int(digit))
    #список_из_суммы_чисел_из_года = [(сумма_чисел_из_года//(10**i))%10 for i in range(math.ceil(math.log(сумма_чисел_из_года, 10))-1, -1, -1)]
    сумма_из_списка_из_суммы_чисел_из_года = sum(список_из_суммы_чисел_из_года)

    """
    #выводим суммы чисел:
    print(сумма_чисел_из_дня)
    print(сумма_чисел_из_месяца)
    print(сумма_из_списка_из_суммы_чисел_из_года)
    """
    #складываем все суммы чисел:
    сумма_всех_сумм_чисел = сумма_чисел_из_дня + сумма_чисел_из_месяца + сумма_из_списка_из_суммы_чисел_из_года
    #делаем список из сумма_всех_сумм_чисел для того чтоб потом его сложить:

    строка_из_числа = str(сумма_всех_сумм_чисел)
    список_из_суммы_всех_сумм_чисел = []
    for digit in строка_из_числа:
        список_из_суммы_всех_сумм_чисел.append (int(digit))
    #список_из_суммы_всех_сумм_чисел = [(сумма_всех_сумм_чисел//(10**i))%10 for i in range(math.ceil(math.log(сумма_всех_сумм_чисел, 10))-1, -1, -1)]
    полная_сумма_всех_сумм_чисел = sum(список_из_суммы_всех_сумм_чисел)
    

    #создаем строку из сумм чисел,потом форматируем и делаем из нее число:
    результат= (сумма_чисел_из_дня,сумма_чисел_из_месяца,сумма_из_списка_из_суммы_чисел_из_года,полная_сумма_всех_сумм_чисел)
    result1 = " ".join(map(str, результат))
    result2 = result1.replace(' ', '')
    result = int(result2)
    #result-это результат вычислений в виде числа.

    await message.answer("...СЧИТАЕМ ЧИСЛО...")
    time.sleep(2.5)
    await message.answer("ВАШЕ ДЕНЕЖНОЕ ЧИСЛО:")
    await message.answer(result)
    print(result)
    print('_________________')
    await state.finish()
@dp.message_handler()
async def process_help_command(message: types.Message):
    await message.reply("Неправильно .")
    await message.answer (" попробуй /start или /help .")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
inp = input()