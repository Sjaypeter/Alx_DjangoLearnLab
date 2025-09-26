from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        
        # Create sample book
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            publication_year=2020
        )

    def test_create_book(self):
        data = {"title": "New Book", "author": "Jane Doe", "publication_year": 2023}
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_books_list(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_books_by_author(self):
        response = self.client.get("/api/books/?author=John Doe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author'], "John Doe")

    def test_update_book(self):
        data = {"title": "Updated Title", "author": "John Doe", "publication_year": 2019}
        response = self.client.put(f"/api/books/{self.book.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)