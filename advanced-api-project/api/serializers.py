from rest_framework import serializers
from .models import Book
from datetime import datetime
from .models import Author
from .serializers import AuthorSerializer

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

