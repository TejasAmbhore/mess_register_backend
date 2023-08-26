from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'checkin', CheckInViewSet, basename='checkin')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('login/', login_view, name='login'),

]