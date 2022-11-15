from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('testdata',views.TestDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('img-with-start-char', views.HelloWorld.as_view(), name='test-get'),
    path('histories', views.History.as_view(), name='history') # TODO: IDでASCソートして返す
]