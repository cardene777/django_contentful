# django_contentful
import data into contentful

## Command
python manage.py makemigrations && python manage.py migrate && python manage.py loaddata fixture/hospital.json && python manage.py loaddata fixture/category.json && python manage.py loaddata fixture/tag.json && python manage.py createsuperuser

