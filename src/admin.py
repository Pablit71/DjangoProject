from django.contrib import admin

from src.models import Book, Reader, Author

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Reader)
