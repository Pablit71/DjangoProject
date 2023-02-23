from rest_framework import serializers
from .models import Reader, Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author_serializer = AuthorSerializer(data=author_data)
        author_serializer.is_valid(raise_exception=True)
        author = author_serializer.save()
        book = Book.objects.create(author=author, **validated_data)
        return book


class ReaderSerializer(serializers.ModelSerializer):
    books = serializers.SlugRelatedField(queryset=Book.objects.all(), many=True, slug_field='title')

    class Meta:
        model = Reader
        fields = '__all__'

    def validate_books(self, books):
        if len(books) > 3:
            raise serializers.ValidationError("Читатель не может иметь более 3 книг")
        return books

    def validate_phone_number(self, phone_number):
        if len(phone_number) > 10:
            raise serializers.ValidationError("Номер телефона не может быть длиннее 10 цифр")
        return phone_number

    def validate(self, data):
        books = data.get('books')
        for book in books:
            if book.available_copies == 0:
                raise serializers.ValidationError(f"Книга '{book.title}' недоступна для добавления в библиотеку")
        return data
