FROM python:3.8.0

RUN mkdir /code
WORKDIR /code

COPY . /code

RUN pip install --upgrade pip && pip install -r requirements.txt 

RUN echo "hahaha"

CMD ["python", "runserver","manager.py"]