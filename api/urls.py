from django.contrib import admin
from django.urls import path
from api.views import AccViews, LoginView, CourseView

urlpatterns = [
    path('accounts/', AccViews.as_view()),
    path('login/', LoginView.as_view()),
    path('courses/', CourseView.as_view()),
    path('courses/<int:course_id>/', CourseView.as_view()),
    path('courses/<int:course_id>/registrations/', CourseView.as_view()),
]