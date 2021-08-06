from django.contrib import admin
from django.urls import path
from api.views import AccViews, LoginView

urlpatterns = [
    path('accounts/', AccViews.as_view()),
    path('login/', LoginView.as_view())
]