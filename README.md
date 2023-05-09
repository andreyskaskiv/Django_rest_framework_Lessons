<a name="top"></a>

#### Stack:
- Django==4.1.7
- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)

### Tutorial: <a href="Tutorial.md">click</a>

1. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
2. toolbar

   [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)  
   `python -m pip install django-debug-toolbar`
   
   [django-debug-toolbar-force](https://django-debug-toolbar-force.readthedocs.io/en/latest/)  
   `python -m pip install django-debug-toolbar-force`

3. migrate

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
4. runserver  
   `python manage.py runserver`

5. [administration](http://127.0.0.1:8000/admin/login/?next=/admin/)
6. [serializers](http://127.0.0.1:8000/book/?format=json)




<a href="#top">UP</a>