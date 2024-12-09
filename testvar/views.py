from django.shortcuts import render
from flashcards.models import FlashcardSet

def index(request):
    # Get all flashcard sets from the database
    flashcard_sets = FlashcardSet.objects.all()

    def index(request):
        flashcard_sets = FlashcardSet.objects.all()  # Fetch all flashcard sets (example)
        return render(request, 'index.html', {'flashcard_sets': flashcard_sets})