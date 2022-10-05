FROM python:3.7-alpine
WORKDIR /setter
ENV PATH=$PATH:.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8120
COPY . .
RUN python manage.py migrate
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8120"]
