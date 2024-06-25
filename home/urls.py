from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("contact/", views.contact_page, name='contactus'),
    path("faq/", views.faq_page, name='faq'),
    path("privacy/", views.privacy_page, name='privacy'),
]
