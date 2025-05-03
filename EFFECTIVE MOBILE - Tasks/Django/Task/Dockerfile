FROM python:3.11-slim

COPY requirements.txt /temp/requirements.txt

RUN apt-get update && apt-get install -y build-essential libpq-dev

RUN pip install --no-cache-dir -r /temp/requirements.txt

COPY dog_api /dog_api/

WORKDIR /dog_api

EXPOSE 8000

RUN adduser --disabled-password service-user

USER service-user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
