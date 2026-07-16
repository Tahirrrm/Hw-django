
from django.contrib import admin
from django.urls import path,include
from . import views  

urlpatterns = [
     

 path('admin/', admin.site.urls),

    # Главная
    path('', views.home, name='home'),

    # Отдельные приложения
    path('day/', include('day_of_week.urls')),
    path('headphones/', include('headphones.urls')),

    # Писатели
    path('writers/', views.writers_list, name='writers'),
    path('writers/<slug:slug>/', views.writer_detail, name='writer_detail'),
    path('writers/<slug:writer_slug>/<slug:book_slug>/', views.book_by_writer, name='book_by_writer'),

    # Книги
    path('books/', views.top_books, name='books'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),

    # День программиста и таблица умножения
    path('programmer/', views.programmer_day, name='programmer'),
    path('table/', views.multiplication_table, name='table'),

    # Приложение "Город"
    path('city/', views.city_app_home, name='city_home'),

    # Новости и управление — без slug
    path('news/', views.city_news, name='news'),
    path('management/', views.city_management, name='management'),
    path('facts/', views.city_facts, name='facts'),
    path('contacts/', views.city_contacts, name='contacts'),

    # История города
    path('history/', views.history_main, name='history_main'),
    path('history/people/', views.history_people, name='history_people'),
    path('history/photos/', views.history_photos, name='history_photos'),

    # Дополнительные slug-пути (если в будущем будут)
    # Например: /history/people/chapaev/
    path('history/people/<slug:slug>/', views.history_people, name='history_people_detail'),
    path('history/photos/<slug:slug>/', views.history_photos, name='history_photos_detail'),

    # Музыка
    path('song/', views.show_song, name='show_song'),
    path('song/en/', views.show_song, name='song_en'),  # передаём язык в view
    path('song/fr/', views.show_song_fr, name='song_fr'),
    path('song/de/', views.show_song_de, name='song_de'),
    path('song/es/', views.show_song_es, name='song_es'),

    # Автомобили
    path('cars/', views.cars_home, name='cars_home'),
    path('toyota/', views.show_toyota, name='toyota'),
    path('honda/', views.show_honda, name='honda'),
    path('renault/', views.show_renault, name='renault'),
]


#     path('admin/', admin.site.urls),
  
#     path('', views.home, name='home'),
#     path('day/', include('day_of_week.urls')),
#     path('headphones/', include('headphones.urls')),

#     path('writers/', views.writers_list, name='writers'),
#     path('writers/<str:slug>/', views.writer_detail, name='writer_detail'),
#     path('writers/<str:writer_slug>/<str:book_slug>/', views.book_by_writer, name='book_by_writer'),

#     path('books/', views.top_books, name='books'),
#     path('books/<int:book_id>/', views.book_detail, name='book_detail'),

#     path('programmer/', views.programmer_day, name='programmer'),
#     path('table/', views.multiplication_table, name='table'),
#     path('city/', views.city_app_home, name='city_home'),

#     path('history/', views.history_main, name='history'),
#     path('history/<str:slug>/', views.history_main, name='history_slug'),
    
#     path('history/people/', views.history_people, name='history_people'),
#     path('history/people/<str:slug>/', views.history_people, name='history_people_slug'),
    
#     path('history/photos/', views.history_photos, name='history_photos'),
#     path('history/photos/<str:slug>/', views.history_photos, name='history_photos_slug'),
    
#     path('news/', views.city_news, name='news'),
#     path('management/', views.city_management, name='management'),
#     path('management/<str:slug>/', views.city_management, name='management_slug'),
    
#     path('facts/', views.city_facts, name='facts'),
#     path('facts/<str:slug>/', views.city_facts, name='facts_slug'),
    
#     path('contacts/', views.city_contacts, name='contacts'),
#     path('contacts/<str:slug>/', views.city_contacts, name='contacts_slug'),
    
#     # фреймворки часть 4
#     path('song/', views.show_song, name='song'),
#     path('fr/', views.show_song_fr, name='song_fr'),
#     path('de/', views.show_song_de, name='song_de'),
#     path('es/', views.show_song_es, name='song_es'),

#     path('toyota/', views.show_toyota, name='toyota'),
#     path('honda/', views.show_honda, name='honda'),
#     path('renault/', views.show_renault, name='renault'),
#     path('cars/', views.cars_home, name='cars_home'),
    
# ]