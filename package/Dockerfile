FROM python:3.9-slim

WORKDIR /app

COPY package/requirements.txt /app/requirements.txt
COPY templates /app/templates
COPY app.py /app/app.py
COPY logger_control.py /app/logger_control.py
COPY logger_reader.py /app/logger_reader.py
COPY modbus_device.py /app/modbus_device.py
COPY modbus_reader.py /app/modbus_reader.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run loggerbridge 
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]