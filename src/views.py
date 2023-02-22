from django.shortcuts import render
from rest_framework import generics, serializers

from src.models import Author, Reader, Book
from src.serializers import ReaderSerializer, BookSerializer, AuthorSerializer


class ReaderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer

    def perform_create(self, serializer):
        max_books = 3
        books = self.request.data.get('books', [])
        if len(books) > max_books:
            raise serializers.ValidationError(f'Maximum {max_books} books allowed.')
        serializer.save()


class ReaderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ReaderListAPIView(generics.ListAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer

    def get(self, request, *args, **kwargs):
        readers = self.get_queryset()
        return render(request, 'reader_list.html', {'readers': readers})
