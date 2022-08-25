FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /receiver
COPY requirements.txt /receiver/
RUN pip install -r requirements.txt
COPY . /receiver/