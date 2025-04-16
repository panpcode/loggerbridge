FROM python:3.9-slim

WORKDIR /app

COPY . /app
COPY package/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "-m", "flask", "run"]