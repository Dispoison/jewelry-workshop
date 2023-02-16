# Jewelry workshop

To prepare the project run the following commands:
```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cp .env.development.example .env

python manage.py makemigrations
python manage.py migrate
python manage.py create_admin
python manage.py db_init
```


To run the project run the following commands:
```
python manage.py runserver
```

To get to the administration panel, follow this link:
http://127.0.0.1:8000/admin/  
And login with username: `admin` and password: `admin`