from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import timedelta, date


BOOKS_TOP = [
    {
        "title": "Война и мир",
        "author": "Л.Н. Толстой",
        "year": 1869,
        "description": "Эпический роман о судьбах людей на фоне войны 1812 года. Одно из величайших произведений мировой литературы."
    },
    {
        "title": "Преступление и наказание",
        "author": "Ф.М. Достоевский",
        "year": 1866,
        "description": "Глубокий психологический роман, исследующий природу преступления и муки совести."
    },
    {
        "title": "Евгений Онегин",
        "author": "А.С. Пушкин",
        "year": 1833,
        "description": "Роман в стихах, названный Белинским 'энциклопедией русской жизни'."
    },
    {
        "title": "Мастер и Маргарита",
        "author": "М.А. Булгаков",
        "year": 1967,
        "description": "Мистический роман о визите дьявола в Москву 1930-х годов."
    },
    {
        "title": "1984",
        "author": "Джордж Оруэлл",
        "year": 1949,
        "description": "Антиутопия о тоталитарном обществе будущего, где свобода мысли под запретом."
    }
]
WRITERS_DB = {
    'hemingway': {
        'name': 'Эрнест Хемингуэй',
        'years': '1899–1961',
        'bio': 'Американский писатель, лауреат Нобелевской премии. Известен лаконичным стилем.',
        'image': 'https://via.placeholder.com/300x400?text=Hemingway',
        'books': [
            {'slug': 'the_old_man_and_the_sea', 'title': 'Старик и море', 'year': 1952, 'desc': 'Повесть о старом рыбаке и его борьбе с гигантским марлином.'},
            {'slug': 'the_sun_also_rises', 'title': 'И восходит солнце', 'year': 1926, 'desc': 'Роман о потерянном поколении после Первой мировой войны.'},
            {'slug': 'for_whom_the_bell_tolls', 'title': 'По ком звонит колокол', 'year': 1940, 'desc': 'Роман о гражданской войне в Испании.'}
        ]
    },
    'shakespeare': {
        'name': 'Уильям Шекспир',
        'years': '1564–1616',
        'bio': 'Английский поэт и драматург, величайший англоязычный писатель.',
        'image': 'https://via.placeholder.com/300x400?text=Shakespeare',
        'books': [
            {'slug': 'hamlet', 'title': 'Гамлет', 'year': 1603, 'desc': 'Трагедия о принце датском и мести.'},
            {'slug': 'romeo_and_juliet', 'title': 'Ромео и Джульетта', 'year': 1597, 'desc': 'История трагической любви.'}
        ]
    },
    'tolstoy': {
        'name': 'Лев Толстой',
        'years': '1828–1910',
        'bio': 'Русский писатель и мыслитель, автор эпопеи «Война и мир».',
        'image': 'https://via.placeholder.com/300x400?text=Tolstoy',
        'books': [
            {'slug': 'war_and_peace', 'title': 'Война и мир', 'year': 1869, 'desc': 'Эпический роман о судьбах людей на фоне войны 1812 года.'},
            {'slug': 'anna_karenina', 'title': 'Анна Каренина', 'year': 1877, 'desc': 'Роман о любви и трагедии в высшем обществе.'}
        ]
    }
}
CARS_DB = {
    'toyota': {
        'brand_name': 'Тойота',
        'cars': [
            {'name': 'Camry', 'model': 'XV70', 'year': 2021, 'engine': '2.5L Бензин', 'features': 'Комфортный седан, надежная подвеска'},
            {'name': 'RAV4', 'model': 'XA50', 'year': 2022, 'engine': '2.0L Гибрид', 'features': 'Кроссовер, полный привод, экономичный расход'}
        ]
    },
    'honda': {
        'brand_name': 'Хонда',
        'cars': [
            {'name': 'Civic', 'model': 'FC', 'year': 2020, 'engine': '1.5L Турбо', 'features': 'Спортивный хэтчбек, отличная управляемость'},
            {'name': 'CR-V', 'model': 'RW', 'year': 2023, 'engine': '2.4L Бензин', 'features': 'Семейный кроссовер, вместительный багажник'}
        ]
    },
    'renault': {
        'brand_name': 'Рено',
        'cars': [
            {'name': 'Duster', 'model': 'HM', 'year': 2022, 'engine': '1.6L Бензин', 'features': 'Внедорожник, высокая проходимость, доступная цена'},
            {'name': 'Logan', 'model': 'II', 'year': 2021, 'engine': '1.6L Бензин', 'features': 'Надежный седан, популярен в такси'}
        ]
    }
}
def get_city_nav():
    return """
    <hr>
    <p style="font-size: 0.9em; color: #666;">
        <b>Меню города:</b> 
        <a href="/city/">← Вернуться в меню приложения</a> • 
        <a href="/news/">Новости</a> • 
        <a href="/management/">Руководство</a> • 
        <a href="/facts/">Факты</a> • 
        <a href="/contacts/">Контакты</a> •
        <a href="/history/">История города</a> • 
    </p>
    """

def home(request):
#   1. ДАТА
    time_now = date.today()
    formatted_time = time_now.strftime("%d.%m.%Y")

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Главная страница</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', sans-serif; 
                padding: 40px; 
                background-color: #f4f7f6; 
                margin: 0;
            }}
            h1 {{ 
                color: #333; 
                text-align: center; 
                margin-bottom: 10px;
            }}
            .subtitle {{
                text-align: center;
                color: #666;
                font-size: 1.1em;
                margin-bottom: 40px;
            }}
            .date-box {{ 
                text-align: center; 
                margin-bottom: 40px; 
                font-size: 1.2em; 
                color: #555; 
            }}
            .cards {{ 
                display: flex; 
                justify-content: center; 
                gap: 30px; 
                flex-wrap: wrap; 
                max-width: 1200px;
                margin: 0 auto;
            }}
            .card {{
                width: 280px; 
                height: 240px;
                background: white; 
                border-radius: 15px;
                padding: 25px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                display: flex; 
                flex-direction: column; 
                justify-content: center;
                text-align: center; 
                transition: transform 0.2s, box-shadow 0.2s;
                border-top: 5px solid #ccc;
            }}
            .card:hover {{ 
                transform: translateY(-5px); 
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }}
            .card h3 {{ 
                margin-top: 0; 
                color: #2c3e50; 
                font-size: 1.3em;
            }}
            .card p {{ 
                color: #7f8c8d; 
                margin: 15px 0; 
                font-size: 1em;
            }}
            .btn {{ 
                margin-top: auto; 
                display: inline-block; 
                padding: 10px 20px; 
                border-radius: 5px; 
                text-decoration: none; 
                font-weight: bold; 
                color: white; 
                font-size: 0.95em;
                transition: background 0.3s;
            }}
            .btn:hover {{
                opacity: 0.9;
            }}
        </style>
    </head>
    <body>
        <h1>Добро пожаловать!</h1>
        <div class="subtitle">Универсальный портал знаний и интересов</div>
        <div class="date-box">📅 Сегодня: <b>{formatted_time}</b></div>
        
        <div class="cards">
        
            
            <!-- День недели -->
            <div class="card" style="border-top: 5px solid #f39c12;">
                 <h3>🗓️ День недели</h3>
                <p>Узнай, какой сегодня день.</p>
                <a href="/day/" class="btn" style="background-color: #f39c12;">Открыть →</a>
                </div>
            <!-- Писатели -->
            <div class="card" style="border-top: 5px solid #8e44ad;">
                <h3>✍️ Писатели</h3>
                <p>Биографии великих авторов.</p>
                <a href="/writers/" class="btn" style="background-color: #8e44ad;">Перейти →</a>
            </div>

            <!-- Книги -->
            <div class="card" style="border-top: 5px solid #27ae60;">
                <h3>📖 Топ книг</h3>
                <p>Лучшие произведения мира.</p>
                <a href="/books/" class="btn" style="background-color: #27ae60;">Перейти →</a>
            </div>

            <!-- День программиста -->
            <div class="card" style="border-top: 5px solid #3498db;">
                <h3>📅 День программиста</h3>
                <p>Расчет 256-го дня года.</p>
                <a href="/programmer/" class="btn" style="background-color: #3498db;">Перейти →</a>
            </div>

            <!-- Таблица умножения -->
            <div class="card" style="border-top: 5px solid #2ecc71;">
                <h3>✖️ Таблица умножения</h3>
                <p>Классическая таблица от 1 до 10.</p>
                <a href="/table/" class="btn" style="background-color: #2ecc71;">Перейти →</a>
            </div>

            <!-- Приложение: Город -->
            <div class="card" style="border-top: 5px solid #e67e22;">
                <h3>🏙️ Приложение: Город</h3>
                <p>Новости, факты, контакты Чебоксар.</p>
                <a href="/city/" class="btn" style="background-color: #e67e22;">Открыть →</a>
            </div>

            <!-- Автомобили -->
            <div class="card" style="border-top: 5px solid #34495e;">
                <h3>🚗 Автомобили</h3>
                <p>Toyota, Honda, Renault — модели и особенности.</p>
                <a href="/toyota/" class="btn" style="background-color: #34495e;">К автомобилям →</a>
            </div>

            <!-- Музыка -->
            <div class="card" style="border-top: 5px solid #9b59b6;">
                <h3>🎵 Музыка</h3>
                <p>Queen — We Are The Champions на 4 языках.</p>
                <a href="/song/" class="btn" style="background-color: #9b59b6;">Слушать →</a>
            </div>
            <div class="card" style="border-top: 5px solid #8E44AD;">
                 <h3>🎧 Наушники</h3>
                <p>Каталог беспроводных моделей</p>
                <a href="/headphones/" class="btn" style="background-color: #8E44AD;">Открыть →</a>
            </div>

            <!-- Звёздные войны -->
            <div class="card" style="border-top: 5px solid #ffe81f;">
                <h3>⭐ Звёздные войны</h3>
                <p>Все фильмы серии через API swapi.dev</p>
                <a href="/swapi/" class="btn" style="background-color: #1a1a2e;">Смотреть →</a>
            </div>
            <!-- Портал -->
            <div class="card" style="border-top: 5px solid #4fc3f7;">
                <h3>🌐 Портал</h3>
                <p>Статьи, новости и админ-панель</p>
                <a href="/articles/" class="btn" style="background-color: #0277bd;">Открыть →</a>
            </div>
         </div>
    </body>
    </html>
    """
    return HttpResponse(html)

#  2. ДЕНЬ ПРОГРАММИСТА
def programmer_day(request):
    today = date.today()
    current_year = today.year
    def get_256th_day(year):
        return date(year, 1, 1) + timedelta(days=255)
    prog_day = get_256th_day(current_year)
    
    if today == prog_day:
        status = "🎉 УРА! СЕГОДНЯ ДЕНЬ ПРОГРАММИСТА! 🎉"
        color = "#d9534f"
    elif today < prog_day:
        days_left = (prog_day - today).days
        status = f"До Дня программиста осталось {days_left} дней."
        color = "#337ab7"
    else:
        next_prog_day = get_256th_day(current_year + 1)
        days_until_next = (next_prog_day - today).days
        status = f"День программиста прошел. До следующего ({next_prog_day.year}) осталось {days_until_next} дней."
        color = "#5cb85c"
    
    nav = f"""
    <hr><p style="font-size: 0.9em; color: #666;">
        <b>Навигация:</b> <a href="/">← Главная</a> • <a href="/table/">Таблица</a> • <a href="/city/">Город</a>
    </p>
    """
    return HttpResponse(f"<h1 style='color: {color}'>День программиста ({current_year})</h1><p>{status}</p>{nav}")

#  3. ТАБЛИЦА УМНОЖЕНИЯ 
def multiplication_table(request):
    table = []
    for i in range(1, 11):
        row = [i * j for j in range(1, 11)]
        table.append((i, row))
    context = {'table': table}
    return render(request, 'multiplication/multiplication_table.html', context)

#  4. ГЛАВНАЯ ПРИЛОЖЕНИЯ "ГОРОД" (МЕНЮ ВНУТРИ ГОРОДА) 

def city_app_home(request):
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head><meta charset="UTF-8"><title>Город Чебоксары</title></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h1>🏙️ Приложение: Город Чебоксары</h1>
        <p>Выберите раздел города:</p>
        <ul style="list-style: none; padding-left: 0;">
            <li style="margin-bottom: 15px;"><a href="/news/" style="font-size: 1.1em; color: #333; text-decoration: none;">📰 Новости города</a></li>
            <li style="margin-bottom: 15px;"><a href="/management/" style="font-size: 1.1em; color: #333; text-decoration: none;">👨‍💼 Руководство города</a></li>
            <li style="margin-bottom: 15px;"><a href="/facts/" style="font-size: 1.1em; color: #333; text-decoration: none;">💡 Интересные факты</a></li>
            <li style="margin-bottom: 15px;"><a href="/contacts/" style="font-size: 1.1em; color: #333; text-decoration: none;">📞 Контактные телефоны</a></li>
            <li style="margin-bottom: 15px;"><a href="/history/" style="font-size: 1.1em; color: #333; text-decoration: none;">🕰️ История города</a></li>
        </ul>
        <hr style="margin: 40px 0;">
        <a href="/">← Вернуться на главную (3 кнопки)</a>
    </body>
    </html>
    """
    return HttpResponse(html)

#  5. ВНУТРЕННИЕ СТРАНИЦЫ ГОРОДА 
def city_news(request):
    content = """
    <h1>Новости города Чебоксары</h1>
    <ul>
        <li><strong>01.10.2026:</strong> Отремонтировали все дороги в городе.</li>
        <li><strong>28.09.2026:</strong> Запущена первая ветка метро.</li>
        <li><strong>25.09.2026:</strong> Проходит фестиваль городской еды.</li>
    </ul>
    """
    return HttpResponse(content + get_city_nav())

def city_management(request):
    content = """
    <h1>Руководство города Чебоксары</h1>
    <p><strong>Мэр города:</strong> Станислав Олегович Трофимов </p>
    <p><strong>Заместитель мэра по вопросам ЖКХ:</strong> Максим Андреев</p>
    <p><strong>Руководитель Департамента транспорта:</strong> Денисов Дмитрий Сергеевич</p>
    """
    return HttpResponse(content + get_city_nav())

def city_facts(request):
    content = """
    <h1>Интересные факты о Чебоксарах</h1>
    <ul>
        <li>Волжская Атлантида: На дне Чебоксарского залива спрятан хрустальный дворец.</li>
        <li>Подземные драконы: Под городом спит гигантский крылатый змей.</li>
        <li>Первое упоминание: 1469 год.</li>
        <li>База из «Звездных войн»: Театр оперы и балета — секретная база повстанцев.</li>
    </ul>
    """
    return HttpResponse(content + get_city_nav())

def city_contacts(request):
    content = """
    <h1>Контактные телефоны городских служб</h1>
    <table style="border-collapse: collapse; width: 50%;">
        <tr style="background: #eee;">
            <th style="border: 1px solid #ccc; padding: 8px;">Служба</th>
            <th style="border: 1px solid #ccc; padding: 8px;">Телефон</th>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px;">Единая диспетчерская служба</td>
            <td style="border: 1px solid #ccc; padding: 8px;">+7 (8352) 23-50-75</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px;">Справочная мэрии</td>
            <td style="border: 1px solid #ccc; padding: 8px;">+7 (8352) 62-85-37</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px;">Экстренные службы (112)</td>
            <td style="border: 1px solid #ccc; padding: 8px;">112 (с мобильного)</td>
        </tr>
    </table>
    """
    return HttpResponse(content + get_city_nav())

# Раздел история
def get_history_nav():
  return """
    <hr>
    <div style="margin-bottom: 15px;">
        <b>Навигация по истории:</b> 
        <a href="/history/" style="color: #2c3e50;">Общая история</a> • 
        <a href="/history/people/" style="color: #2c3e50;">Известные жители</a> • 
        <a href="/history/photos/" style="color: #2c3e50;">Исторические фото</a>
    </div>
    """
    
#  1. ОБЩАЯ ИСТОРИЯ ГОРОДА 
def history_main(request, slug=None):
    content = """
    <h1>📜 История города Чебоксары</h1>
    <p>Чебоксары — один из старейших городов России, чья история тесно связана с великой рекой Волгой.</p>
    <ul>
        <li><strong>1469 год:</strong> Первое летописное упоминание города. Именно эта дата считается официальным годом основания Чебоксар.</li>
        <li><strong>XVI век:</strong> После присоединения к Русскому государству город становится важным торговым и военным форпостом на Волге.</li>
        <li><strong>XIX век:</strong> Чебоксары превращаются в крупный центр торговли хлебом, лесом и рыбой. Город растет и богатеет.</li>
        <li><strong>XX век:</strong> Индустриализация, строительство ГЭС, превращение Чебоксар в столицу Чувашской АССР.</li>
    </ul>
    <p>Сегодня Чебоксары — это город, где древность переплетается с современностью, а легенды живут рядом с фактами.</p>
    """
    full_nav = get_history_nav() + get_city_nav()
    
    return HttpResponse(content + full_nav)

# 2. ИЗВЕСТНЫЕ ЖИТЕЛИ ГОРОДА
def history_people(request, slug=None):
    content = """
    <h1>👨‍🏫 Известные жители Чебоксар</h1>
    <p>Город подарил стране множество талантливых людей. Вот лишь некоторые из них:</p>
    <ul>
        <li><strong>Василий Иванович Чапаев:</strong> Легендарный комдив, герой Гражданской войны. Хотя он родился в соседней деревне, его имя неразрывно связано с историей всего Поволжья и часто звучит в Чебоксарах.</li>
        <li><strong>Пётр Петрович Хузангай:</strong> Выдающийся чувашский поэт, переводчик, общественный деятель. Его творчество — гордость национальной культуры.</li>
        <li><strong>Андриян Николаев:</strong> Космонавт №3, дважды Герой Советского Союза. Уроженец Чувашии, он прославил свой край на весь мир.</li>
        <li><strong>Местные краеведы:</strong> Благодаря их кропотливой работе мы знаем столько интересных фактов о прошлом города.</li>
    </ul>
    <p>Это лишь малая часть тех, кто внес вклад в развитие города. Их наследие живет в названиях улиц и в памяти горожан.</p>
    """
    full_nav = get_history_nav() + get_city_nav()
    
    return HttpResponse(content + full_nav)

#  3. ИСТОРИЧЕСКИЕ ФОТОГРАФИИ 
def history_photos(request, slug=None):
    content = """
    <h1>📸 Исторические фотографии Чебоксар</h1>
    <p>Погрузитесь в атмосферу старого города. К сожалению, в этом текстовом прототипе мы не можем показать реальные картинки, но вот как выглядели главные места раньше:</p>
    
    <div style="margin-top: 20px;">
        <div style="border: 1px solid #ccc; padding: 15px; margin-bottom: 15px;">
            <h3>🏛️ Дореволюционный центр</h3>
            <p>На старых снимках — купеческие дома, торговые ряды и мощеные улицы. Город выглядел совсем иначе, чем сейчас, сохраняя дух провинциальной России.</p>
        </div>
        
        <div style="border: 1px solid #ccc; padding: 15px; margin-bottom: 15px;">
            <h3>🌊 Строительство Чебоксарской ГЭС</h3>
            <p>Один из самых масштабных проектов XX века. Фотографии стройки показывают гигантский размах работ и энтузиазм строителей.</p>
        </div>
        
        <div style="border: 1px solid #ccc; padding: 15px;">
            <h3>🌆 Чебоксары 80-х годов</h3>
            <p>Город в эпоху расцвета: новые микрорайоны, широкие проспекты и узнаваемые силуэты зданий, которые мы видим и сегодня.</p>
        </div>
    </div>
    <p><em>Примечание: В полноценной версии сайта здесь были бы загружены реальные архивные снимки.</em></p>
    """
    full_nav = get_history_nav() + get_city_nav()
    
    return HttpResponse(content + full_nav)

# ПИСАТЕЛИ


# 1. Общий список писателей
def writers_list(request, slug=None):

    # content = """
    # <h1 style="color: #8e44ad;">✍️ Известные писатели</h1>
    # <p>Выберите автора из списка или используйте поиск (в данном прототипе — переход по ссылке).</p>
    # <div style="display: flex; gap: 20px; flex-wrap: wrap;">
    # """
    
    # for key, data in WRITERS_DB.items():
    #     content += f"""
    #     <div style="flex: 1; min-width: 250px; border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: #fff;">
    #         <h3>{data['name']}</h3>
    #         <p><b>Годы жизни:</b> {data['years']}</p>
    #         <a href="/writers/{key}/" style="color: #8e44ad; font-weight: bold;">Подробнее →</a>
    #     </div>
    #     """
    
    # content += """
    # </div>
    # <hr>
    # <p style="color: #666;"><b>Навигация:</b> <a href="/">← На главную</a> | <a href="/books/">Топ лучших книг</a></p>
    # """
    # return HttpResponse(content)


    # Получаем параметры из URL: ?writers=Hemingway&year=1926

    req_writer = request.GET.get('writers')
    req_year = request.GET.get('year')

    if req_writer and req_year:
        w_key = req_writer.lower()

        
        if w_key in WRITERS_DB:
            writer_data = WRITERS_DB[w_key]
            found_book = None

            try:
                year_val = int(req_year)
            except ValueError:
               
                year_val = None

            if year_val is not None:
                for book in writer_data['books']:
                    if book['year'] == year_val:
                        found_book = book
                        break

           
            if found_book:
                html = f"""
                <!DOCTYPE html>
                <html lang="ru">
                <head><meta charset="UTF-8"><title>{found_book['title']}</title></head>
                <body style="font-family: sans-serif; max-width: 700px; margin: 40px auto; background: #f9f9f9; padding: 20px;">
                    <a href="/writers/" style="color: #8e44ad;">← Назад к списку писателей</a>
                    <hr>
                    <h1 style="color: #27ae60;">Результат поиска</h1>
                    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h2>{found_book['title']}</h2>
                        <p><b>Автор:</b> {writer_data['name']}</p>
                        <p><b>Год издания:</b> {found_book['year']}</p>
                        <p>{found_book['desc']}</p>
                    </div>
                    <p style="margin-top: 20px;"><a href="/writers/{w_key}/">Перейти на страницу автора →</a></p>
                </body>
                </html>
                """
                return HttpResponse(html)

        if w_key in WRITERS_DB:
            return redirect('writer_detail', slug=w_key)
        else:
       
            return redirect('writers')

    content = """
    <h1 style="color: #8e44ad;">✍️ Известные писатели</h1>
    <p>Выберите автора из списка:</p>
    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
    """
    for key, data in WRITERS_DB.items():
        content += f"""
        <div style="flex: 1; min-width: 250px; border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: #fff;">
            <h3>{data['name']}</h3>
            <p><b>Годы жизни:</b> {data['years']}</p>
            <a href="/writers/{key}/" style="color: #8e44ad; font-weight: bold;">Подробнее →</a>
        </div>
        """
    content += """
    </div>
    <hr>
    <p style="color: #666;"><b>Навигация:</b> <a href="/">← На главную</a></p>
    """
    return HttpResponse(content)

# 2. Страница конкретного писателя 
def writer_detail(request, slug):
    
    key = slug.lower()
    
    if key not in WRITERS_DB:
    
        return redirect('writers')
    
    data = WRITERS_DB[key]
    
    books_html = ""
    for book in data['books']:
        books_html += f"<li><a href='/writers/{key}/{book['slug']}/' style='color: #27ae60;'>{book['title']}</a> ({book['year']})</li>"

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head><meta charset="UTF-8"><title>{data['name']}</title></head>
    <body style="font-family: sans-serif; max-width: 800px; margin: 40px auto; background: #f9f9f9; padding: 20px;">
        <a href="/writers/" style="color: #8e44ad; text-decoration: underline;">← Назад к списку писателей</a>
        <hr>
        <div style="display: flex; gap: 30px; align-items: top;">
            <div style="flex: 0 0 250px;">
                <img src="{data['image']}" alt="{data['name']}" style="width: 100%; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);">
            </div>
            <div style="flex: 1;">
                <h1 style="color: #8e44ad;">{data['name']} ({data['years']})</h1>
                <p style="line-height: 1.6; color: #444; font-size: 1.1em;">{data['bio']}</p>
                
                <h3 style="margin-top: 30px; color: #27ae60;">Книги автора:</h3>
                <ul style="list-style-position: inside;">{books_html}</ul>
            </div>
        </div>
        <hr>
        <p style="color: #666;"><a href="/">← На главную страницу проекта</a></p>
    </body>
    </html>
    """
    return HttpResponse(html)

def book_by_writer(request, writer_slug, book_slug):
    w_key = writer_slug.lower()
    b_key = book_slug.lower()

    if w_key not in WRITERS_DB:
        return redirect('writers')
    
    writer_data = WRITERS_DB[w_key]
    found_book = None
    for book in writer_data['books']:
        if book['slug'].lower() == b_key:
            found_book = book
            break
    
    if not found_book:
        return redirect('writer_detail', slug=w_key)

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>{found_book['title']} — {writer_data['name']}</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; max-width: 700px; margin: 40px auto; background: #f4f7f6; padding: 20px; }}
            .card {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; }}
            .meta {{ color: #7f8c8d; margin-bottom: 20px; font-size: 0.9em; }}
            p {{ line-height: 1.6; color: #333; }}
            a.back-link {{ color: #8e44ad; text-decoration: underline; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="card">
            <a href="/writers/{w_key}/" class="back-link">← Назад к {writer_data['name']}</a>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            
            <h1>{found_book['title']}</h1>
            <div class="meta">
                <b>Автор:</b> {writer_data['name']} • 
                <b>Год издания:</b> {found_book['year']}
            </div>
            
            <p><b>Описание:</b></p>
            <p>{found_book['desc']}</p>
            
            <hr style="border: 0; border-top: 1px dashed #ccc; margin: 30px 0;">
            <p style="font-size: 0.85em; color: #999;">
                Это страница из раздела писателей нашего проекта.
            </p>
            <a href="/" style="color: #3498db;">← На главную страницу</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def top_books(request, slug=None):
    content = """
    <h1 style="color: #27ae60;">📖 Топ лучших книг</h1>
    <p>Наша субъективная подборка культовых произведений.</p>
    <ol style="line-height: 2em; color: #333;">
    """
    
    for index, book in enumerate(BOOKS_TOP, 1):
        
        content += f"""
        <li>
            <b><a href="/books/{index}/" style="color: #27ae60; text-decoration: none;">{book['title']}</a></b> 
            (<i>{book['author']}, {book['year']}</i>)<br>
            <span style="font-size: 0.9em; color: #666;">{book['description']}</span>
        </li>
        """
    
    content += """
    </ol>
    <hr>
    <p style="color: #666;"><b>Навигация:</b> <a href="/">← На главную</a> | <a href="/writers/">Писатели</a></p>
    """
    return HttpResponse(content)
def book_detail(request, book_id):
  
    if 1 <= book_id <= len(BOOKS_TOP):
        book = BOOKS_TOP[book_id - 1]  
        
        html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>{book['title']} — Топ книг</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 40px auto; background: #f4f7f6; padding: 20px; }}
                .card {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
                h1 {{ color: #27ae60; border-bottom: 2px solid #27ae60; padding-bottom: 10px; }}
                .meta {{ color: #666; margin-bottom: 20px; font-size: 0.9em; }}
                p {{ line-height: 1.6; color: #333; }}
                a.back-link {{ color: #8e44ad; text-decoration: underline; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="card">
                <a href="/books/" class="back-link">← Назад к списку книг</a>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                
                <h1>{book['title']}</h1>
                <div class="meta">
                    <b>Автор:</b> {book['author']} • 
                    <b>Год издания:</b> {book['year']}
                </div>
                
                <p><b>О книге:</b></p>
                <p>{book['description']}</p>
                
                <hr style="border: 0; border-top: 1px dashed #ccc; margin: 30px 0;">
                <p style="font-size: 0.85em; color: #999;">
                    Это страница из раздела «Топ лучших книг» нашего проекта.
                </p>
                <a href="/" style="color: #3498db;">← На главную страницу</a>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)
    else:

        return redirect('books')
    

# фреймворки часть 4

def show_song(request):
   
    lyrics_text = "We are the champions, my friends\nQueen, We are the champions"
    
    context = {
        'lyrics': lyrics_text
    }
    
    return render(request, 'song.html', context)

def show_song_en(request):
    lyrics_text = "We are the champions, my friends\nQueen, We are the champions"
    context = {'lyrics': lyrics_text, 'lang_name': 'English'}
    return render(request, 'song.html', context)

def show_song_fr(request):
    # Перевод на французский
    lyrics_text = "Nous sommes les champions, mes amis\nQueen, Nous sommes les champions"
    context = {'lyrics': lyrics_text, 'lang_name': 'Français'}
    return render(request, 'song.html', context)

def show_song_de(request):
    # Перевод на немецкий
    lyrics_text = "Wir sind die Meister, meine Freunde\nQueen, Wir sind die Meister"
    context = {'lyrics': lyrics_text, 'lang_name': 'Deutsch'}
    return render(request, 'song.html', context)

def show_song_es(request):
    # Перевод на испанский
    lyrics_text = "Somos los campeones, mis amigos\nQueen, Somos los campeones"
    context = {'lyrics': lyrics_text, 'lang_name': 'Español'}
    return render(request, 'song.html', context)

def cars_home(request):
    """Главная страница раздела авто (можно сделать общую подборку или просто приветствие)"""
    context = {
        'car_brand': 'Главная',
        'car_data': None 
    }
    return render(request, 'cars.html', context)

def show_toyota(request):
    data = CARS_DB.get('toyota')
    context = {
        'car_brand': data['brand_name'],
        'car_data': data['cars']
    }
    return render(request, 'cars.html', context)

def show_honda(request):
    data = CARS_DB.get('honda')
    context = {
        'car_brand': data['brand_name'],
        'car_data': data['cars']
    }
    return render(request, 'cars.html', context)

def show_renault(request):
    data = CARS_DB.get('renault')
    context = {
        'car_brand': data['brand_name'],
        'car_data': data['cars']
    }
    return render(request, 'cars.html', context)

