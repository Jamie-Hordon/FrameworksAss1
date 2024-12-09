from rest_framework import serializers
from .models import FlashcardSet, Flashcard

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = '__all__'

class FlashcardSetSerializer(serializers.ModelSerializer):
    flashcards = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source='flashcard_set'
    )

    class Meta:
        model = FlashcardSet
        fields = '__all__'