from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from src.models import Author, Reader, Book
from src.permissions import PermissionPolicyMixin, PermissionReader
from src.serializers import ReaderSerializer, BookSerializer, AuthorSerializer


class AuthorViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
        'retrieve': [AllowAny]
    }


class BookViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
        'retrieve': [AllowAny]
    }


class ReaderViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    permission_classes_per_method = {
        'list': [IsAdminUser],
        'create': [AllowAny],
        'update': [PermissionReader],
        'destroy': [PermissionReader],
        'retrieve': [PermissionReader]
    }
