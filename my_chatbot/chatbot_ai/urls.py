from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),             # For the 'index.html' template
    path('account/', views.account, name='account'), # For the 'account.html' template
    path('chat/', views.chat, name='chat'),   # For the 'chat.html' template

    # Add other paths as needed...
]
