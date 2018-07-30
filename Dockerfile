FROM python:3.6-alpine

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

ENV FLASK_APP manage.py
ENV flask_config production

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky


COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY manage.py config.py boot.sh ./

RUN ls -l

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
