FROM python:3.10

WORKDIR /todo-lr1/app

COPY ./requirements.txt /todo-lr1/requirements.txt

RUN pip install --default-timeout=1000 --no-cache-dir --upgrade -r /todo-lr1/requirements.txt

COPY ./app /todo-lr1/app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
