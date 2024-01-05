FROM python:3.11

COPY requirements.txt .

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY reddit.py .
COPY files /files
COPY cogs /cogs
COPY .env .

CMD ["python", "main.py"]
