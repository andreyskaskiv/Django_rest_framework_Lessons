from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username_Serializer')

        self.book_1 = Book.objects.create(name='Test book 1', price=500,
                                          author_name='Author 1', description='',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=777,
                                          author_name='Author 5', description='',
                                          owner=self.user)
        self.book_3 = Book.objects.create(name='Test book Author 1', price=777,
                                          author_name='Author 2', description='',
                                          owner=self.user)

    def test_ok(self):
        data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'Test book 1',
                'price': '500.00',
                'author_name': 'Author 1',
                'description': '',
                'owner': self.book_1.owner_id,
            },
            {
                'id': self.book_2.id,
                'name': 'Test book 2',
                'price': '777.00',
                'author_name': 'Author 5',
                'description': '',
                'owner': self.book_1.owner_id,
            },
            {
                'id': self.book_3.id,
                'name': 'Test book Author 1',
                'price': '777.00',
                'author_name': 'Author 2',
                'description': '',
                'owner': self.book_1.owner_id,
            },

        ]
        self.assertEqual(expected_data, data)
