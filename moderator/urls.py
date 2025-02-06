# moderator/urls.py
from django.urls import path
from .views import ModView

urlpatterns = [
    path('xmlmod/', ModView.as_view(), name="mod_dashboard"),
]
