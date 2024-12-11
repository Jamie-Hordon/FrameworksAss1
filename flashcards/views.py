from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status, viewsets
from .models import FlashcardSet, Flashcard
from .serializers import FlashcardSetSerializer, FlashcardSerializer
from django.utils.timezone import now
from rest_framework.response import Response
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import random


def index(request):
    flashcard_sets = FlashcardSet.objects.all()
    return render(request, 'index.html', {'flashcard_sets': flashcard_sets})

@api_view(['GET'])
def get_version(request):
    return Response({"version": "1.0.0"})
    
@csrf_exempt # This is sketchy but i dont want to deal with it :P
def create_flashcard(request):
    if request.method == 'POST':
        set_id = request.POST.get('set_id')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        
        # Find the set
        flashcard_set = FlashcardSet.objects.get(id=set_id)
        
        # Create the new flashcard
        flashcard = Flashcard.objects.create(
            set=flashcard_set,
            question=question,
            answer=answer
        )

        # Return a success response
        return JsonResponse({
            'success': True,
            'flashcard': {
                'question': flashcard.question,
                'answer': flashcard.answer,
            }
        }, status=201)

    return JsonResponse({'success': False})

def get_flashcard_sets(request):
    if request.method == "GET":
        sets = FlashcardSet.objects.all().values("id", "name", "created_at")
        return JsonResponse(list(sets), safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            if not name:
                return JsonResponse({"error": "Name is required"}, status=400)

            new_set = FlashcardSet.objects.create(name=name)
            return JsonResponse({
                "id": new_set.id,
                "name": new_set.name,
                "created_at": new_set.created_at,
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        

def play_flashcard(request):
    # Get all flashcard sets for the dropdown
    flashcard_sets = FlashcardSet.objects.all()

    if request.method == 'POST':
        # Get the selected set
        set_id = request.POST.get('set_id')

        # Ensure a set was selected
        if set_id:
            flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
            flashcards = flashcard_set.flashcards.all()  # Assuming 'flashcards' is the related name
            
            # Check if there are any flashcards in the selected set
            if not flashcards:
                # If no flashcards, notify the user and let them pick another set
                return render(request, 'play_flashcard.html', {
                    'flashcard_sets': flashcard_sets,
                    'flashcard_set': flashcard_set,
                    'message': "This set has no flashcards. Please choose another set. Or add some in the Sets page"
                })

            # User input handler
            if 'answer' in request.POST:
                user_answer = request.POST.get('answer').strip()
                flashcard_id = request.POST.get('flashcard_id')
                flashcard = get_object_or_404(Flashcard, id=flashcard_id)
                is_correct = user_answer.lower() == flashcard.answer.lower()

                # Return the current flashcard with the result (correct or wrong)
                return render(request, 'play_flashcard.html', {
                    'flashcard_sets': flashcard_sets,
                    'flashcard': flashcard,
                    'is_correct': is_correct,
                    'user_answer': user_answer,
                    'flashcard_set': flashcard_set,
                })
            
            # Pick a random flashcard if no answer submitted yet
            flashcard = random.choice(flashcards)

            # Show the flashcard without feedback
            return render(request, 'play_flashcard.html', {
                'flashcard_sets': flashcard_sets,
                'flashcard': flashcard,
                'flashcard_set': flashcard_set,
            })

    # Just show the dropdown if no flashcard selected yet
    return render(request, 'play_flashcard.html', {
        'flashcard_sets': flashcard_sets,
    })


class FlashcardSetViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing flashcard sets.
    """
    queryset = FlashcardSet.objects.all()
    serializer_class = FlashcardSetSerializer

    def create(self, request, *args, **kwargs):
        # Debugging output to ensure this method is triggered
        print("Create method triggered")
        
        # Get today's date
        today = now().date()

        # Count flashcard sets created today
        daily_count = FlashcardSet.objects.filter(created_at__date=today).count()

        print(f"Daily count: {daily_count}")

        # Enforce the limit
        if daily_count <= 20:
            print("Creating a new flashcard set.")  # Debug message
            return super().create(request, *args, **kwargs)
        else:
            print("Daily limit reached.")  # Debug message
            return Response(
                {'error': 'Daily limit of 20 flashcard sets reached.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class FlashcardViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing flashcards.
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
