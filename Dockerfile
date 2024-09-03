FROM python:3.12

WORKDIR /app

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .

ENV PYTHONUNBUFFERED 1

CMD ["python", "manage.py", "csu"]