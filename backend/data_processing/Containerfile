FROM python:3.11-alpine

RUN apk update --no-cache
RUN apk upgrade

WORKDIR /app

COPY . /app

RUN python3 -m venv .venv
RUN /bin/sh -c "source .venv/bin/activate"

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

CMD flask run --port 3000 --host 0.0.0.0
