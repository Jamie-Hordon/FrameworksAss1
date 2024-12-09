from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlashcardSetViewSet, FlashcardViewSet
from . import views

router = DefaultRouter()
router.register(r'flashcard-sets', FlashcardSetViewSet)
router.register(r'flashcards', FlashcardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('version/', views.get_version, name='get_version'),
    path('sets/', views.get_flashcard_sets, name='get_flashcard_sets'),
    path('sets/<str:fcname>', views.get_flashcard_sets, name='get_flashcard_set')
]
