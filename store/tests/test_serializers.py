from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name='Test_book_1', price='500.00', description='')
        book_2 = Book.objects.create(name='Test_book_2', price='600.00', description='')
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test_book_1',
                'price': '500.00',
                'description': '',
            },
            {
                'id': book_2.id,
                'name': 'Test_book_2',
                'price': '600.00',
                'description': '',
            },
        ]
        self.assertEqual(expected_data, data)
