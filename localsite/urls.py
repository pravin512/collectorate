from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adhikari_list/<slug:meeting_type>', views.adhikari_list, name='adhikari_list'),
    path('meeting_list/<int:adhikari_id>', views.meeting_list, name='meeting_list'),
    path('import_meeting/', views.import_meeting, name='import_meeting'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
]