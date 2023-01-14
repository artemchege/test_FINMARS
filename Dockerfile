FROM python:3.9-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]