from django.http import HttpResponse

# База данных наушников
HEADPHONES_DB = {
    'buds_live': {
        'name': 'Samsung Galaxy Buds Live',
        'year': 2020,
        'features': 'Активное шумоподавление, беспроводные, стильный дизайн, хорошее качество звука',
        'price': '12 990 ₽',
        'image': 'https://via.placeholder.com/200?text=Buds+Live'
    },
    'airpods_pro': {
        'name': 'Apple AirPods Pro',
        'year': 2019,
        'features': 'ANC, прозрачный режим, отличная интеграция с Apple, компактный кейс',
        'price': '19 990 ₽',
        'image': 'https://via.placeholder.com/200?text=AirPods+Pro'
    },
    'sony_wf1000xm4': {
        'name': 'Sony WF-1000XM4',
        'year': 2021,
        'features': 'Лучшее шумоподавление, высокое качество звука, долгий заряд',
        'price': '24 990 ₽',
        'image': 'https://via.placeholder.com/200?text=XM4'
    }
}

def headphones_list(request):
    html = """
    <h1>🎧 Наушники — Выбери модель</h1>
    <p>Кликни по интересующей модели:</p>
    <div style="display: flex; gap: 20px; flex-wrap: wrap; margin: 20px 0;">
    """
    for key, data in HEADPHONES_DB.items():
        html += f"""
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; width: 250px; text-align: center;">
            <h3>{data['name']}</h3>
            <img src="{data['image']}" alt="{data['name']}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 8px;">
            <p><b>Год:</b> {data['year']}</p>
            <p><b>Цена:</b> <span style="color: #e74c3c;">{data['price']}</span></p>
            <a href="/headphones/{key}/" style="color: #3498db; text-decoration: none; font-weight: bold;">Подробнее →</a>
        </div>
        """
    html += """
    </div>
    <p><a href="/">← На главную</a></p>
    """
    return HttpResponse(html)


def headphone_detail(request, model):
    if model not in HEADPHONES_DB:
        return HttpResponse('<h1>❌ Модель не найдена</h1><p><a href="/headphones/">← Назад</a></p>', status=404)

    data = HEADPHONES_DB[model]
    html = f"""
    <h1>{data['name']}</h1>
    <img src="{data['image']}" alt="{data['name']}" style="width: 250px; border-radius: 10px; margin: 20px 0;">
    <p><b>Год выпуска:</b> {data['year']}</p>
    <p><b>Особенности:</b> {data['features']}</p>
    <p><b>Цена:</b> <span style="color: #e74c3c; font-size: 1.2em;">{data['price']}</span></p>
    <p><a href="/headphones/">← К списку</a> | <a href="/">На главную</a></p>
    """
    return HttpResponse(html)
