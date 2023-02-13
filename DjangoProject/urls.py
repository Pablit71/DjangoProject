"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .yasg import urlpatterns as swagger

from src.views import ReaderListCreateAPIView, ReaderRetrieveUpdateDestroyAPIView, BookListCreateAPIView, \
    BookRetrieveUpdateDestroyAPIView, AuthorListCreateAPIView, AuthorRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('readers/', ReaderListCreateAPIView.as_view(), name='reader_list_create'),
    path('readers/int:pk/', ReaderRetrieveUpdateDestroyAPIView.as_view(), name='reader_retrieve_update_destroy'),
    path('books/', BookListCreateAPIView.as_view(), name='book_list_create'),
    path('books/int:pk/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book_retrieve_update_destroy'),
    path('authors/', AuthorListCreateAPIView.as_view(), name='author_list_create'),
    path('authors/int:pk/', AuthorRetrieveUpdateDestroyAPIView.as_view(), name='author_retrieve_update_destroy'),
]

urlpatterns += swagger
