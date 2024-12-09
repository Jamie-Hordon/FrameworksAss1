from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status, viewsets
from .models import FlashcardSet, Flashcard
from .models import FlashcardSet
from .serializers import FlashcardSetSerializer, FlashcardSerializer
from django.utils.timezone import now
from rest_framework.response import Response
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404

def index(request):
    flashcard_sets = FlashcardSet.objects.all()
    return render(request, 'index.html', {'flashcard_sets': flashcard_sets})


@api_view(['GET'])
def get_version(request):
    return Response({"version": "1.0.0"})


@api_view(['GET'])
def get_flashcard_sets(request):
    flashcard_sets = FlashcardSet.objects.all()
    serializer = FlashcardSetSerializer(flashcard_sets, many=True)
    return Response(serializer.data)

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
