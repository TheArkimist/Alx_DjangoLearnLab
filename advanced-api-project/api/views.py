from django.shortcuts import render
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer


# ListView for retrieving all books with advanced query capabilities
class BookListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Define fields for filtering
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Define fields for searching
    search_fields = ['title', 'author__name']

    # Define fields for ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


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
        serializer.save()


# UpdateView for modifying an existing book
class BookUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_update(self, serializer):
        # Custom logic before updating the book
        serializer.save()


# DeleteView for removing a book
class BookDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer