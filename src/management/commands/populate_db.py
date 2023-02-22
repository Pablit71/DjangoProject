from django.core.management.base import BaseCommand
from src.models import Author, Book, Reader
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int, default=10, help='Number of authors to create')
        parser.add_argument('--books', type=int, default=20, help='Number of books to create')
        parser.add_argument('--readers', type=int, default=10, help='Number of readers to create')

    def handle(self, *args, **options):
        fake = Faker()

        # create authors
        authors = []
        for i in range(options['authors']):
            author = Author(first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            photo='photos/{}'.format(random.choice(['author1.jpg', 'author2.jpg', 'author3.jpg'])))
            authors.append(author)

        Author.objects.bulk_create(authors)

        # create books
        books = []
        for i in range(options['books']):
            author = random.choice(authors)
            book = Book(title=fake.sentence(nb_words=6),
                        description=fake.paragraph(),
                        page_count=random.randint(100, 1000),
                        author=author,
                        available_copies=random.randint(1, 10))
            books.append(book)

        Book.objects.bulk_create(books)

        # create readers
        readers = []
        for i in range(options['readers']):
            reader = Reader(first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            phone_number='89{}'.format(fake.msisdn()[3:]))
            reader.save()

            # add books to reader
            books = list(Book.objects.order_by('?')[:random.randint(0, 3)])
            for book in books:
                reader.books.add(book)

            readers.append(reader)

        Reader.objects.bulk_create(readers)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
