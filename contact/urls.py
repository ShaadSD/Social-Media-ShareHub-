from django.urls import path
from . import views
urlpatterns=[
    path('contact/',views.ContactUsViewset.as_view(),name='contact'),
]