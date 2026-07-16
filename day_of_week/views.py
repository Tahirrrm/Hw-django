from django.shortcuts import render
from datetime import date

def today(request):
  
    
    DAYS = {
        0: ("Понедельник", "linear-gradient(135deg, #ff6b6b, #ee5a52)"),
        1: ("Вторник", "linear-gradient(135deg, #4ecdc4, #44a08d)"),
        2: ("Среда", "linear-gradient(135deg, #45b7d1, #96c93d)"),
        3: ("Четверг", "linear-gradient(135deg, #96ceb4, #8aa62b)"),
        4: ("Пятница", "linear-gradient(135deg, #feca57, #ff9ff3)"),
        5: ("Суббота", "linear-gradient(135deg, #ff9ff3, #54a0ff)"),
        6: ("Воскресенье", "linear-gradient(135deg, #5f27cd, #341f97)")
    }
    
    today_weekday = date.today().weekday()
    day_name, background = DAYS[today_weekday]
    
    return render(request, 'day_of_week/day_of_week.html', {
        'day_name': day_name,
        'background': background
    })