from rest_framework import serializers
from .models import Reader, Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author_first_name, author_last_name = author_data.split(" ")
        author, created = Author.objects.get_or_create(
            first_name=author_first_name,
            last_name=author_last_name
        )
        validated_data['author'] = author
        return super().create(validated_data)


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
