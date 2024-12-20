"""
URL configuration for testvar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.views import serve
from django.urls import path
from flashcards import views
from django.http import HttpResponse
from . import views as tvviews

def index(request):
    return HttpResponse("Welcome to the Flashcard App!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('flashcards.urls')),
    path('', views.index, name='index'),
    path("new_card/", views.create_flashcard, name='create_flashcard'), # Create new card
    path('sets/new/', tvviews.new_flashcard_set, name='new_set'),  # Create new set
    path('sets/', tvviews.flashcard_set_list, name='flashcard_set_list'),
    path('sets/<int:set_id>/flashcards/', tvviews.flashcard_set_flashcards_view, name='flashcard_set_flashcards_view'),
    path('play/', views.play_flashcard, name='play_flashcard'),
]
