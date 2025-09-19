from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('home/', views.home, name='home'),
    path('deposit/', views.deposit, name='deposit'),
    path('deposit/submit/', views.deposit_submit, name='deposit_submit'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('withdraw/submit/', views.withdraw_submit, name='withdraw_submit'),
    path('match/submit/', views.bet_submit, name='bet_submit'),
    path('match/<int:id>/', views.matchs, name='matchs'),
    path('match/<int:id>/live/', views.live_score_api, name='live_score_api'),
    path('activeBets/', views.activeBets, name='activeBets'),
    path('settledBets/', views.settledBets, name='settledBets'),
]
