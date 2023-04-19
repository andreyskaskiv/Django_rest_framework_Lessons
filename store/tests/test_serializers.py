from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username_Serializer')

        self.user1 = User.objects.create(username='user1',
                                         first_name='Ivan', last_name='Petrov')
        self.user2 = User.objects.create(username='user2',
                                         first_name='Ivan', last_name='Sidorov')
        self.user3 = User.objects.create(username='user3',
                                         first_name='1', last_name='2')

        self.book_1 = Book.objects.create(name='Test book 1', price=500,
                                          author_name='Author 1', description='',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=777,
                                          author_name='Author 5', description='',
                                          owner=self.user)
        self.book_3 = Book.objects.create(name='Test book Author 1', price=777,
                                          author_name='Author 2', description='',
                                          owner=self.user)

        UserBookRelation.objects.create(user=self.user1, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book_1, like=True,
                                        rate=5)
        user_book_3 = UserBookRelation.objects.create(user=self.user3, book=self.book_1, like=True)
        user_book_3.rate = 4
        user_book_3.save()

        UserBookRelation.objects.create(user=self.user1, book=self.book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=self.user2, book=self.book_2, like=True,
                                        rate=4)
        UserBookRelation.objects.create(user=self.user3, book=self.book_2, like=False)

    def test_01_ok(self):
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
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
                'readers': [{
                    'first_name': 'Ivan',
                    'last_name': 'Petrov'
                },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    },
                ],
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': self.user.username,
            },
            {
                'id': self.book_2.id,
                'name': 'Test book 2',
                'price': '777.00',
                'author_name': 'Author 5',
                'description': '',
                'owner': self.book_1.owner_id,
                'readers': [{
                    'first_name': 'Ivan',
                    'last_name': 'Petrov'
                },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    },
                ],
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': self.user.username,
            },
            {
                'id': self.book_3.id,
                'name': 'Test book Author 1',
                'price': '777.00',
                'author_name': 'Author 2',
                'description': '',
                'owner': self.book_1.owner_id,
                'readers': [],
                'annotated_likes': 0,
                'rating': None,
                'owner_name': self.user.username,
            },

        ]

        # print()
        # print(f"data => {data}")
        # print()
        # print(f"expected_data => {expected_data}")

        self.assertEqual(expected_data, data)
