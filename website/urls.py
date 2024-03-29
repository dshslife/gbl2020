from django.urls import path, include

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('login', views.test, name='test'),
  path('bingo', views.bingo, name='bingo'),
  path('profile', views.profile, name='profile'),
  path('information', views.information, name='information'),
  path('logout', views.logout, name="logout"),
  path('webpush/', include('webpush.urls')),
  path('map', views.map, name='map'),
  path('booth', views.BoothCheck.as_view(), name='booth'),
  path('booth/<slug:id>', views.BoothInfo, name='detail'),
  path('push', views.WebPush.as_view(), name='webpush'),
  path('api/list', views.BoothList.as_view(), name='boothlist'),
  path('api/set', views.setBoothBusy.as_view(), name='setBoothBusy')
]