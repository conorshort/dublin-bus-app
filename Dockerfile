# FROM python3.8:-alpine

# ENV PYTHONBUFFERED 1

# COPY ./requirements.txt /requirements.txt

# RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
# RUN pip install -r /requirements.txt
# RUN apk del .tmp

# RUN mkdir /app
# COPY . /app/
# WORKDIR /app
# COPY ./scripts /scripts

# RUN chmod +x /scripts/*

# RUN mkdir -p /vol/web/media
# RUN mkdir -p /vol/web/static

# RUN adduser -D user
# RUN chown -R user:user /vol
# # 755 is so user called user has full acces but everyone else has read access 
# RUN chmod -R 755 /vol/web
# USER user

# # entrypoint to app which will run uwsgi and start django app
# CMD ["entrypoint.sh"]

FROM python:3

ENV PYTHONBUFFERED 1

# copy all the files to the container
COPY ./WebApp /app

# set a directory for the app
WORKDIR /app


# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 8000

CMD ["entrypoint.sh"]