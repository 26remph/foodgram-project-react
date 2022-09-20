FROM python:3.7-slim
LABEL author='v.bars@vidim.ru' version='1.0'

RUN mkdir /app
COPY ../ /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN python3 ./app/manage.py makemigrations
WORKDIR /app

#WORKDIR /app
#COPY enrollment/requirements.txt .
#RUN pip3 install -r requirements.txt --no-cache-dir
#COPY ./ .

CMD ["gunicorn", "enrollment.wsgi:application", "--bind", "0:80"]
