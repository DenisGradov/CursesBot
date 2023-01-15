import telebot, sqlite3,urllib.parse,re,random
from telebot import types
from config import * 
from datetime import date

curs=[0,0,0,0]

connect=sqlite3.connect('db.db')
cursor=connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    tg_id id,
    check_curs INTEGER,
    ban TEXT
)""")
connect.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS curs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    link TEXT,
    download TEXT,
    pas_state TEXT,
    pas TEXT
)""")
connect.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS stats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checkToday INTEGER,
    checkAll INTEGER,
    nowDay TEXT
)""")
connect.commit()


connect=sqlite3.connect('db.db')
cursor=connect.cursor()
cursor.execute(f"SELECT id FROM stats")
data=cursor.fetchone()

if data is None:
    connect  = sqlite3.connect('db.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO stats (checkToday, checkAll, nowDay) VALUES (?, ?, ?)', (0,0,date.today()))
    connect.commit() 

bot=telebot.TeleBot(token)

@bot.message_handler()
def ms(message):
    
    connect=sqlite3.connect('db.db')
    cursor=connect.cursor()
    cursor.execute(f"SELECT ban FROM users WHERE tg_id=?", (message.chat.id,))
    ban=cursor.fetchone()
    connect.commit()
    if ban is None:
            x = bot.get_chat_member(channel, message.chat.id)
            if x.status == "member" or x.status == "creator" or x.status == "administrator":
                user_menu(message)
            else:
                klava=types.InlineKeyboardMarkup(row_width=1)
                btn1=types.InlineKeyboardButton(text='📚 Канал', url=channelLink)
                btn2=types.InlineKeyboardButton(text='Проверить подписку ✅', callback_data='check')
                klava.add(btn1,btn2)
                bot.send_message(message.chat.id, '😅Привет!\nЯ создал данного бота совершенно бесплатно. Благодаря нему - ты можешь получить совершенно разные знания, из разных сфер. Взамен я лишь прошу оформить подписку на мой канал.\nНе беспокойся, в нем нет ни спама, ни рекламы. В этом канале я публикую свои проекты, которые могут быть тебе интересны.\n\nПодпишись на канал, а после нажми на "Проверить подписку"', reply_markup=klava, parse_mode='Markdown')
    else:
        ban=ban[0]
        if ban=='0':
            x = bot.get_chat_member(channel, message.chat.id)
            if x.status == "member" or x.status == "creator" or x.status == "administrator":
                user_menu(message)
            else:
                klava=types.InlineKeyboardMarkup(row_width=1)
                btn1=types.InlineKeyboardButton(text='📚 Канал', url=channelLink)
                btn2=types.InlineKeyboardButton(text='Проверить подписку ✅', callback_data='check')
                klava.add(btn1,btn2)
                bot.send_message(message.chat.id, '😅Привет!\nЯ создал данного бота совершенно бесплатно. Благодаря нему - ты можешь получить совершенно разные знания, из разных сфер. Взамен я лишь прошу оформить подписку на мой канал.\nНе беспокойся, в нем нет ни спама, ни рекламы. В этом канале я публикую свои проекты, которые могут быть тебе интересны.\n\nПодпишись на канал, а после нажми на "Проверить подписку"', reply_markup=klava, parse_mode='Markdown')

@bot.callback_query_handler(func= lambda callback: callback.data)
def ms(call):
    if call.data=='check':
        x = bot.get_chat_member(channel, call.message.chat.id)
        if x.status == "member" or x.status == "creator" or x.status == "administrator":
            message=call.message
            bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAEGs2ljjmUphqqhjOWhjWm092qCQAfDjQAChwIAAladvQpC7XQrQFfQkCsE')
            bot.send_message(message.chat.id,'/start')
            user_menu(message)
        else:
            klava=types.InlineKeyboardMarkup(row_width=1)
            btn1=types.InlineKeyboardButton(text='📚 Канал', url=channelLink)
            btn2=types.InlineKeyboardButton(text='Проверить подписку ✅', callback_data='check')
            klava.add(btn1,btn2)
            bot.send_message(call.message.chat.id, '😅Привет!\nЯ создал данного бота совершенно бесплатно. Благодаря нему - ты можешь получить совершенно разные знания, из разных сфер. Взамен я лишь прошу оформить подписку на мой канал.\nНе беспокойся, в нем нет ни спама, ни рекламы. В этом канале я публикую свои проекты, которые могут быть тебе интересны.\n\nПодпишись на канал, а после нажми на "Проверить подписку"', reply_markup=klava, parse_mode='Markdown')


def user_menu(message):
    connect=sqlite3.connect('db.db')
    cursor=connect.cursor()
    cursor.execute(f"SELECT tg_id FROM users WHERE tg_id={message.chat.id}")
    data=cursor.fetchone()

    if data is None:
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute('INSERT INTO users (name, tg_id, ban, check_curs) VALUES (?, ?, ?, ?)', (message.from_user.first_name, message.chat.id, 0, 0))
        connect.commit() 
        bot.send_message(logs,f'Новый юзер в боте - @{message.from_user.first_name} ({message.chat.id})')
    elif message.text=='➕Добавить' and message.chat.id==admin:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('◀️Назад')
        step1=bot.send_message(message.chat.id,'1️⃣ Отправь ссылку на курс',reply_markup=klava)
        bot.register_next_step_handler(step1,step1_def)
    elif message.text=='🔥Скачать курс':
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('🎲Рандомый курс','◀️Назад')
        down1=bot.send_message(message.chat.id,'Отправь ссылку на курс:\n(Не знаешь как сделать? Смотри инфо)',reply_markup=klava)
        bot.register_next_step_handler(down1,down1_def)
    elif message.text=='ℹ️Инфо':
        connect=sqlite3.connect('db.db')
        cursor=connect.cursor()
        cursor.execute(f"SELECT check_curs FROM users WHERE tg_id={message.chat.id}")
        curssee=cursor.fetchone()
        connect.commit()
        
        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT COUNT (id) FROM curs')
        connect.commit()
        
        cursall=cursor.fetchall()[0][0]

        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT COUNT (id) FROM users')
        connect.commit()
        usersAll=cursor.fetchall()[0][0]

        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT checkToday FROM stats')
        connect.commit()
        checkToday=cursor.fetchall()[0][0]

        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT checkAll FROM stats')
        connect.commit()
        checkAll=cursor.fetchall()[0][0]

        klava=types.InlineKeyboardMarkup(row_width=1)
        btn1=types.InlineKeyboardButton(text='📚Тема на лолзе',url=lolz) 
        btn2=types.InlineKeyboardButton(text='💿Как найти курс?',url=howFindCurs) 
        btn3=types.InlineKeyboardButton(text='🧔🏿‍♂️Автор бота',url=autor) 
        klava.add(btn1,btn2,btn3)
        text=f'{message.from_user.first_name} (`{message.chat.id}`)\nВы получили `{curssee[0]}` курсов.\n\nЮзеров в боте: `{usersAll}`\nКурсов в боте: `{cursall}`\nПолучено курсов: `{checkAll}`\nПолучено курсов сегодня: `{checkToday}`'
        bot.send_message(message.chat.id, text,parse_mode='Markdown', reply_markup=klava)
    elif message.text=='❌Бан' and message.chat.id==admin:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('◀️Назад')
        ban=bot.send_message(message.chat.id,'🆔 Какого пользователя ты хочешь забанить(разбанить)?',reply_markup=klava)
        bot.register_next_step_handler(ban,ban_def)
    elif message.text=='📭Рассылка' and message.chat.id==admin:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('◀️Назад')
        ads=bot.send_message(message.chat.id,'✏️ Введи текст своей рассылки. Если хочешь, что бы у рассылки была фотография - отправь фотографию, добавив к ней текст (одним сообщением)',reply_markup=klava)
        bot.register_next_step_handler(ads,ads_f)
    else:
        klava=types.ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
        klava.add('🔥Скачать курс','ℹ️Инфо')
        if message.chat.id==admin:
            klava.add('➕Добавить','📭Рассылка','❌Бан')
        bot.send_message(message.chat.id,'Меню:',reply_markup=klava)


photo_status=''
photo_id=''
description=''

def ads_f(message):
    global photo_status
    global photo_id
    global description
    if message.content_type!='photo' and message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('◀️Назад')
        ads=bot.send_message(message.chat.id,'✏️ Введи текст своей рассылки. Если хочешь, что бы у рассылки была фотография - отправь фотографию, добавив к ней текст (одним сообщением)',reply_markup=klava)
        bot.register_next_step_handler(ads,ads_f)

    elif message.text=='◀️Назад':
        user_menu(message)
    elif message.content_type=='photo':
        bot.send_photo(message.chat.id, message.photo[0].file_id, message.caption)
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='✅ Создаем'
        button2='⬅️ Вернуться'
        klava.add(button1,button2)
        photo_status=1
        description=message.caption
        photo_id=message.photo[0].file_id
        ads_y=bot.send_message(message.chat.id,'Вот так будет выглядеть рассылка. Проверь и подтверди старт рекламы', reply_markup=klava)
        bot.register_next_step_handler(ads_y,ads_yf)
    else:
        bot.send_message(message.chat.id, message.text)
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='✅ Создаем'
        button2='⬅️ Вернуться'
        klava.add(button1,button2)
        photo_status=0
        description=message.text
        ads_y=bot.send_message(message.chat.id,'Вот так будет выглядеть рассылка. Проверь и подтверди старт рекламы', reply_markup=klava)
        bot.register_next_step_handler(ads_y,ads_yf)

def ads_yf(message):
    if message.text is None:
        user_menu(message)
    elif message.text=='⬅️ Вернуться':
        user_menu(message)
    else:

        global photo_status
        global photo_id
        global description

        connect  = sqlite3.connect('db.db')
        cursor = connect.cursor()
        cursor.execute(f'SELECT id FROM users ORDER BY id DESC LIMIT 1')
        connect.commit()
        i=1
        i2=int((cursor.fetchall())[0][0])
        try_false=0
        try_true=0
        for i in range(i2+1):
            connect  = sqlite3.connect('db.db')
            cursor = connect.cursor()
            cursor.execute(f'SELECT tg_id FROM users WHERE id = ?', (i,))
            connect.commit()
            if photo_status==1:
                try_true=try_true+1
                try:
                    bot.send_photo(cursor.fetchall()[0][0],photo_id,description)
                except Exception as error:
                    try_false=try_false+1

            else:
                try_true=try_true+1
                try:
                    bot.send_message(cursor.fetchall()[0][0],description)
                except Exception as error:
                    try_false=try_false+1
        
        text=f'📭 Рассылка была отправлена `{try_true-1}` пользователям!\n✅ Успешно доставлено: `{try_true-try_false}`\n❌ Не дошло: `{try_false-1}`'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        user_menu(message)


def ban_def(message):
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('🎲Рандомый курс','◀️Назад')
        ban=bot.send_message(message.chat.id,'🆔 Какого пользователя ты хочешь забанить(разбанить)?',reply_markup=klava)
        bot.register_next_step_handler(ban,ban_def)
    elif message.text=='◀️Назад':
        user_menu(message)
    else:
        connect=sqlite3.connect('db.db')
        cursor=connect.cursor()
        cursor.execute(f"SELECT ban FROM users WHERE tg_id=?", (message.text,))
        ban=cursor.fetchone()
        connect.commit()

        if ban is None:
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('◀️Назад')
            ban=bot.send_message(message.chat.id,'🆔 Какого пользователя ты хочешь забанить(разбанить)?',reply_markup=klava)
            bot.register_next_step_handler(ban,ban_def)
        else:
            
            connect=sqlite3.connect('db.db')
            cursor=connect.cursor()
            cursor.execute(f"SELECT name FROM users WHERE tg_id={message.text}")
            name=cursor.fetchone()[0]
            connect.commit()
            ban=ban[0]
            print(ban)
            if ban=='0':
                ban=1
                ms='забанен'
            else:
                ban=0
                ms='разбанен'
            connect  = sqlite3.connect('db.db')
            cursor = connect.cursor()
            cursor.execute('UPDATE users SET ban = (?) WHERE tg_id = (?)', (ban,message.text, )) 
            connect.commit()
            bot.send_message(message.chat.id,f'{name} был успешно {ms}!')
            user_menu(message)

def down1_def(message):
    try:
        msOld=''
        if message.text is None:
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('🎲Рандомый курс','◀️Назад')
            down1=bot.send_message(message.chat.id,'Отправь ссылку на курс:\n(Не знаешь как сделать? Смотри инфо)',reply_markup=klava)
            bot.register_next_step_handler(down1,down1_def)
        elif message.text=='◀️Назад':
            user_menu(message)
        else:
            if message.text=='🎲Рандомый курс':
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT COUNT (id) FROM curs')
                x=random.randint(1, int(cursor.fetchone()[0]))
                connect.commit()
                
                connect=sqlite3.connect('db.db')
                cursor=connect.cursor()
                cursor.execute(f"SELECT link FROM curs WHERE id=?", (x,))
                link=cursor.fetchone()
                if link is None:
                    bot.send_message(message.chat.id,'Что-то пошло не так')
                else:
                    msOld=message.text
                    message.text=link[0]
                
            connect=sqlite3.connect('db.db')
            cursor=connect.cursor()
            cursor.execute(f"SELECT download FROM curs WHERE link=?", (message.text,))
            data=cursor.fetchone()
            cursor.execute(f"SELECT download FROM curs WHERE name=?", (message.text,))
            data2=cursor.fetchone()
            cursor.execute(f"SELECT pas_state FROM curs WHERE name=?", (message.text,))
            pas_state=cursor.fetchone()
            if pas_state is None:
                cursor.execute(f"SELECT pas_state FROM curs WHERE link=?", (message.text,))
                pas_state=cursor.fetchone()
            if pas_state is None:
                passw=''
            else:
                pas_state=pas_state[0]
                if pas_state=='True':
                    cursor.execute(f"SELECT pas FROM curs WHERE name=?", (message.text,))
                    pas=cursor.fetchone()[0]
                    passw=f'\n\nПароль: {pas}'
                else:
                    passw=''

            print(data)
            if data is None and data2 is None:
                print(data2)
                klava=types.InlineKeyboardMarkup(row_width=1)
                btn1=types.InlineKeyboardButton(text='Попросить курс⚒',url=lolz)
                klava.add(btn1)
                bot.send_message(message.chat.id,'Данного курса нет в базе данных. Скинь ссылку на курс в тему лолза',reply_markup=klava)
            else:
                if data is None:
                    link=data2[0]
                else:
                    link=data[0]
                if msOld!='':
                    try:
                        klava=types.InlineKeyboardMarkup(row_width=1)
                        btn1=types.InlineKeyboardButton(text='Оставить отзыв🥇',url=lolz)
                        btn2=types.InlineKeyboardButton(text='Скачать курс🔥',url=link)
                        btn0=types.InlineKeyboardButton(text='Источник курса🔗',url=message.text)
                        klava.add(btn2,btn1,btn0)
                        bot.send_message(message.chat.id,f'Вот твоя ссылка!\nВежливым тоном будет написать в теме лолза "Благодарность" за получение курса :){passw}',reply_markup=klava)
                    except:
                        klava=types.InlineKeyboardMarkup(row_width=1)
                        btn1=types.InlineKeyboardButton(text='Оставить отзыв🥇',url=lolz)
                        btn0=types.InlineKeyboardButton(text='Источник курса🔗',url=message.text)
                        klava.add(btn1,btn0)
                        bot.send_message(message.chat.id,f'Вот твоя ссылка!\nВежливым тоном будет написать в теме лолза "Благодарность" за получение курса :){passw}',reply_markup=klava)
                        if len(link) > 4096:
                            for x in range(0, len(link), 4096):
                                bot.send_message(message.chat.id, link[x:x+4096])
                        else:
                            bot.send_message(message.chat.id, link)
                else:
                   
                    
                    try:
                        klava=types.InlineKeyboardMarkup(row_width=1)
                        btn1=types.InlineKeyboardButton(text='Оставить отзыв🥇',url=lolz)
                        btn2=types.InlineKeyboardButton(text='Скачать курс🔥',url=link)
                        klava.add(btn2,btn1)
                        bot.send_message(message.chat.id,f'Вот твоя ссылка!\nВежливым тоном будет написать в теме лолза "Благодарность" за получение курса :){passw}',reply_markup=klava)

                    except:
                        klava=types.InlineKeyboardMarkup(row_width=1)
                        btn1=types.InlineKeyboardButton(text='Оставить отзыв🥇',url=lolz)
                        klava.add(btn1)
                        bot.send_message(message.chat.id,f'Вот твоя ссылка!\nВежливым тоном будет написать в теме лолза "Благодарность" за получение курса :){passw}',reply_markup=klava)
                        if len(link) > 4096:
                            for x in range(0, len(link), 4096):
                                bot.send_message(message.chat.id, link[x:x+4096])
                        else:
                            bot.send_message(message.chat.id, link)

                user_menu(message)
                connect=sqlite3.connect('db.db')
                cursor=connect.cursor()
                cursor.execute(f"SELECT check_curs FROM users WHERE tg_id={message.chat.id}")
                curssee=cursor.fetchone()
                connect.commit()
                x=curssee[0]+1
                
                bot.send_message(logs,f'@{message.from_user.username} | {message.chat.id} посмотрел курс (за все время уже {x} курсов')
                
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute('UPDATE users SET check_curs = (?) WHERE tg_id = (?)', (x,message.chat.id, )) 
                connect.commit()
            
                connect=sqlite3.connect('db.db')
                cursor=connect.cursor()
                cursor.execute(f"SELECT checkAll FROM stats")
                curssee=cursor.fetchone()
                connect.commit()
                x=curssee[0]+1
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute('UPDATE stats SET checkAll = (?)', (x,)) 
                connect.commit()

                tod=date.today()
                
                connect=sqlite3.connect('db.db')
                cursor=connect.cursor()
                cursor.execute(f"SELECT nowDay FROM stats")
                curssee=cursor.fetchone()
                connect.commit()
                if str(tod)==str(curssee[0]):
                    connect  = sqlite3.connect('db.db')
                    cursor = connect.cursor()
                    cursor.execute(f"SELECT checkToday FROM stats")
                    connect.commit()
                    x=cursor.fetchone()[0]+1
                else:
                    connect  = sqlite3.connect('db.db')
                    cursor = connect.cursor()
                    cursor.execute('UPDATE stats SET nowDay = (?) ', (tod, )) 
                    connect.commit()
                    x=1
                connect  = sqlite3.connect('db.db')
                cursor = connect.cursor()
                cursor.execute('UPDATE stats SET checkToday = (?) ', (x, )) 
                connect.commit()
    except:
        bot.send_message(message.chat.id,'Что-то пошло не так')


        user_menu(message)


def step1_def(message):
    global curs
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('◀️Назад')
        step1=bot.send_message(message.chat.id,'1️⃣ Отправь ссылку на курс',reply_markup=klava)
        bot.register_next_step_handler(step1,step1_def)
    elif message.text=='◀️Назад':
        message.text=='/start'
        user_menu(message)
    else:
        curs[0]=message.text
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('◀️Назад')
        step2=bot.send_message(message.chat.id,'2️⃣ Отправь ссылку на скачивание',reply_markup=klava)
        bot.register_next_step_handler(step2,step2_def)

def step2_def(message):
    global curs
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('◀️Назад')
        step2=bot.send_message(message.chat.id,'2️⃣ Отправь ссылку на скачивание',reply_markup=klava)
        bot.register_next_step_handler(step2,step2_def)
    elif message.text=='◀️Назад':
        message.text=='/start'
        user_menu(message)
    else:
        curs[1]=message.text
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('❌Пароля нет')
        klava.add('◀️Назад')
        step3=bot.send_message(message.chat.id,'3️⃣ Если у курса есть пароль - введи его. В противном случае нажми на кнопку',reply_markup=klava)
        bot.register_next_step_handler(step3,step3_def)

def step3_def(message):
    global curs
    if message.text is None:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('❌Пароля нет')
        klava.add('◀️Назад')
        step3=bot.send_message(message.chat.id,'3️⃣ Если у курса есть пароль - введи его. В противном случае нажми на кнопку',reply_markup=klava)
        bot.register_next_step_handler(step3,step3_def)
    elif message.text=='◀️Назад':
        message.text=='/start'
        user_menu(message)
    elif message.text=='❌Пароля нет':
        curs[2]='-'
        curs[3]='False'
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('✅Создаем','❌Не создаем')
        step4=bot.send_message(message.chat.id,f'4️⃣ Подтверди создание курса\n\n*Курс:* {curs[0]}\n*Скачать:* {curs[1]}\n*Пароль:* -',reply_markup=klava)
        bot.register_next_step_handler(step4,step4_def)
    else:
        curs[2]=message.text
        curs[3]='True'
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        klava.add('✅Создаем','❌Не создаем')
        step4=bot.send_message(message.chat.id,f'4️⃣ Подтверди создание курса\n\n*Курс:* {curs[0]}\n*Скачать:* {curs[1]}\n*Пароль:* `{message.text}`',reply_markup=klava)
        bot.register_next_step_handler(step4,step4_def)


def step4_def(message):
    global curs
    if message.text is None:
        if curs[2]=='-':
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('✅Создаем','❌Не создаем')
            step4=bot.send_message(message.chat.id,f'4️⃣ Подтверди создание курса\n\n*Курс:* {curs[0]}\n*Скачать:* {curs[1]}\n*Пароль:* -',reply_markup=klava, parse_mode='Markdown')
            bot.register_next_step_handler(step4,step4_def)
        else:
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('✅Создаем','❌Не создаем')
            step4=bot.send_message(message.chat.id,f'4️⃣ Подтверди создание курса\n\n*Курс:* {curs[0]}\n*Скачать:* {curs[1]}\n*Пароль:* `{curs[2]}`',reply_markup=klava, parse_mode='Markdown')
            bot.register_next_step_handler(step4,step4_def)
    elif message.text=='❌Не создаем':
        message.text=='/start'
        user_menu(message)
    elif message.text=='✅Создаем':
        if needs_decoding(curs[0]):
            name= curs[0]
            link = urllib.parse.unquote(curs[0])
        else:
            name= urllib.parse.quote((curs[0]), safe=':/*().')
            link = (curs[0])
        
        connect=sqlite3.connect('db.db')
        cursor=connect.cursor()
        cursor.execute(f"SELECT download FROM curs WHERE link=?", (link,))
        data=cursor.fetchone()
        cursor.execute(f"SELECT download FROM curs WHERE name=?", (name,))
        data2=cursor.fetchone()

        if data is None and data2 is None:
            connect  = sqlite3.connect('db.db')
            cursor = connect.cursor()
            cursor.execute('INSERT INTO curs (name,link, download, pas_state, pas) VALUES (?, ?, ?, ?,?)', (name,link, curs[1], curs[3], curs[2]))
            connect.commit()
            bot.send_message(message.chat.id,'Курс успешно добавлен!')
        else:
            bot.send_message(message.chat.id,'Курс уже есть в базе!')
        message.text=='/start'
        user_menu(message)

    else:
        if curs[2]=='-':
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('✅Создаем','❌Не создаем')
            step4=bot.send_message(message.chat.id,f'4️⃣ Подтверди создание курса\n\n*Курс:* {curs[0]}\n*Скачать:* {curs[1]}\n*Пароль:* -',reply_markup=klava)
            bot.register_next_step_handler(step4,step4_def)
        else:
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            klava.add('✅Создаем','❌Не создаем')
            step4=bot.send_message(message.chat.id,f'4️⃣ Подтверди создание курса\n\n*Курс:* {curs[0]}\n*Скачать:* {curs[1]}\n*Пароль:* `{curs[2]}`',reply_markup=klava)
            bot.register_next_step_handler(step4,step4_def)


def needs_decoding(url):
    return bool(re.search(r'%[0-9A-Fa-f]{2}', url))

bot.polling()

