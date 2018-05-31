from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index.html$', views.index, name='index'),
    url(r'^about.html$', views.about, name='about'),
    url(r'^publish_invitecode$', views.publish_invitecode, name='publish_invitecode'),
    url(r'^invitecode$', views.invitecode, name='invitecode'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register_api$', views.register_api, name='register_api'),
    url(r'^console$', views.console, name='console'),
    url(r'^create_machine$', views.create_machine, name='create_machine'),
]
