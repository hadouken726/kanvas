from django.contrib import admin
from django.urls import path
from api.views import AccViews, LoginView, CourseView, ActivityView, SubmissionView

urlpatterns = [
    path('accounts/', AccViews.as_view()),
    path('login/', LoginView.as_view()),
    path('courses/', CourseView.as_view()),
    path('courses/<int:course_id>/', CourseView.as_view()),
    path('courses/<int:course_id>/registrations/', CourseView.as_view()),
    path('activities/', ActivityView.as_view()),
    path('activities/<int:activity_id>/submissions/', SubmissionView.as_view()),
    path('submissions/<int:submission_id>/', SubmissionView.as_view()),
    path('submissions/', SubmissionView.as_view())
]