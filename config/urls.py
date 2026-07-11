
from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    path('admin/', admin.site.urls),
  
    path('', views.home, name='home'),

    path('writers/', views.writers_list, name='writers'),
    path('writers/<str:slug>/', views.writer_detail, name='writer_detail'),
    path('writers/<str:writer_slug>/<str:book_slug>/', views.book_by_writer, name='book_by_writer'),

    path('books/', views.top_books, name='books'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),

    path('programmer/', views.programmer_day, name='programmer'),
    path('table/', views.multiplication_table, name='table'),
    path('city/', views.city_app_home, name='city_home'),

    path('history/', views.history_main, name='history'),
    path('history/<str:slug>/', views.history_main, name='history_slug'),
    
    path('history/people/', views.history_people, name='history_people'),
    path('history/people/<str:slug>/', views.history_people, name='history_people_slug'),
    
    path('history/photos/', views.history_photos, name='history_photos'),
    path('history/photos/<str:slug>/', views.history_photos, name='history_photos_slug'),
    
    path('news/', views.city_news, name='news'),
    path('management/', views.city_management, name='management'),
    path('management/<str:slug>/', views.city_management, name='management_slug'),
    
    path('facts/', views.city_facts, name='facts'),
    path('facts/<str:slug>/', views.city_facts, name='facts_slug'),
    
    path('contacts/', views.city_contacts, name='contacts'),
    path('contacts/<str:slug>/', views.city_contacts, name='contacts_slug'),
   
]