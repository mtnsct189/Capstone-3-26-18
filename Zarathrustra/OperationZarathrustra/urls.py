from django.urls import path

from . import views

app_name = "OZ"
urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', views.logout, {'next_page': 'login'}, name='logout'),
    path('signup/', views.signup, name='signup'),

]
