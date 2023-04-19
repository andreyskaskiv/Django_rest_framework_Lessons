from django.db.models import Avg

from store.models import UserBookRelation


def set_rating(book):
    """Rating setting function"""
    rating = UserBookRelation.objects.filter(book=book).aggregate(rating=Avg('rate')).get('rating')
    book.rating = rating
    book.save()
