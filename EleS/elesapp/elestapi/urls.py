from django.urls import path
from .views import start_page, signin, group_list, all_group_dischip_list, create_teacher, set_mark_for_gr, delete_teacher


urlpatterns = [
    path('', start_page), #Стартовая страница и страница авторизации;
    path('home_page', signin), #Главная страница;
    path('group_list', group_list), #Список группы;
    path('diship_list', all_group_dischip_list), #Список дисциплин;
    path('create_teacher', create_teacher), #Создать преподавателя;
    path('set_mark', set_mark_for_gr), #Оценки;
    path('delete_teacher', delete_teacher), #Создать преподавателя;
]

