FROM musk96/python-mariadb:latest
WORKDIR /code/
COPY . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]