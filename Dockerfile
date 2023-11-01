FROM python:3.10

WORKDIR /app
COPY app /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["sh", "-c", "python flaskapp.py & python schedule_discord.py"]

