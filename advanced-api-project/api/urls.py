from django.urls import path
from .views import BookListView
from .views import BookCreateView, BookDetailView, BookUpdateView, BookDeleteView

urlpatterns = [
   path('books/list', BookListView.as_view(), name='book-list'),
   path('books/create/', BookCreateView.as_view(), name='book-list'),
   path('books/update/', BookUpdateView.as_view(), name='book-list'),
   path('books/delete/', BookDeleteView.as_view(), name='book-list'),
]