from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone


def home(request):
    time_now = timezone.now()
    formatted_time = time_now.strftime("%d.%m.%Y %H:%M:%S")
    return HttpResponse(f"Текущая дата и время: {formatted_time}")

def multiplication_table(request):
    table = []
    for i in range(1, 11):
        row = [i * j for j in range(1, 11)]
        table.append((i, row))

    context = {'table': table}
    return render(request, 'multiplication/multiplication_table.html', context)
    
    