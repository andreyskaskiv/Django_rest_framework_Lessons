from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username_Serializer')

        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')

        self.book_1 = Book.objects.create(name='Test book 1', price=500,
                                          author_name='Author 1', description='',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=777,
                                          author_name='Author 5', description='',
                                          owner=self.user)
        self.book_3 = Book.objects.create(name='Test book Author 1', price=777,
                                          author_name='Author 2', description='',
                                          owner=self.user)

        UserBookRelation.objects.create(user=user1, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book_1, like=True,
                                        rate=4)

        UserBookRelation.objects.create(user=user1, book=self.book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user2, book=self.book_2, like=True,
                                        rate=4)
        UserBookRelation.objects.create(user=user3, book=self.book_2, like=False)

    def test_ok(self):
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'Test book 1',
                'price': '500.00',
                'author_name': 'Author 1',
                'description': '',
                'owner': self.book_1.owner_id,
                'readers': [2, 3, 4],
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': '4.67'
            },
            {
                'id': self.book_2.id,
                'name': 'Test book 2',
                'price': '777.00',
                'author_name': 'Author 5',
                'description': '',
                'owner': self.book_1.owner_id,
                'readers': [2, 3, 4],
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.50'
            },
            {
                'id': self.book_3.id,
                'name': 'Test book Author 1',
                'price': '777.00',
                'author_name': 'Author 2',
                'description': '',
                'owner': self.book_1.owner_id,
                'readers': [],
                'likes_count': 0,
                'annotated_likes': 0,
                'rating': None
            },

        ]

        # print()
        # print(f"data => {data}")
        # print(f"expected_data => {expected_data}")

        self.assertEqual(expected_data, data)
