FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

ENV VAULTER_APP='Production'

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["python3", "-m", "flask", "--app", "vaulter", "--debug", "run", "--host=0.0.0.0"]

EXPOSE 5000