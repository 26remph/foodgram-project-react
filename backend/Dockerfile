#FROM python:3.7-slim
FROM python:3.9.14-slim-bullseye
LABEL author='remph' email='v.bars@vidim.ru'\
      project='foodgram' version='1.0' \
      description='Ya-prktikum diplom work.'\
      vendor='X26' git='26Remph'

RUN mkdir /app
COPY ["../", "/app"]
RUN python -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN python3 ./app/manage.py makemigrations
WORKDIR /app

#WORKDIR /app
#COPY enrollment/requirements.txt .
#RUN pip3 install -r requirements.txt --no-cache-dir
#COPY ./ .

#CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
ENTRYPOINT ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
