from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer


# ListView for retrieving all books
class BookListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'author__name']  # Enable search by title or author name
    ordering_fields = ['publication_year', 'title']  # Enable ordering by year or title


# DetailView for retrieving a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# CreateView for adding a new book
class BookCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        # Custom logic before saving the book
        # For example, you can add the current user as the creator of the book
        serializer.save()  # Save the book instance


# UpdateView for modifying an existing book
class BookUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_update(self, serializer):
        # Custom logic before updating the book
        # For example, you can log the update or modify data before saving
        serializer.save()  # Save the updated book instance


# DeleteView for removing a book
class BookDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer