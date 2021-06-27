# Rest Django

### Versions
* Python 3.6.9
* Django 3.2.4
* Django Rest Framework 3.12.4

### Installation

1. Clone the repository
2. Go to the root folder and create the environment: `python3 -m venv env`
3. Then, activate it: `source env/bin/activate`
4. Install dependencies with `pip3`: `pip3 install -r requirements.txt`
5. Run migrations (if there's not database): `python3 manage.py migrate`
6. Go to the root folder and run the server: `python3 manage.py runserver`

### How to run tests
* Tests using Coverage
  1. `coverage run --source='.' manage.py test blog`
  2. `coverage report --omit=*/env/*,*/app/*,manage.py`

### Commands
* `python3 manage.py seed_post [post_quantity]`: this command create mock objects for table post, also post_quantity is a required argument, integer and must be greater than 0

### Useful resources
* At the `postman` folder, there's Postman Collection to test the API