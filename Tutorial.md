~~~shell
$ pip install -r requirements.txt
~~~
~~~shell
$ pip freeze > requirements.txt
~~~

<a name="top"></a>
### Tutorial
1. Create <a href="#project">project</a>
2. Create <a href="#databases">Databases</a>
3. Create <a href="#store">store</a>
4. Create <a href="#oauth">OAuth</a>
5. <a href="#crud">CRUD</a>
6. Create <a href="#permissions">Permissions</a>
7. Create <a href="#like">Like, Bookmarks, Rating </a>
8. Create <a href="#annotation">Annotation and Aggregation </a>
9. Оптимизация SQL запросов в <a href="#orm">ORM</a>
10. Caching <a href="#fields">fields</a>



### 1. Create project: <a name="project"></a>
   ```
   python manage.py startapp .....
   ```
---


### 2. Databases: <a name="databases"></a>

1.

* https://docs.djangoproject.com/en/4.1/ref/databases/
* https://docs.djangoproject.com/en/4.1/ref/databases/#postgresql-notes
* https://www.postgresql.org/download/
* https://postgresapp.com/

- CREATE DATABASE book_store_db;
- CREATE ROLE book_store_username with password 'book_store_password';
- ALTER ROLE "book_store_username" WITH LOGIN;
- GRANT ALL PRIVILEGES ON DATABASE "book_store_db" to book_store_username;
- ALTER USER book_store_username CREATEDB;

psycopg2.errors.InsufficientPrivilege:
- GRANT postgres TO book_store_username;

```shell
sudo su - postgres
psql

\list

\c book_store_db

\dt

```

2. settings.py

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "book_store_db",
        "USER": "book_store_username",
        "PASSWORD": "book_store_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

3. migrate
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
4. Create createsuperuser
   ```
   python manage.py createsuperuser
   ```

---




### 2. app store: <a name="store"></a>

1. Create app store
   ```
   python manage.py startapp store
   ```

2. Registration  app store:
   ```
   _django_rest_framework_lessons_/settings.py -> 
   
   INSTALLED_APPS = [
      ....
    'store',
      ....
   ]
   ```

3. Create models:
   ```
   store -> models.py
   
   Book
   ```
   ```
   python manage.py makemigrations
   python manage.py migrate
   ``` 


4. Registration in admin panel:
   ```
   store -> admin.py
   
   BookAdmin
   ```

5. Create serializers:
   ```
   store -> serializers.py
   
   BooksSerializer
   ```

6. Create Views:
   ```
   store -> views.py 
   
   class BookViewSet(ModelViewSet)
   ```

7. Add the URLs:
   ```
   _django_rest_framework_lessons_ -> urls.py added urlpatterns
   
   router = SimpleRouter()

   router.register(r'book', BookViewSet)

   urlpatterns += router.urls
   ```


8. Test serializers

    * pip install django-extensions
       ```
          INSTALLED_APPS = (
              ...
              'django_extensions',
          )
        ```
       ```
       python manage.py shell_plus
       ```

   
   ```
   Book.objects.create(name='Test_book_1', price='500.00')
   Book.objects.create(name='Test_book_2', price='600.00')
   ```

   [&#8658; test serializers ](http://127.0.0.1:8000/book/?format=json)

9. Create TestCase

   ```
   store/tests -> test_api.py
   
   BooksApiTestCase
   ```
   ```
   url = reverse('book-list') - all
   
   url = reverse('book-detail') + pk - single
   ```
   
   ```
   store/tests -> test_serializers.py
   
   BookSerializerTestCase
   ```

10. [Filtering in django-rest-framework](https://www.django-rest-framework.org/api-guide/filtering/)

       ```
       store -> views.py
    
       class BookViewSet(ModelViewSet):
           ...
            filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
            filterset_fields = ['price']
            search_fields = ['name', 'author_name', 'description']
            ordering_fields = ['price', 'author_name']
       ```
    
       ```
       _django_rest_framework_lessons_ -> settings.py
    
       REST_FRAMEWORK = {
       'DEFAULT_RENDERER_CLASSES': (
           'rest_framework.renderers.JSONRenderer',
       ),
       'DEFAULT_PARSER_CLASSES': (
           'rest_framework.parsers.JSONParser',
       )
       }
       ```
    
   #### test:

- [all](http://127.0.0.1:8000/book/) :
   ```
   [{"id":7,"name":"Test_book_1","price":"500.00","author_name":"author_1","description":""},
  {"id":9,"name":"test_3","price":"555.00","author_name":"author_3","description":"django"},
  {"id":8,"name":"Test_book_2 django","price":"600.00","author_name":"author_2","description":""}]
   ```
- [filterset_fields = ['price']](http://127.0.0.1:8000/book/?price=500) :
   ```
   [{"id":7,"name":"Test_book_1","price":"500.00","author_name":"author_1","description":""}]
   ```
- [search_fields = ['django']](http://127.0.0.1:8000/book/?search=django)
   ```
   [{"id":9,"name":"test_3","price":"555.00","author_name":"author_3","description":"django"},
  {"id":8,"name":"Test_book_2 django","price":"600.00","author_name":"author_2","description":""}]
   ```
- [ordering_fields = ['-price']](http://127.0.0.1:8000/book/?ordering=-price)
   ```
   [{"id":8,"name":"Test_book_2 django","price":"600.00","author_name":"author_2","description":""},
  {"id":9,"name":"test_3","price":"555.00","author_name":"author_3","description":"django"},
  {"id":7,"name":"Test_book_1","price":"500.00","author_name":"author_1","description":""}]
   ```
  
11. Continued TestCase

   ```
   store/tests -> test_api.py
   
   BooksApiTestCase
   ```
   ```
   store/tests -> test_serializers.py
   
   BookSerializerTestCase
   ```


### 4. Create OAuth: <a name="oauth"></a>

* [Tutorial 4: Authentication & Permissions](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/)
* [Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
* [Python Social Auth, Django Framework](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html)
* [GitHub](https://python-social-auth.readthedocs.io/en/latest/backends/github.html)

- authenticity = подлинность
- authorization(permissions) = предоставление определённому лицу или группе лиц прав на выполнение определённых действий

1. added
   ```
   _django_rest_framework_lessons_/settings.py -> 
    
    INSTALLED_APPS = (
        ...
        'social_django',
        ...
    )
     ```
    ```
    AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    )
    ```
    ```
    # GITHUB
    SOCIAL_AUTH_JSONFIELD_ENABLED = True
    SOCIAL_AUTH_GITHUB_KEY = env('SOCIAL_AUTH_GITHUB_KEY')
    SOCIAL_AUTH_GITHUB_SECRET = env('SOCIAL_AUTH_GITHUB_SECRET')
    ```
   
2. Add the URLs:
   ```
   _django_rest_framework_lessons_ -> urls.py added urlpatterns
   
    urlpatterns = patterns('',
        ...
        re_path('', include('social_django.urls', namespace='social')),
        path('auth/', auth),
        ...
    )
   ```
3. Create Views:
   ```
   store -> views.py
   
   def auth(request):
      return render(request, 'oauth.html')
   ```
    ```
   store -> views.py
   
   class BookViewSet(ModelViewSet):
      ...
      permission_classes = [IsAuthenticated]
      ...
   ```


### 5. CRUD <a name="crud"></a>
Postman

----------------------------
* [GET http://127.0.0.1:8000/book/](http://127.0.0.1:8000/book/)
![GET.png](img%2FCRUD%2FGET.png)

----------------------------
* [GET http://127.0.0.1:8000/book/6/](http://127.0.0.1:8000/book/6/)
![GET_id.png](img%2FCRUD%2FGET_id.png)

----------------------------
csrftoken
* [GET http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
![csrftoken.png](img%2FCRUD%2Fcsrftoken.png)

----------------------------
* [POST http://127.0.0.1:8000/book/](http://127.0.0.1:8000/book/)
![POST.png](img%2FCRUD%2FPOST.png)

----------------------------
* 201 Created
![POST_1.png](img%2FCRUD%2FPOST_1.png)

----------------------------
* 400 Bad Request
![POST_2.png](img%2FCRUD%2FPOST_2.png)

----------------------------
* [PUT http://127.0.0.1:8000/book/9/](http://127.0.0.1:8000/book/9/)
![PUT.png](img%2FCRUD%2FPUT.png)

----------------------------
* [DELETE http://127.0.0.1:8000/book/9/](http://127.0.0.1:8000/book/9/)
![DELETE.png](img%2FCRUD%2FDELETE.png)


1. Refactor Views:

    ```
   store -> views.py
   
   class BookViewSet(ModelViewSet):
      ...
      permission_classes = [IsAuthenticatedOrReadOnly]
      ...
   ```

2. Continued TestCase

* Checking Previous Tests
   ```pycon
    python manage.py test
   ```

  
* New test:

   ```
   store/tests -> test_api.py
   
   def setUp(self):
       self.user = User.objects.create(username='test_username')
       ... 
   ```
   ```
   store/tests -> test_api.py
   
   def test_05_POST_create(self):
       ...      

   def test_06_PUT_update(self):
       ... 
       
   def test_07_DELETE(self):
       ...          
          
   def test_08_get_id(self):
       ...    
   ```
  
'book-list' - no id  
'book-detail' - have id


### 6. Create Permissions: <a name="permissions"></a>

Любой может открывать книги,  
создавать может только тот, кто авторизован,  
но изменять может только тот, кто создал.

1. Models refactoring:
   ```
   store -> models.py
   
    class Book(models.Model):
        ...
        owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                          null=True)
   ```

2. migrate
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create permissions:
   ```
   store -> permissions.py
   
   class IsOwnerOrStaffOrReadOnly(BasePermission):
   ```

4. Views refactoring:
   ```
   store -> views.py 
   
   class BookViewSet(ModelViewSet)
        ...
        permission_classes = [IsOwnerOrStaffOrReadOnly]
        ...
   
   
        def perform_create(self, serializer):
            serializer.validated_data['owner'] = self.request.user
            serializer.save()  
   
   ```

5. Continued TestCase
   ```pycon
    python manage.py test
   ```

* addition test:

    ```
    store/tests -> test_api.py
    
    def test_05_POST_create(self):
       ...
       self.assertEqual(self.user, Book.objects.last().owner)
    ```
   
    ```
    store/tests -> test_api.py
    
    def setUp(self):
       ... 
       self.book_1 = Book.objects.create(name='Test book 1', price=500,
                                  author_name='Author 1',
                                  owner=self.user)
       ... 
    
    ```

    ```
    store/tests -> test_serializers.py
    
    class BookSerializerTestCase(TestCase):
        def setUp(self):
           ... 
            self.user = User.objects.create(username='test_username_Serializer')
    
            self.book_1 = Book.objects.create(name='Test book 1', price=500,
                                              author_name='Author 1', description='',
                                              owner=self.user)
           ... 
  
        def test_ok(self):
        ...
        'owner': self.book_1.owner_id,
        ...
  
     ```   


* New test:

    ```
    store/tests -> test_api.py
    
    def test_09_PUT_update_not_owner(self):
       ...      
    
    def test_10_PUT_update_not_owner_but_staff(self):
       ...   

    def test_11_DELETE_not_owner(self):
       ...      
    
    def test_12_DELETE_not_owner_but_staff(self):
       ...  
  
    ```


### 7. Like, Bookmarks, Rating: <a name="like"></a>

1. Create models:
   ```
   store -> models.py
   
   UserBookRelation
   ```

2. Models refactoring:
   ```
   store -> models.py
   
    class Book(models.Model):
        ...
        owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, related_name='my_books')
        readers = models.ManyToManyField(User, through='UserBookRelation',
                                     related_name='books')
   ```

```
python manage.py makemigrations
python manage.py migrate
``` 

3. Registration in admin panel:
   ```
   store -> admin.py
   
   UserBookRelationAdmin
   ```
   
4. `python manage.py shell_plus`

    ```
    >>> user = User.objects.last()
    
    >>> user.books.all()
    <QuerySet [<Book: Id 17: Test book 3>]>
    
    >>> user.my_books.all()
    <QuerySet [<Book: Id 16: Test book 2>]>
    
    
    >>> user = User.objects.get(id=1)
    
    >>> user.books.all()
    <QuerySet [<Book: Id 17: Test book 3>, <Book: Id 15: Test book 1>]>
    
    >>> user.my_books.all()
    <QuerySet [<Book: Id 15: Test book 1>]>
    ```
   
my_books = created  
books = UserBookRelation (like/in_bookmarks/rate)


5. Create serializers:  
    id мы берем из self.request.user, поэтому не передаем в сериализоторе
   ```
   store -> serializers.py
   
   UserBookRelationSerializer
   ```

6. Create Views:  
    `lookup_field = 'book'` создаем  для удобства, для фронта подменяя id релейшена на id книги, и реализуем через def get_object
    ```
    store -> views.py 
    
    class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
    ```

7. Add the URLs: 
   ```
   _django_rest_framework_lessons_ -> urls.py 

   router.register(r'book_relation', UserBooksRelationView)

   ```

8. Create TestCase

   ```pycon
    python manage.py test
   ```

* addition test:

    ```
    store/tests -> test_serializers.py
    
    class BookSerializerTestCase(TestCase):
        def test_ok(self):
        ...
        'readers': [],
        ...
  
     ```   
  
* New test:

   ```
   store/tests -> test_api.py
   
   BooksRelationTestCase
   ```


### 8. Create Annotation and Aggregation: <a name="annotation"></a>

1. Serializers refactoring:
    Создаем свое поле, но это поля создает еще дополнительный запрос в базу данных
    на каждый объект (книгу), проблема n+1
    self - это сам сериализатор, а instance - это то что мы сериализуем 
   ```
   store -> serializers.py
   
   class BooksSerializer(ModelSerializer):
        likes_count = serializers.SerializerMethodField()
        ...
   
        def get_likes_count(self, instance):
            ...
   ```
   
2. addition test_serializers:
    
    ```
    store/tests -> test_serializers.py
    
    class BookSerializerTestCase(TestCase):
        def setUp(self):
        ...
        user1 = 
        user2 = 
        user3 = 
        ...
  
     ```  

    ```
    store/tests -> test_serializers.py
    
    class BookSerializerTestCase(TestCase):
        def test_ok(self):
        ...
        'readers': [2, 3, 4],
        'likes_count': 3,
        ...
  
     ```  
   
3. Annotation, View refactoring:
    Аннотируем каждую книгу, присваиваем вот этому полю annotated_likes количество (Count)
    в случае (Case), когда (When) userbookrelation__like=True. И оно его сериализует через IntegerField

    ```
    store -> views.py 
    
    class BookViewSet(ModelViewSet):
            queryset = Book.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                rating=Avg('userbookrelation__rate')
            ).order_by('id')
               ...
    ```
4. Serializers refactoring:

   ```
   store -> serializers.py
   
   class BooksSerializer(ModelSerializer):
        ...
        annotated_likes = serializers.IntegerField(read_only=True)
        rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

        class Meta:
            fields = ('id', 'name', 'price', 'author_name', 'description', 'owner', 'readers',
                  'likes_count', 'annotated_likes', 'rating')

   ```

5. addition test_serializers:
    
    ```
    store/tests -> test_serializers.py
    
    class BookSerializerTestCase(TestCase):
        def setUp(self):
        ...
        rate=
        ...
  
     ```  

    ```
    store/tests -> test_serializers.py
    
    class BookSerializerTestCase(TestCase):
        def test_ok(self):
            books = Book.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                rating=Avg('userbookrelation__rate')
            ).order_by('id')
   
            ...
            'annotated_likes': 3,
            'rating': '4.67'
            ...
  
     ```  

6. addition test_api:

    ```
    store/tests -> test_api.py
    
    def setUp(self):
       ... 
       UserBookRelation.objects.create(user=self.user, book=self.book_1, like=True,
                                        rate=5)
       ... 
    
   
    def test_01_get(self):
       ... 
       books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
       ... 
   
        self.assertEqual(serializer_data[0]['rating'], '5.00')
        self.assertEqual(serializer_data[0]['likes_count'], 1)
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)
       ... 
   

   
    def test_02_get_filter(self):
       ... 
       books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
       ... 

   
   
    def test_03_get_search(self):
       ... 
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
       ... 

   
    def test_04_get_ordering(self):
       ... 
        books = Book.objects.annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('-price')
        serializer_data = BooksSerializer(books, many=True).data
       ... 
 
   
   
    def test_08_get_id(self):
       ... 
        books = Book.objects.filter(id__in=[self.book_1.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
       ...      
   
       self.assertEqual(serializer_data[0], response.data)
   
   
    ```


### 9. Оптимизация SQL запросов ORM: <a name="orm"></a>  

https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

1. Install the App:
   ```
   _django_rest_framework_lessons_/settings.py -> 
   
   INSTALLED_APPS = [
      ....
    "debug_toolbar",
      ....
   ]
   
   MIDDLEWARE = [
        # ...
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        # ...
    ]
   
   
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
   
   ```

2. Add the URLs:
   ```
   _django_rest_framework_lessons_ -> urls.py 
   
    if settings.DEBUG:
        urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
   ```

3. Add django-debug-toolbar-force:  
https://django-debug-toolbar-force.readthedocs.io/en/latest/

   ```
   _django_rest_framework_lessons_/settings.py -> 

   MIDDLEWARE = [
        # ...
        'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',
        # ...
    ]

   ```

    `GET http://127.0.0.1:8000/book/?debug-toolbar`

4. N+1 
![1.png](img%2FSQL_optimization%2F1.png)
* Serializers refactoring:
    
   ```
   store -> serializers.py
   
   class BooksSerializer(ModelSerializer):
        DEL likes_count

   ```
  ![2.png](img%2FSQL_optimization%2F2.png)

* test_api and test_serializers refactoring

5. addition owner_name in serializers:

   ```
   store -> serializers.py
   
   class BooksSerializer(ModelSerializer):
        ...
        owner_name = serializers.CharField(source='owner.username', default="",
                                   read_only=True)

   ```
   ![3.png](img%2FSQL_optimization%2F3.png)


* views refactoring:

    ```
    store -> views.py 
    
    class BookViewSet(ModelViewSet):
            queryset = Book.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                rating=Avg('userbookrelation__rate')
            ).select_related('owner').order_by('id')
               ...
    ```
    ![4.png](img%2FSQL_optimization%2F4.png)

6. Create serializers:
   ```
   store -> serializers.py
   
   BookReaderSerializer
   ```
   
7. addition readers in serializers:

   ```
   store -> serializers.py
   
   class BooksSerializer(ModelSerializer):
        ...
        readers = BookReaderSerializer(many=True, read_only=True)

   ```
   ![5.png](img%2FSQL_optimization%2F5.png)
   
* views refactoring:
    ```
    store -> views.py 
    
    class BookViewSet(ModelViewSet):
          queryset = Book.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                rating=Avg('userbookrelation__rate')
          ).select_related('owner').prefetch_related('readers').order_by('id')
                 ...
    ```
    ![6.png](img%2FSQL_optimization%2F6.png)


8. addition test_serializers:
    
    ```
    store/tests -> test_serializers.py
    
    class BookSerializerTestCase(TestCase):
        def setUp(self):
        ...
        first_name='', last_name='')
        ...
  
     ```  

    ```
    store/tests -> test_serializers.py
    
    class BookSerializerTestCase(TestCase):
        def test_ok(self):
            books = Book.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                rating=Avg('userbookrelation__rate')
            ).order_by('id')
   
            ...
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
            ...
  
     ```

9. addition test_api:
    Тест SQL запросов, отлавливаем количество запросов

    ```
    store/tests -> test_api.py
   
    def test_01_get(self):
       ... 
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(2, len(queries))
       ... 
    ```    


```
python manage.py test
```


### 10. Caching fields: <a name="fields"></a>

Рейтинг будем пересчитывать только по событию лайка  
Переносим рейтинг (rating) из class BookViewSet(ModelViewSet) в class Book(models.Model).

1. Models refactoring:
   ```
   store -> models.py
   
    class Book(models.Model):
        ...
        rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)
   ```

2. migrate
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create utils:

    ```
    store -> utils.py
    
    def set_rating(book):
       ...
    ```

4. Create test_rating:

   ```
   store/tests -> test_rating.py
    
   class SetRatingTestCase(TestCase):
      ...
   ```
   
5. Models refactoring:
    ```
    store -> models.py
    
    class UserBookRelation(models.Model):
         ...
   
        def __init__(self, *args, **kwargs):
            super(UserBookRelation, self).__init__(*args, **kwargs)
            self.old_rate = self.rate
        
        def save(self, *args, **kwargs):
            creating = not self.pk
        
            super().save(*args, **kwargs)
        
            if self.old_rate != self.rate or creating:
                from store.utils import set_rating
                set_rating(self.book)
    ```
   
6. test_serializers refactoring:

   ```
    class BookSerializerTestCase(TestCase):
        def setUp(self):
            user_book_3 = UserBookRelation.objects.create(user=self.user3, book=self.book_1, like=True)
            user_book_3.rate = 4
            user_book_3.save()
   ```

   ```
    class BookSerializerTestCase(TestCase):
        def test_ok(self):
            books = Book.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
            ).order_by('id')
   ```

7. test_api refactoring:

   ```
    class BookSerializerTestCase(TestCase):
        def test_ok(self):
            books = Book.objects.all().annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
            ).order_by('id')
   ```


```
python manage.py test
```


<a href="#top">UP</a>