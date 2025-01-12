import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import matplotlib.pyplot as plt
import io

# Токен вашого бота
API_TOKEN = "7760885159:AAF4j1St-sY774wvaMV_o0vIXMW-qU460yg"

bot = telebot.TeleBot(API_TOKEN)


# Словник для збереження даних користувачів
user_data = {}
import matplotlib.pyplot as plt
import io

# Функція для створення графіку з додаванням загальної суми
def create_report(chat_id):
    if "prices" in user_data[chat_id] and user_data[chat_id]["prices"]:
        # Дані для графіка (ціни акаунтів та час продажу)
        prices = [price for account, price, time in user_data[chat_id]["prices"]]
        times = [time for account, price, time in user_data[chat_id]["prices"]]

        # Обчислення загальної суми
        total_sum = sum(prices)

        # Створення графіку
        plt.figure(figsize=(10, 6))
        plt.plot(times, prices, marker='o', linestyle='-', color='b')
        plt.title(f'Продажі акаунтів (Загальна сума: ${total_sum:.2f})')
        plt.xlabel('Час')
        plt.ylabel('Ціна ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Збереження графіку в буфер
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Відправка графіку
        bot.send_photo(chat_id, buf)
        plt.close()  # Закриваємо графік, щоб не було пам'яті

    else:
        bot.send_message(chat_id, "У вас немає записів про продаж акаунтів для створення виписки.", reply_markup=finances_menu())

# Головне меню
def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Акаунти📁"), KeyboardButton("Фінанси💰"))
    return keyboard

# Меню фінансів
def finances_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Установить ціну💵"), KeyboardButton("Купили акк💸"))
    keyboard.add(KeyboardButton("Создать виписку📊"))
    keyboard.add(KeyboardButton("Назад↩️"))
    return keyboard

# Меню для установки ціни акаунту
def set_price_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Назад↩️"))
    return keyboard

# Меню для кнопки "Купили акк"
def bought_account_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    return keyboard


# Показ акаунтів та фінансів
def show_finances(chat_id):
    if "prices" not in user_data[chat_id]:
        user_data[chat_id]["prices"] = []   
    text = "💸Список продажу акаунтів:\n\n"
    if user_data[chat_id]["prices"]:
        text += "\n\n".join([f"💵Ціна: {price} $ (📆{time})" for account, price, time in user_data[chat_id]["prices"]])
    else:
        text += "😭Ви ще не встановили ціни на акаунти."
    # Видалення старого повідомлення, якщо воно існує
    if user_data[chat_id]["messages"]:
        try:
            # Якщо повідомлення існує, видаляємо його
            bot.delete_message(chat_id, user_data[chat_id]["messages"][0])
        except telebot.apihelper.ApiTelegramException:
            pass  # Якщо повідомлення вже видалене, нічого не робимо
    # Відправлення нового повідомлення і збереження його ID
    msg = bot.send_message(chat_id, text, reply_markup=finances_menu())
    user_data[chat_id]["messages"] = [msg.message_id]  # Зберігаємо ID нового повідомлення

# Встановлення ціни акаунту
def set_price(message):
    chat_id = message.chat.id
    price = message.text

    # Перевірка на "Назад"
    if price.lower() == "назад↩️":
        bot.send_message(chat_id, "↩️Повернення в меню фінансів.", reply_markup=finances_menu())
        return

    try:
        # Перевірка чи введено число
        price = float(price)
        user_data[chat_id]["price"] = price
        bot.send_message(chat_id, f"Ціна акаунту встановлена: {price} $. Тепер натисніть 'Купили акк' після продажу акаунту.", reply_markup=finances_menu())
    except ValueError:
        bot.send_message(chat_id, "Будь ласка, введіть правильну ціну (число в $).", reply_markup=set_price_menu())
        bot.register_next_step_handler(message, set_price)


# Кнопка "Купили акк"
def bought_account(message):
    chat_id = message.chat.id
    if "price" in user_data[chat_id]:
        price = user_data[chat_id]["price"]
        # Додаємо акаунт з ціною та часом покупки
        user_data[chat_id]["prices"].append((f"Аккаунт {len(user_data[chat_id]['prices']) + 1}", price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Видалення старого повідомлення про продаж акаунту
        if user_data[chat_id].get("last_sale_message_id"):
            try:
                bot.delete_message(chat_id, user_data[chat_id]["last_sale_message_id"])  # Видаляємо старе повідомлення
            except telebot.apihelper.ApiTelegramException:
                pass  # Якщо повідомлення вже видалене, ігноруємо помилку

        # Відправка нового повідомлення про продаж акаунту
        msg = bot.send_message(chat_id, f"💲Ви продали акаунт за *{price}* $. \nОсь список всіх акаунтів і їх цін:", reply_markup=finances_menu(), parse_mode='Markdown')
        user_data[chat_id]["last_sale_message_id"] = msg.message_id  # Зберігаємо ID нового повідомлення

        # Відправка списку акаунтів і їх цін
        show_finances(chat_id)
    else:
        bot.send_message(chat_id, "Будь ласка, спочатку встановіть ціну для акаунту.", reply_markup=finances_menu())
  

# Меню акаунтів
def accounts_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Назад↩️"), KeyboardButton("Добавить акаунт➕"), KeyboardButton("Удалить акаунт⛔"))
    return keyboard

# Меню для додавання акаунту
def add_account_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Відмінити❌"))
    return keyboard

# Меню для видалення акаунту
def delete_account_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Назад↩️"), KeyboardButton("Видалити всі акаунти🗑️"))
    return keyboard

# Меню підтвердження видалення всіх акаунтів
def confirm_delete_all_accounts_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Підтвердити ✅"), KeyboardButton("Відмінити ❌"))
    return keyboard

# Показ акаунтів
def show_accounts(chat_id):
    accounts = user_data[chat_id]["accounts"]
    
    if accounts:
        text = "Ваші акаунти:\n\n" + "\n\n".join(f"{i+1}. {account}" for i, account in enumerate(accounts))
    else:
        text = "😭Ви поки що не добавили акаунти."

    # Перевіряємо чи повідомлення ще не було видалене або неактивне
    if user_data[chat_id]["messages"]:
        try:
            # Якщо повідомлення існує, редагуємо його
            bot.edit_message_text(text, chat_id, user_data[chat_id]["messages"][0], reply_markup=accounts_menu())
        except telebot.apihelper.ApiTelegramException:
            # Якщо не вдалося редагувати (повідомлення видалене), відправляємо нове повідомлення
            msg = bot.send_message(chat_id, text, reply_markup=accounts_menu())
            user_data[chat_id]["messages"] = [msg.message_id]
    else:
        # Якщо повідомлення ще не було надіслано, надсилаємо його і зберігаємо ID
        msg = bot.send_message(chat_id, text, reply_markup=accounts_menu())
        user_data[chat_id]["messages"].append(msg.message_id)

# Додавання нового акаунту
def add_account(message):
    chat_id = message.chat.id
    account_data = message.text  # Дані, введені користувачем

    # Перевіряємо, чи не була натиснута кнопка "Відмінити"
    if account_data.lower() == "відмінити❌":
        user_data[chat_id]["adding_account"] = False  # Скасовуємо статус додавання акаунту
        bot.send_message(chat_id, "Додавання акаунту скасовано.↩️", reply_markup=accounts_menu())
        show_accounts(chat_id)
        return

    # Перевіряємо, чи ми вже в процесі додавання акаунту
    if user_data[chat_id]["adding_account"]:
        # Зберігаємо акаунт
        user_data[chat_id]["accounts"].append(account_data)

        # Оновлюємо список акаунтів
        show_accounts(chat_id)

        # Тепер просто чекаємо наступного вводу акаунту
        msg = bot.send_message(chat_id, "*Акаунт додано!✅* \nЩоб вийти натисніть 'Відмінити❌'", reply_markup=add_account_menu(), parse_mode='Markdown')
        bot.register_next_step_handler(msg, add_account)

# Видалення акаунту
def delete_account(message):
    chat_id = message.chat.id
    accounts = user_data[chat_id]["accounts"]

    # Якщо натискається кнопка "Назад", відправляємо користувача в головне меню
    if message.text == "Назад↩️":
        bot.send_message(chat_id, "Виберіть розділ:", reply_markup=accounts_menu())
        return

    # Логіка для видалення всіх акаунтів
    if message.text == "Видалити всі акаунти🗑️":
        msg = bot.send_message(chat_id, "Ви впевнені, що хочете видалити всі акаунти? Це не можна буде скасувати.", reply_markup=confirm_delete_all_accounts_menu())
        bot.register_next_step_handler(msg, confirm_delete_all_accounts)
        return

    try:
        account_number = int(message.text) - 1  # Перетворюємо введений номер на індекс
        if 0 <= account_number < len(accounts):
            deleted_account = accounts.pop(account_number)
            bot.send_message(chat_id, f"Акаунт '{deleted_account}' видалено!", reply_markup=accounts_menu())
            # Перевірка на наявність акаунтів
            if not accounts:  # Якщо акаунтів більше немає
                bot.send_message(chat_id, "⚠️Ви видалили всі акаунти.", reply_markup=accounts_menu())
            else:
                show_accounts(chat_id)  # Оновлюємо список акаунтів
        else:
            bot.send_message(chat_id, "Невірний номер акаунту. Спробуйте ще раз.", reply_markup=delete_account_menu())
            return
    except ValueError:
        # Якщо введено не число
        bot.send_message(chat_id, "Будь ласка, введіть число для номеру акаунту. Спробуйте ще раз:", reply_markup=delete_account_menu())
        # Продовжуємо чекати ввід правильної цифри
        bot.register_next_step_handler(message, delete_account)

# Підтвердження видалення всіх акаунтів
def confirm_delete_all_accounts(message):
    chat_id = message.chat.id
    if message.text == "Підтвердити ✅":
        user_data[chat_id]["accounts"].clear()  # Очищаємо список акаунтів
        bot.send_message(chat_id, "Всі акаунти були видалені!", reply_markup=accounts_menu())
        show_accounts(chat_id)  # Оновлюємо список акаунтів
    elif message.text == "Відмінити ❌":
        bot.send_message(chat_id, "Видалення акаунтів скасовано.", reply_markup=accounts_menu())
        show_accounts(chat_id)  # Оновлюємо список акаунтів
    else:
        bot.send_message(chat_id, "Невірний вибір. Спробуйте ще раз.", reply_markup=confirm_delete_all_accounts_menu())
        bot.register_next_step_handler(message, confirm_delete_all_accounts)

# Хендлер для /start і головного меню
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {"accounts": [], "prices": [], "messages": [], "adding_account": False}  # Ініціалізація даних для користувача
    bot.send_message(message.chat.id, "Цей бот пропонує два основні розділи для роботи з акаунтами та фінансами:\n\n*Акаунти 📁* — для додавання/видалення акаунтів та полегшення модерації на платформі FunPay.\n\n*Фінанси 💰* — для додавання сум з продажів, а також автоматичного обчислення загального заробітку за місяць і весь час.\n\nЩоб продовжити, виберіть потрібний розділ: *Акаунти* або *Фінанси*.", reply_markup=main_menu(), parse_mode='Markdown')


# Хендлер для кнопок
@bot.message_handler(func=lambda message: True)
def menu_handler(message):
    chat_id = message.chat.id

    # Ініціалізація даних користувача, якщо їх немає
    if chat_id not in user_data:
        user_data[chat_id] = {"accounts": [], "prices": [], "messages": [], "adding_account": False}

    # Перехід до розділу "Акаунти"
    if message.text == "Акаунти📁":
        show_accounts(chat_id)

    # Перехід до розділу "Фінанси"
    elif message.text == "Фінанси💰":
        show_finances(chat_id)

     # Перехід до меню "Установить ціну"
    elif message.text == "Установить ціну💵":
        msg = bot.send_message(chat_id, "🆕Введіть ціну акаунту в $:", reply_markup=set_price_menu())
        bot.register_next_step_handler(msg, set_price)

    # Перехід до меню "Купили акк"
    elif message.text == "Купили акк💸":
        bought_account(message)

    # Створення виписки (графік)
    elif message.text == "Создать виписку📊":
        create_report(chat_id)

    # Повернення до головного меню
    elif message.text == "Назад↩️":
        bot.send_message(chat_id, "Виберіть розділ:", reply_markup=main_menu())

    # Повернення до головного меню (незалежно від наявності акаунтів)
    elif message.text == "Назад↩️":
        # Повертаємось до головного меню, не показуючи акаунти
        bot.send_message(chat_id, "Виберіть розділ:", reply_markup=main_menu())

    # Додавання нового акаунту
    elif message.text == "Добавить акаунт➕":
        user_data[chat_id]["adding_account"] = True  # Встановлюємо статус додавання акаунту
        msg = bot.send_message(chat_id, "🆕Введіть дані для нового акаунту:", reply_markup=add_account_menu())
        bot.register_next_step_handler(msg, add_account)

    # Видалення акаунту
    elif message.text == "Удалить акаунт⛔":
        if not user_data[chat_id]["accounts"]:  # Якщо акаунти відсутні
            bot.send_message(chat_id, "У вас поки немає акаунтів для видалення.", reply_markup=accounts_menu())
            return
        msg = bot.send_message(chat_id, "Введіть номер акаунту, який потрібно видалити:", reply_markup=delete_account_menu())
        bot.register_next_step_handler(msg, delete_account)

    # Видалити всі акаунти
    elif message.text == "Видалити всі акаунти🗑️":
        if not user_data[chat_id]["accounts"]:  # Якщо акаунти відсутні
            bot.send_message(chat_id, "У вас немає акаунтів для видалення.", reply_markup=accounts_menu())
        else:
            msg = bot.send_message(chat_id, "Ви впевнені, що хочете видалити всі акаунти? Це не можна буде скасувати.", reply_markup=confirm_delete_all_accounts_menu())
            bot.register_next_step_handler(msg, confirm_delete_all_accounts)
        return

    # Якщо текст не відповідає жодній дії
    else:
        bot.send_message(chat_id, "Я не розумію цю команду. Спробуйте ще раз.")

# Запуск бота
bot.polling(none_stop=True)