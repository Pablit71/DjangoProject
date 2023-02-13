from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    page_count = models.PositiveIntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    available_copies = models.PositiveIntegerField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Reader(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    books = models.ManyToManyField(Book, through='ReaderBook', related_name='readers')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ReaderBook(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_borrowed = models.DateField(auto_now_add=True)
    date_returned = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if the reader has already borrowed 3 books
        if self.reader.books.count() >= 3:
            raise ValueError('Reader can borrow only 3 books at a time')
        # Check if the book is available in the library
        if self.book.available_copies <= 0:
            raise ValueError('Book is not available in the library')
        self.book.available_copies -= 1
        self.book.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.book.available_copies += 1
        self.book.save()
