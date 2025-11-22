from rest_framework import generics
from .serializers import BookSerializer
from .models import Book
from rest_framework import viewsets

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
