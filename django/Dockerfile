FROM python:2.7
RUN ["pip","install","Django==1.9","numpy","sympy","django-redis","gunicorn","pymongo"]
RUN mkdir -p /code
WORKDIR /code
EXPOSE 8000
#CMD python manage.py runserver 0.0.0.0:8000
CMD gunicorn -w 3 -b 0.0.0.0:8000 --access-logfile - composeexample.wsgi 
