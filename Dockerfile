FROM python:3.7-slim

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1
ENV HOME /opt/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    	python-psycopg2 \
    	gettext \
    	libpq-dev \
    	gcc \
    	python-dev \
        libffi-dev \
        libpango1.0-0 \
        libcairo2 \
        postgresql-client \
        locales \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p $HOME

WORKDIR $HOME
COPY requirements.txt $HOME
RUN pip install -U pip && pip install -r requirements.txt \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && sed -i -e 's/# en_US ISO-8859-1/en_US ISO-8859-1/' /etc/locale.gen \
    && sed -i -e 's/# es_CO.UTF-8 UTF-8/es_CO.UTF-8 UTF-8/' /etc/locale.gen \
    && sed -i -e 's/# es_CO ISO-8859-1/es_CO ISO-8859-1/' /etc/locale.gen \
    && echo 'LANG="en_US.UTF-8"'>/etc/default/locale \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG=en_US.UTF-8

COPY . $HOME

# Run migrations and collect static files
# CMD ["entrypoint.sh"] # This is not running because when the image gets built all the
# env vars in settings.py are missing

#ENV PATH /env/bin:$PATH

# RUN chmod +x /opt/app/entrypoint.sh
#
# ENTRYPOINT entrypoint.sh

# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate --noinput

EXPOSE 8000

# Collect static files
#CMD ["python", "manage.py", "collectstatic", "--noinput"]

# Apply database migrations
#CMD ["python", "manage.py", "migrate", "--noinput"]

CMD ["gunicorn", "--name", "apitude-app", "--config", "gunicorn.ini.py", "coins.wsgi:application"]
