from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('img-with-start-char', views.ImgWithStartChar.as_view(), name='img-with-start-char'),
    path('histories', views.History.as_view(), name='history') # TODO: IDでASCソートして返す
]