import config
import telebot
from telebot import types# кнопки
from string import Template

bot = telebot.TeleBot(config.TOKEN)
text_about = '''Что вы получите после окончания курсов?🧑🏻‍💻👩🏻‍💻
💥 Основы программирования; 
💥 Владение языком - Python;
💥 И многое, многое другое...Хотите записаться на на пробный урок?'''

text_title = '''Ваша заявка принята😊. Ждём вас в воскресенье в 15:00 
по адресу: ул.Раззакова 32 (бизнес-центр «Олимп»),
 6 этаж 03 кабинет. Убедительно просим не опаздывать!🤗'''

 
user_dict = {}

class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname','cource', 'phone', ]
        
        for key in keys:
            self.key = None

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('static/itc.png', 'rb')
	bot.send_sticker(message.chat.id, sti)

	# keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Информация")
	item2 = types.KeyboardButton("Пробный урок")
	item3 = types.KeyboardButton("Оставить заявку")
    

	markup.row(item1, item2).add(item3)

	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, \
     бот созданный чтобы принимать заявку на пробный урок и проинформировать вас о наших курсах))".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.text == 'Пробный урок':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Python")
        item2 = types.KeyboardButton("Javascript")
        item3 = types.KeyboardButton("Full-stack")


        markup.row(item1, item2).add(item3)
        bot.send_message(message.chat.id, "  <b>{0.first_name}</b>, на какие курсы я могу вас записать?!".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)
    if message.text == 'Python':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Да")
        markup.add(item1)
        bot.send_message(message.chat.id, text_about, reply_markup=markup)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Python")
                        


        
    elif message.text == 'Javascript':
        bot.send_message(message.chat.id, 'https://www.inst\nagram.com/p/CR1n2C8r-ge/?utm_source=ig_web_copy_link')
    elif message.text == 'Full-stack':
        bot.send_message(message.chat.id, 'https://www.instagram.com/p/CQlmqMHL1UR/?utm_source=ig_web_copy_link')
    elif message.text == 'Пробный урок':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
        item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
        markup.add(item1, item2)

    elif message.text == 'Оставить заявку' or message.text == 'Да':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Ош')
        itembtn2 = types.KeyboardButton('Бишкек')

        markup.add(itembtn1, itembtn2,)

        msg = bot.send_message(message.chat.id, 'Ваш город?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_city_step)

def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Фамилия Имя Отчество', reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('JavaScript')
        itembtn2 = types.KeyboardButton('Python')
        itembtn3 = types.KeyboardButton('FULL-Stack')

   
        markup.add(itembtn1, itembtn2, itembtn3, )

        msg = bot.send_message(chat_id, 'На какой пробный урок вас записать', reply_markup=markup)
        bot.register_next_step_handler(msg,cource)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')
def cource(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.cource = message.text

        msg = bot.send_message(chat_id, 'Ваш номер телефона')
        bot.register_next_step_handler(msg, phone)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def phone(message):
    try:
        int(message.text)
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, text_title, parse_mode="Markdown")
        # отправить в группу которую указываете 
        bot.send_message(bot.get_chat('@itc_kg').id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown") 
                
    except Exception as e:
        msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
        bot.register_next_step_handler(msg,phone)

def getRegData(user, title, name):
    t = Template('$title *$name* \nГород: *$userCity* \nФамилия и имя: *$fullname* \nПробный урок по: *$cource* \nТелефон: *$phone*  ')

    return t.substitute({
        'title': title,
        'name': name,
        'userCity': user.city,
        'fullname': user.fullname,
        'cource': user.cource,
        'phone':user.phone

    })

bot.polling(none_stop=True)



