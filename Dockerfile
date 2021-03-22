FROM python:3.7

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip3 install flask && pip3 install flask-sqlalchemy && pip3 install pymysql

EXPOSE 5000
EXPOSE 27017

CMD ["python3","wsgi.py"]