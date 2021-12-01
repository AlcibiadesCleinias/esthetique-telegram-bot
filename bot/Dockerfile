FROM python:3.9.5-slim

WORKDIR /opt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install gcc netcat -y \
    && apt-get clean

COPY src/requirements.txt /opt/.
RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt

COPY src/ /opt/

CMD ["python", "main.py"]
