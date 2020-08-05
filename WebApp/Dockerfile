FROM python:3.8.5-buster as builder



WORKDIR /usr/src/app


ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip 

COPY ./requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt







FROM python:3.8.5-buster

RUN mkdir -p /home/app

RUN addgroup --system app && useradd --system app -g app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static

WORKDIR $APP_HOME


COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*


# copy project
COPY . $APP_HOME



# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user


 
