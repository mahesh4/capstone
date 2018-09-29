from django.conf.urls import url,patterns,include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    url(r'^nash', csrf_exempt(views.nash), name='nash'),
    url(r'^signin',views.signin,name='signin'),
    url(r'^sensor', csrf_exempt(views.sensor), name='sensor'),  
    url(r'^data', csrf_exempt(views.data), name='data'),
    url(r'^signout',views.signout,name='signout'),
    url(r'^$', views.index, name='index'),
]
