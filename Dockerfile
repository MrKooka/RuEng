FROM python:3.8
COPY . /app
EXPOSE 5000
WORKDIR /app
RUN python3 -m pip install --upgrade pip &&\
	python -m pip install --upgrade setuptools &&\
	pip install -r requirements.txt

CMD ["gunicorn","-w","3","-b","0.0.0.0:5000","wsgi:app"]