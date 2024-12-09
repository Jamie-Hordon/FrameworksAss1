from django.db import models
from django.utils.timezone import now

class FlashcardSet(models.Model):
    name = models.CharField(max_length=100)  # Name of the flashcard set
    description = models.TextField()  # Brief description of the set
    created_at = models.DateTimeField(default=now)  # Timestamp when created

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        print("Custom save method triggered")
        today = now().date()
        daily_count = FlashcardSet.objects.filter(created_at__date=today).count()
        
        if daily_count >= 20:
            raise ValueError("Daily limit of 20 flashcard sets reached.")
        
        super().save(*args, **kwargs)

class Flashcard(models.Model):
    set = models.ForeignKey(
        FlashcardSet, on_delete=models.CASCADE, related_name='cards'
    )  # Links a card to a set
    question = models.TextField()  # Question on the card
    answer = models.TextField()  # Answer on the card
    created_at = models.DateTimeField(default=now)  # Timestamp when created

    def __str__(self):
        return self.question