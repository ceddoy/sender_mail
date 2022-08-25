FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app_work
COPY requirements.txt /app_work/
RUN pip install -r requirements.txt
COPY . /app_work/
