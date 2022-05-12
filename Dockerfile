FROM python:slim

COPY . /tmp/discord/
RUN pip install -r /tmp/discord/requirements.txt

ENTRYPOINT ["python", "/tmp/discord/bot/main.py"]