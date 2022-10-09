FROM python:3.10

LABEL maintainer="serhii.vlakh@gmail.com"

EXPOSE 8080

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/api
COPY ./db /code/db

RUN mkdir upload

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]