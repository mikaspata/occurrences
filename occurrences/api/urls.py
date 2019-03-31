from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^occurences/$', views.OccurenceView.as_view()),
    url(r'^occurences/(?P<pk>[0-9]+)/$', views.OccurenceDetail.as_view()),
]