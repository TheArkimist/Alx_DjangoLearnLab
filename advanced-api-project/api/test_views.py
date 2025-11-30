# api/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from api.models import Book


class BookAPITestCase(APITestCase):
    """
    Test suite for CRUD operations and list/search/filter functionalities
    for the Book API endpoints.
    """

    def setUp(self):
        # Create user for authenticated routes
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        # Create some sample book objects
        self.book1 = Book.objects.create(
            title="Django for Beginners",
            author="William S.",
            description="Introductory Django book",
            price=10
        )

        self.book2 = Book.objects.create(
            title="Advanced Django",
            author="John D.",
            description="Advanced concepts",
            price=20
        )

        # Login user and get auth token if needed
        self.client.login(username="testuser", password="password123")

    # ---------------------------------------------------------
    # TEST LIST VIEW
    # ---------------------------------------------------------
    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ---------------------------------------------------------
    # TEST DETAIL VIEW
    # ---------------------------------------------------------
    def test_retrieve_single_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    # ---------------------------------------------------------
    # TEST CREATE
    # ---------------------------------------------------------
    def test_create_book(self):
        url = reverse("book-list")
        payload = {
            "title": "New Book",
            "author": "Author Y",
            "description": "Some description",
            "price": 15
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "New Book")

    # ---------------------------------------------------------
    # TEST UPDATE
    # ---------------------------------------------------------
    def test_update_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        payload = {
            "title": "Django for Pros",
            "author": self.book1.author,
            "description": self.book1.description,
            "price": 12
        }

        response = self.client.put(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_book = Book.objects.get(id=self.book1.id)
        self.assertEqual(updated_book.title, "Django for Pros")
        self.assertEqual(updated_book.price, 12)

    # ---------------------------------------------------------
    # TEST DELETE
    # ---------------------------------------------------------
    def test_delete_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ---------------------------------------------------------
    # TEST SEARCH
    # ---------------------------------------------------------
    def test_search_books(self):
        url = reverse("book-list") + "?search=Django"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2 books contain "Django"
        self.assertEqual(len(response.data), 2)

    # ---------------------------------------------------------
    # TEST FILTERING (price filter example)
    # ---------------------------------------------------------
    def test_filter_books_by_price(self):
        url = reverse("book-list") + "?price=20"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only book2 has price=20
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Advanced Django")

    # ---------------------------------------------------------
    # TEST ORDERING (order by price)
    # ---------------------------------------------------------
    def test_order_books_by_price(self):
        url = reverse("book-list") + "?ordering=price"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        prices = [item["price"] for item in response.data]
        self.assertEqual(prices, sorted(prices))

    # ---------------------------------------------------------
    # TEST PERMISSIONS
    # ---------------------------------------------------------
    def test_permission_denied_for_unauthenticated_user(self):
        self.client.logout()

        url = reverse("book-list")
        payload = {
            "title": "Should Fail",
            "author": "X",
            "price": 10
        }

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
