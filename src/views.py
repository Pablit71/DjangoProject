from django.shortcuts import render
from rest_framework import generics

from src.models import Author, Reader, Book
from src.serializers import ReaderSerializer, BookSerializer, AuthorSerializer


class ReaderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer


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
