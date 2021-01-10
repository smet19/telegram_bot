FROM python:3.8.5

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "echo_bot.py"]