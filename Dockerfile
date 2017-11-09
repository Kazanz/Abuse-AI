FROM strayge/alpine-py3-numpy-scipy

RUN apk add --no-cache nginx supervisor
RUN apk add --no-cache python3-dev build-base linux-headers pcre-dev

RUN chown -R nginx:www-data /var/lib/nginx
RUN mkdir /etc/nginx/sites-enabled
RUN mkdir /run/nginx
RUN rm /etc/nginx/nginx.conf
ADD docker/nginx/nginx.conf /etc/nginx/
ADD docker/nginx/nginx-app.conf /etc/nginx/sites-enabled/

RUN pip install https://github.com/unbit/uwsgi/archive/uwsgi-2.0.zip#egg=uwsgi
RUN mkdir /etc/uwsgi
ADD docker/uwsgi /etc/uwsgi/

RUN rm /etc/supervisord.conf
ADD docker/supervisord/supervisord.conf /etc/

EXPOSE 80

RUN mkdir /app
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install flask 
RUN pip install flask-apispec 
RUN pip install numpy 
RUN pip install scipy 
RUN pip install scikit-learn

ADD app.py /app/app.py
ADD wsgi.py /app/wsgi.py
ADD templates /app/templates
ADD static /app/static
ADD model.pickle /app/model.pickle

ENV PYTHONPATH /app/

CMD supervisord -n
