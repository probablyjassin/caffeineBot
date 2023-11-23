FROM python:3.11

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY reddit.py .
COPY files /files
COPY cogs /cogs
COPY .env .

CMD ["python", "main.py"]