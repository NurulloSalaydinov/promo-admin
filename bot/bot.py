import logging

from utils.config import BOT_TOKEN
from utils.utils import RegisterForm, PromocodeForm, CartForm
from aiogram.dispatcher import FSMContext
from utils.buttons import contact_btn, promocode_btn, start_btn, info_btn, cart_btn

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types


# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

from utils.resource import load_client, register_client, send_code, load_products, order_product


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id = message['from'].id
    res = load_client(user_id)
    try:
        if res['status'] != 104:
            if int(res['client']['telegram_id']) == user_id:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add(promocode_btn)
                markup.add(info_btn)
                markup.add(cart_btn)
                await message.reply(f"Salom {res['client']['first_name']} 👋\nSizning to'plagan balingiz ⭐️{res['client']['points']}", reply_markup=markup)
            else:
                await message.reply("Sizda biror narsa nato'gri ketgan iltimos @NurulloSalaydinov yoki +998888330116 ga Xabar bering !")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add(contact_btn)
            await RegisterForm.phone.set()
            await message.reply("Assalomu alaykum 👋\nMen Binokor kompaniyasining yordamchi botiman!\nRo'yhatdan o'tish uchun telefon raqamingizni ulashing !", reply_markup=markup)
    except Exception as e:
        print(e, '40 qator bot.py')
        await message.reply("Server hozircha ishlamayapti, keyinroq qayta urinib ko'ring !")


@dp.message_handler(lambda message: message.text == "📔Promokod jo'natish")
async def promocode(message: types.Message):
    user_id = message['from'].id
    res = load_client(user_id)
    try:
        print(res['status'])
        if res['status'] != 104:
            if int(res['client']['telegram_id']) == user_id:
                markup = types.ReplyKeyboardRemove()
                await PromocodeForm.code.set()
                await message.reply(f"Yaxshi menga promokodni yuboring.", reply_markup=markup)
            else:
                await message.reply("Sizda biror narsa nato'gri ketgan iltimos @NurulloSalaydinov yoki +998888330116 ga Xabar bering !")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add(contact_btn)
            await RegisterForm.phone.set()
            await message.reply("Siz ro'yhatdan o'tmagansiz, Iltimos ro'yhatdan o'tish uchun telefon raqamingizni ulashing !", reply_markup=markup)
    except Exception as e:
        print(e)
        await message.reply("Server hozircha ishlamayapti, keyinroq qayta urinib ko'ring !")

# Mening balim
@dp.message_handler(lambda message: message.text == "⭐️ Mening balim")
async def promocode(message: types.Message):
    user_id = message['from'].id
    res = load_client(user_id)
    try:
        if res['status'] != 104:
            if int(res['client']['telegram_id']) == user_id:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                markup.add(promocode_btn)
                markup.add(info_btn)
                markup.add(cart_btn)
                await message.reply(f"Profil {res['client']['first_name']}{res['client']['phone']}\nSizning to'plagan balingiz ⭐️{res['client']['points']}", reply_markup=markup)
            else:
                await message.reply("Sizda biror narsa nato'gri ketgan iltimos @NurulloSalaydinov yoki +998888330116 ga Xabar bering !")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add(contact_btn)
            await RegisterForm.phone.set()
            await message.reply("Siz ro'yhatdan o'tmagansiz, Iltimos ro'yhatdan o'tish uchun telefon raqamingizni ulashing !", reply_markup=markup)
    except Exception as e:
        print(e)
        await message.reply("Server hozircha ishlamayapti, keyinroq qayta urinib ko'ring !")

# Harid
@dp.message_handler(lambda message: message.text == "🛒 Sovg'alar")
async def promocode(message: types.Message):
    user_id = message['from'].id
    res = load_client(user_id)
    try:
        if res['status'] != 104:
            if int(res['client']['telegram_id']) == user_id:
                res_p = load_products()
                products = res_p['products']
                markup = types.InlineKeyboardMarkup(row_width=1)
                for product in products:
                    markup.insert(types.InlineKeyboardButton(f"{product['title']} - ⭐️{product['req_points']}", callback_data=f"{product['id']}"))
                await message.reply(f"🎁 Hozirda mavjud bo'lgan sovg'alar\n Buyurtma berish uchun pastdan sovg'ani tanlang!", reply_markup=markup)
            else:
                await message.reply("Sizda biror narsa nato'gri ketgan iltimos @NurulloSalaydinov yoki +998888330116 ga Xabar bering !")
        else:
            res_p = load_products()
            products = res_p['products']
            markup = types.InlineKeyboardMarkup(row_width=1)
            msg = ""
            for product in products:
                msg += f"\n{product['title']} - ⭐️{product['req_points']}"
            await message.reply(f"🎁 Hozirda mavjud bo'lgan sovg'alar {msg}\n❗️Siz hali ro'yhatdan o'tmagansiz ro'yhatdan o'tish uchun /start", reply_markup=markup)
    except Exception as e:
        print(e)
        await message.reply("Server hozircha ishlamayapti, keyinroq qayta urinib ko'ring !")


@dp.message_handler(state=RegisterForm.phone, content_types=[types.ContentType.CONTACT])
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
        username = message['from'].username
        res = register_client(message, username)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        if res['status'] == 101:
            markup.add(promocode_btn)
            markup.add(info_btn)
            markup.add(cart_btn)
            await message.reply("🎉 Siz ro'yhatdan muvaffaqqiyatli o'tdingiz!", reply_markup=markup)
            await state.finish()
        elif res['status'] == 100:
            markup.add(promocode_btn)
            markup.add(info_btn)
            markup.add(cart_btn)
            await message.reply("Siz ro'yhatdan allaqachon o'tgansiz!", reply_markup=markup)
            await state.finish()
        else:
            markup.add(start_btn)
            await message.reply("Hatolik yuz berdi, iltimos keyinroq qayta urinib koring 🤖", reply_markup=markup)


@dp.message_handler(state=PromocodeForm.code)
async def process_promocode(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['code'] = message.text
        res = send_code(message.text, message['from'].id)
        if res['status'] == 102:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add(promocode_btn)
            markup.add(info_btn)
            markup.add(cart_btn)
            await message.reply(f"Promokod muvaffaqiyatli tasdiqlandi !\nHozirgi balingiz ⭐️{res['points']}", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add(promocode_btn)
            markup.add(info_btn)
            markup.add(cart_btn)
            await message.reply("Promokod natog'ri tasdiqlanmadi 😕\nPromokodingizni qayta tekshirib ko'ring 😉", reply_markup=markup)
    await state.finish()


@dp.callback_query_handler()
async def receive_callback(call: types.CallbackQuery):
    # print(call)
    # print(call.data)
    res = order_product(call.data, call.from_user.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if res['status'] == 102:
        markup.add(promocode_btn)
        markup.add(info_btn)
        markup.add(cart_btn)
        msg = f"{res['product']['title']} ni yaxshi kunlarda ishlating 🙌\n🥳🎁 Sovg'a muvaffaqiyatli yuborildi tez orada siz bilan aloqaga chiqamiz 😉"
    elif res['status'] == 103:
        msg = f"Sizda bal yetarli emas 😐\nBal to'plash uchun promokodlarni yuboring 😉"
        markup.add(promocode_btn)
        markup.add(info_btn)
        markup.add(cart_btn)
    elif res['status'] == 108:
        msg = f"Siz hali ro'yhatdan o'tmagansiz iltimos ro'yhatdan o'ting !"
        markup.add(contact_btn)
    await bot.send_message(call.from_user.id, msg, reply_markup=markup)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
