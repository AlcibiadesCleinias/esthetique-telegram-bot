FROM python:3.9.5-slim

WORKDIR /opt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY src/requirements.txt /opt/.

RUN apt-get update \
    && apt-get install gcc netcat -y \
    && apt-get clean

RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt

COPY src/ /opt/

#ENTRYPOINT ["/opt/entrypoint.sh"]  # todo: interactive?
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port",  "8000"]
