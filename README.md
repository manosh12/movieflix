1.Clone the repository:
 https://github.com/manosh12/movieflix.git
 OR
 git@github.com:manosh12/movieflix.git

2.Create and activate a virtual environment:
 python -m venv venv
 source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
 pip install -r requirements.txt

create a .env

Add printed secret key to .env SECRET_KEY
 python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Run Migrations
 python manage.py migrate

Create a superuser:
 python manage.py createsuperuser

Start the development server:
 python manage.py runserver

