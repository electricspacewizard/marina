FROM python:3.7

RUN pip3 install psycopg2
RUN pip3 install flask
RUN pip3 install boto3
RUN pip3 install python-dotenv

WORKDIR /app
COPY . /app

EXPOSE 80
ENV IN_DOCKER 1

CMD ["python3", "app.py"]