import logging

from typing import TYPE_CHECKING

from django.urls import path
from django.contrib.auth import views as auth_views

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

app_name = 'accounts'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
