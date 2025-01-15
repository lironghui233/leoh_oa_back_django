from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'absent'

router = DefaultRouter(trailing_slash=False)
router.register('absent', views.AbsentViewSet, basename='absent')

urlpatterns = [
    path('type', views.AbsentTypeView.as_view(), name='absenttypes'),
    path('responder', views.ResponderView.as_view(), name='getresponder'),
] + router.urls