from django.test import TestCase
from . import models
from django.urls import reverse
from rest_framework.test import APIClient
from flashcards.models import FlashcardSet, Flashcard
from django.utils.timezone import now


# Create your tests here.

class FlashcardSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.set1 = FlashcardSet.objects.create(name="Set 1", description="Description 1")
        self.set2 = FlashcardSet.objects.create(name="Set 2", description="Description 2")

    def test_get_flashcard_sets(self):
        """Test retrieving all flashcard sets."""
        response = self.client.get(reverse('get_flashcard_sets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Set 1")

    def test_flashcard_set_creation(self):
        """Ensure flashcard sets are created correctly."""
        self.assertEqual(FlashcardSet.objects.count(), 2)
        self.assertEqual(self.set1.name, "Set 1")
        self.assertEqual(self.set2.description, "Description 2")

    def test_flashcard_set_str(self):
        """Test string representation of a flashcard set."""
        self.assertEqual(str(self.set1), "Set 1")

    def test_flashcard_set_exists(self):
        """Check if a flashcard set exists by name."""
        exists = FlashcardSet.objects.filter(name="Set 1").exists()
        self.assertTrue(exists)

    def test_flashcard_set_does_not_exist(self):
        """Check that a non-existent flashcard set does not exist."""
        exists = FlashcardSet.objects.filter(name="Nonexistent").exists()
        self.assertFalse(exists)

    def test_flashcard_set_update(self):
        """Test updating a flashcard set's name."""
        self.set1.name = "Updated Set"
        self.set1.save()
        self.assertEqual(self.set1.name, "Updated Set")


class FlashcardAPITests(TestCase):
    def setUp(self):
        self.set = FlashcardSet.objects.create(name="Set 1", description="Description 1")

    def test_create_flashcard(self):
        """Test creating a new flashcard."""
        data = {
            "set_id": self.set.id,
            "question": "What is Django?",
            "answer": "A Python web framework."
        }
        response = self.client.post(reverse('create_flashcard'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Flashcard.objects.count(), 1)


class EmptyFlashcardSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_flashcard_sets_empty(self):
        """Test retrieving flashcard sets when none exist."""
        response = self.client.get(reverse('get_flashcard_sets'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class APIDocumentationTests(TestCase):
    def test_api_version_endpoint(self):
        """Test the API version endpoint."""
        response = self.client.get(reverse('get_version'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("version", response.json())


class URLReverseTests(TestCase):
    def test_reverse_get_version(self):
        """Test reverse URL for API version."""
        url = reverse('get_version')
        self.assertEqual(url, '/api/version/')

    def test_reverse_get_flashcard_sets(self):
        """Test reverse URL for retrieving flashcard sets."""
        url = reverse('get_flashcard_sets')
        self.assertEqual(url, '/api/sets/')