from setuptools import setup, find_packages

setup(
    name="event_management_system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Django==4.2.7',
        'djangorestframework==3.14.0',
        'django-cors-headers==4.3.1',
        'drf-spectacular==0.26.5',
        'python-dotenv==1.0.0',
        'Pillow>=10.1.0',
        'django-filter==23.3',
        'drf-yasg==1.21.7',
        'dj-database-url==3.0.1',
        'psycopg2-binary==2.9.9',
        'gunicorn==23.0.0',
    ],
)
