from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']

        def create(self, validated_data):
            return Book.objects.create(**validated_data)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book.author.field.related_model
        fields = ['id', 'name']

   