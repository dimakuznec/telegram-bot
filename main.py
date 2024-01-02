import telebot
import platform

# Вставьте свой токен, который вы получили от BotFather
TOKEN = '6686980838:AAGCJJxCttz9406OO1RUNI-7PBCb_aksH2I'
# Вставьте ссылку на ваш Telegram-канал
CHANNEL_LINK = 'https://t.me/IT_juniorMy'
bot = telebot.TeleBot(TOKEN)

user_versions = {}  # Словарь для хранения версий Windows пользователей

def get_skype_version(user_id):
    user_version = user_versions.get(user_id)
    if user_version:
        if '10' in user_version:
            return "Подходящая версия Skype для вашей Windows 10: [Версия Skype для Windows 10](https://www.skype.com/)"
        elif '7' in user_version or '8' in user_version:
            return "Подходящая версия Skype для вашей Windows 7/8: [Версия Skype для Windows 7/8](https://www.skype.com/)"
        elif '11' in user_version:
            return "Подходящая версия Skype для вашей Windows 11: [Версия Skype для Windows 11](https://www.skype.com/)"
        else:
            return "Для вашей версии Windows нет определённой рекомендации для Skype."
    else:
        return "Пожалуйста, укажите версию Windows с помощью команды /setversion."

def get_welcome_message():
    return (
        "Привет! Я могу помочь вам выбрать подходящую версию Skype для вашей операционной системы.\n"
        "Для начала, укажите вашу версию Windows с помощью команды /setversion.\n"
        "Если вы хотите завершить работу со мной, напишите /выход в любой момент."
    )

@bot.message_handler(commands=['start', 'старт'])
def handle_start(message):
    user_id = message.chat.id
    user_versions.pop(user_id, None)  # Сбрасываем выбранную версию при старте
    bot.send_message(user_id, get_welcome_message())

@bot.message_handler(commands=['skypeupdate'])
def handle_skype_update(message):
    user_id = message.chat.id
    skype_version = get_skype_version(user_id)
    bot.send_message(user_id, skype_version, parse_mode='Markdown', disable_web_page_preview=False)
    bot.send_message(user_id, "Если вы хотите завершить работу со мной, напишите /выход в любой момент.")

@bot.message_handler(commands=['setversion'])
def handle_set_version(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Введите вашу версию Windows:")
    bot.register_next_step_handler(message, process_set_version)

def process_set_version(message):
    user_id = message.chat.id
    user_version = message.text.strip()
    user_versions[user_id] = user_version
    bot.send_message(user_id, f"Версия Windows установлена: {user_version}")
    handle_skype_update(message)

@bot.message_handler(commands=['exit', 'выход'])
def handle_exit(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Спасибо за то, что воспользовались нашими услугами! Ваш запрос завершен.\n"
    f"Подписывайтесь на наш Telegram-канал: {CHANNEL_LINK}")
    bot.send_message(user_id, get_welcome_message())  # Отправляем приветственное сообщение

if __name__ == "__main__":
    bot.polling(none_stop=True)
    