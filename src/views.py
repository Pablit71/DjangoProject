from django.shortcuts import render
from rest_framework import generics, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from src.models import Author, Reader, Book
from src.serializers import ReaderSerializer, BookSerializer, AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
