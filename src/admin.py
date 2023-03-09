from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from src.models import Book, Reader, Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'photo', 'date_create', 'date_update')
    list_filter = ('date_create', 'date_update')


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'page_count', 'author_link', 'available_copies', 'date_create', 'date_update')
    list_filter = ('author', 'available_copies', 'date_create', 'date_update')

    def author_link(self, obj):
        url = reverse('admin:src_author_change', args=[obj.author_id])
        return format_html("<a href='{}'>{}</a>", url, obj.author)

    def make_book_unavailable(self, request, queryset):
        queryset.update(available_copies=0)

    make_book_unavailable.short_description = "Отметить выбранные книги как недоступные"

    actions = [make_book_unavailable]


class ReaderAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone_number', 'is_active', 'date_update')
    list_filter = ('is_active', 'date_update')
    list_display_links = ('phone_number',)

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Активировать выбранных читателей"

    # экшен для изменения статуса неактивности читателя
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Деактивировать выбранных читателей"

    def delete_all_books(self, request, queryset):
        for obj in queryset:
            obj.books.clear()

    delete_all_books.short_description = "Удалить все книги у выбранных пользователей"

    actions = [make_active, make_inactive, delete_all_books]


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Reader, ReaderAdmin)
