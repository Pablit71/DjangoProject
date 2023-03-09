from rest_framework import serializers

from .models import Reader, Book, Author


class PageCountValidator:
    def __call__(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество страниц не может быть отрицательным")


class PhoneNumberValidator:
    def __call__(self, value):
        phone_number = str(value)
        if not phone_number.startswith("7"):
            raise serializers.ValidationError("Номер телефона должен начинаться с 7")
        if len(phone_number) != 11:
            raise serializers.ValidationError("Номер телефона должен содержать 11 цифр")
        if not phone_number.isdigit():
            raise serializers.ValidationError("Номер телефона должен содержать только цифры")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    page_count = serializers.IntegerField(validators=[PageCountValidator()])

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

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        author_first_name, author_last_name = author_data.split(" ")
        author, created = Author.objects.get_or_create(
            first_name=author_first_name,
            last_name=author_last_name
        )
        instance.author = author
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.page_count = validated_data.get('page_count', instance.page_count)
        instance.available_copies = validated_data.get('available_copies', instance.available_copies)
        instance.save()
        return instance


class ReaderSerializer(serializers.ModelSerializer):
    books = serializers.SlugRelatedField(queryset=Book.objects.all(), many=True, slug_field='title')
    phone_number = serializers.CharField(validators=[PhoneNumberValidator()])

    class Meta:
        model = Reader
        fields = '__all__'

    def validate_books(self, books):
        if len(books) > 3:
            raise serializers.ValidationError("Читатель не может иметь более 3 книг")
        return books

    def validate(self, data):
        books = data.get('books')
        for book in books:
            if book.available_copies == 0:
                raise serializers.ValidationError(f"Книга '{book.title}' недоступна для добавления в библиотеку")
        return data

    def create(self, validated_data):
        books = validated_data.pop('books', [])
        reader = super().create(validated_data)
        for book in books:
            book.available_copies -= 1
            book.save()
            reader.books.add(book)
        reader.set_password(reader.password)
        reader.save()
        return reader

    def update(self, instance, validated_data):
        books = validated_data.pop('books', [])
        reader = super().update(instance, validated_data)
        reader.set_password(reader.password)

        # Получаем уникальный набор книг
        new_books = set(books)
        old_books = set(instance.books.all())

        # Обновляем количество доступных копий для каждой книги
        for book in old_books - new_books:
            book.available_copies += 1
            book.save()

        for book in new_books - old_books:
            book.available_copies -= 1
            book.save()

        # Добавляем новые книги
        for book in new_books - old_books:
            instance.books.add(book)

        # Удаляем старые книги
        for book in old_books - new_books:
            instance.books.remove(book)

        reader.save()
        return reader
