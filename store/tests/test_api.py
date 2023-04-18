import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Case, When, Avg
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')

        self.book_1 = Book.objects.create(name='Test book 1', price=500,
                                          author_name='Author 1',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=777,
                                          author_name='Author 5')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=777,
                                          author_name='Author 2')

        UserBookRelation.objects.create(user=self.user, book=self.book_1, like=True,
                                        rate=5)

    def test_01_get(self):
        url = reverse('book-list')

        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(2, len(queries))

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rating'], '5.00')
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)

    def test_02_get_filter(self):
        url = reverse('book-list')
        books = Book.objects.filter(id__in=[self.book_2.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        response = self.client.get(url, data={'price': 777})
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_03_get_search(self):
        url = reverse('book-list')
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_04_get_ordering(self):
        url = reverse('book-list')
        books = Book.objects.annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('-price')
        response = self.client.get(url, data={'ordering': '-price'})
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_05_POST_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "Test book 3",
            "price": "988.00",
            "author_name": "Author 3",
            "description": "DESCRIPTION"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, json_data,
                                    content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_06_PUT_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 69,
            "author_name": self.book_1.author_name,
            "description": self.book_1.description
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(69, self.book_1.price)

    def test_07_DELETE(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))

        self.client.force_login(self.user)
        response = self.client.delete(url,
                                      content_type='application/json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())

    def test_08_get_id(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        books = Book.objects.filter(id__in=[self.book_1.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        response = self.client.get(url)
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data[0], response.data)

    def test_09_PUT_update_not_owner(self):
        self.user_not_owner = User.objects.create(username='test_username_not_owner', )
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 69,
            "author_name": self.book_1.author_name,
            "description": self.book_1.description
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_not_owner)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.book_1.refresh_from_db()
        self.assertEqual(500, self.book_1.price)

    def test_10_PUT_update_not_owner_but_staff(self):
        self.user_not_owner = User.objects.create(username='test_username_not_owner',
                                                  is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 69,
            "author_name": self.book_1.author_name,
            "description": self.book_1.description
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_not_owner)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(69, self.book_1.price)

    def test_11_DELETE_not_owner(self):
        self.assertEqual(3, Book.objects.all().count())
        self.user_not_owner = User.objects.create(username='test_username_not_owner', )
        url = reverse('book-detail', args=(self.book_1.id,))

        self.client.force_login(self.user_not_owner)
        response = self.client.delete(url,
                                      content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.assertEqual(3, Book.objects.all().count())

    def test_12_DELETE_not_owner_but_staff(self):
        self.assertEqual(3, Book.objects.all().count())
        self.user_not_owner = User.objects.create(username='test_username_not_owner',
                                                  is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))

        self.client.force_login(self.user_not_owner)
        response = self.client.delete(url,
                                      content_type='application/json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())


class BooksRelationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username', )
        self.user_2 = User.objects.create(username='test_username_2', )

        self.book_1 = Book.objects.create(name='Test book 1', price=500,
                                          author_name='Author 1',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=777,
                                          author_name='Author 5')

    def test_01_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))

        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)
        self.assertTrue(relation.like)

    def test_02_in_bookmarks(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)
        self.assertTrue(relation.in_bookmarks)

    def test_03_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))

        data = {
            "rate": 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)
        self.assertEqual(3, relation.rate)

    def test_04_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))

        data = {
            "rate": 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
