from django.shortcuts import render, redirect
from flashcards.models import FlashcardSet, Flashcard
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import now
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    # Get all flashcard sets from the database
    flashcard_sets = FlashcardSet.objects.all()

    def index(request):
        flashcard_sets = FlashcardSet.objects.all()  # Fetch all flashcard sets (example)
        return render(request, 'index.html', {'flashcard_sets': flashcard_sets})
    
def new_flashcard(request):
    if request.method == "POST":
        set_id = request.POST.get("set_id")
        question = request.POST.get("question")
        answer = request.POST.get("answer")

        flashcard_set = FlashcardSet.objects.get(id=set_id)
        Flashcard.objects.create(flashcard_set=flashcard_set, question=question, answer=answer, created_at=now )
        return redirect(f"/sets/{set_id}/flashcards/")
    
    
@csrf_exempt # This is sketchy but i dont want to deal with it :P
def new_flashcard_set(request):
    if request.method == "POST":
        # Get the submitted data
        set_name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        time = now().date()

        if set_name:  # Ensure a name is provided
            # Save the new flashcard set
            FlashcardSet.objects.create(name=set_name, description=description, created_at = time)
            return redirect('flashcard_set_list')  # Redirect to the flashcard set list
        
        return HttpResponse("Name is required", status=400)

    # Render the form if the request is GET
    return render(request, 'new_set.html')

def flashcard_set_list(request):
    flashcard_sets = FlashcardSet.objects.all() # Fetches all flashcard sets
    return render(request, 'flashcard_set_list.html', {'flashcard_sets': flashcard_sets})

def flashcard_sets_view(request):
    # Get all flashcard sets and their related flashcards
    flashcard_sets = FlashcardSet.objects.prefetch_related('flashcards').all()

    # Pass the flashcard sets to the template
    return render(request, 'flashcard_set_list.html', {'flashcard_sets': flashcard_sets})

def flashcard_set_flashcards_view(request, set_id):
    # Get the flashcard set or return 404 if not found
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)

    # Get the flashcards related to this set
    flashcards = flashcard_set.flashcards.all().values('question', 'answer')

    # Return the flashcards as JSON
    return JsonResponse(list(flashcards), safe=False)