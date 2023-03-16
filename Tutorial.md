~~~shell
$ pip install -r requirements.txt
~~~
~~~shell
$ pip freeze > requirements.txt
~~~

<a name="top"></a>
### Tutorial
1. Create <a href="#project">project</a>
2. Create <a href="#Databases">Databases</a>
3. Create <a href="#store">store</a>







### 1. Create project: <a name="project"></a>
   ```
   python manage.py startapp .....
   ```
---


### 2. Databases: <a name="Databases"></a>

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






---




























































<a href="#top">UP</a>