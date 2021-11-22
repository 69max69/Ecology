from django.urls import path, include

from .views import *

urlpatterns = [
    path('', start_page, name='start_page'),
    path('view_branch/', view_branch),
    path('view_objects/', view_objects),
    path('register/', register, name='register'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('add_educated_waste/', add_educated_waste, name='add_educated_waste'),
    path('add_educated_waste1/', add_educated_waste1, name='add_educated_waste1'),
    path('add_reclaimed_waste/', add_reclaimed_waste, name='add_reclaimed_waste'),
    path('add_reclaimed_waste1/', add_reclaimed_waste1, name='add_reclaimed_waste1'),
    path('add_transferred_waste/', add_transferred_waste, name='add_transferred_waste'),
    path('add_transferred_waste1/', add_transferred_waste1, name='add_transferred_waste1'),
    path('view_waste_motion/', view_waste_motion, name='view_waste_motion'),
    path('create_report/', create_report, name='create_report'),
    path('month_report/', month_report, name='month_report'),
    path('quater_report/', quater_report, name='quater_report'),
    path('year_report/', year_report, name='year_report'),
    path('remove_motion/<str:atribute>/', remove_motion, name='remove_motion'),
    path('reports/', report, name='reports'),
    path('remove_report/<int:pk>/', remove_report, name='remove_report'),
    path('sort_waste_motion/', sort_waste_motion, name='sort_waste_motion'),
    path("auth/", include("django.contrib.auth.urls")),

]