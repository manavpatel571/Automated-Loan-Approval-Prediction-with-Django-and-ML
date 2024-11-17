#!usrbinenv bash
# exit on error
chmod +x build.sh
set -o errexit

pip install -r DjangoAPI/require.txt  

python manage.py collectstatic --no-input
python manage.py migrate
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input --email $DJANGO_SUPERUSER_EMAIL
fi